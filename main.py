import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint
import tkinter as tk

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"


def get_all_forms(url):
    soup = bs(s.get(url).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    details = {}
    try:
        action = form.attrs.get("action").lower()
    except:
        action = None
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def is_vulnerable(response):
    errors = {
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
    }
    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False


def scan_sql_injection(url):
    for c in "\"'":
        new_url = f"{url}{c}"
        result_text.insert(tk.END, f"[!] Trying {new_url}\n")
        res = s.get(new_url)
        if is_vulnerable(res):
            result_text.insert(tk.END, f"[+] SQL Injection vulnerability detected, link: {new_url}\n")
            return
    forms = get_all_forms(url)
    result_text.insert(tk.END, f"[+] Detected {len(forms)} forms on {url}.\n")
    for form in forms:
        form_details = get_form_details(form)
        for c in "\"'":
            data = {}
            for input_tag in form_details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    try:
                        data[input_tag["name"]] = input_tag["value"] + c
                    except:
                        pass
                elif input_tag["type"] != "submit":
                    data[input_tag["name"]] = f"test{c}"
            url = urljoin(url, form_details["action"])
            if form_details["method"] == "post":
                res = s.post(url, data=data)
            elif form_details["method"] == "get":
                res = s.get(url, params=data)
            if is_vulnerable(res):
                result_text.insert(tk.END, f"[+] SQL Injection vulnerability detected, link: {url}\n")
                result_text.insert(tk.END, "[+] Form:\n")
                pprint(form_details)
                break


def start_scan():
    url = url_entry.get()
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, f"[+] Scanning: {url}\n")
    scan_sql_injection(url)

# GUI code
root = tk.Tk()
root.title("SQL Injection Scanner")

url_label = tk.Label(root, text="URL:")
url_label.pack(side=tk.LEFT, padx=5)

url_entry = tk.Entry(root, width=50)
url_entry.pack(side=tk.LEFT, padx=5)

scan_button = tk.Button(root, text="Scan", command=start_scan)
scan_button.pack(side=tk.LEFT, padx=5,  pady=10)

result_label = tk.Label(root, text="Result:")
result_label.pack(side=tk.LEFT, padx=2, pady=10)

result_text = tk.Text(root, height=20, width=80)
result_text.pack(side=tk.LEFT, padx=5, pady=10)

root.mainloop()
