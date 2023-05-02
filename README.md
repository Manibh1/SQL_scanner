# SQL_Scanner
This is a simple SQL Scanner implemented using Python. It can be used to scan a target website for SQL injection vulnerabilities.
Installation

1. Clone the repository:
git clone https://github.com/Dev2409/sql-scanner.git
2. Install the required dependencies:
pip install -r requirements.txt

## Usage

1. Run the scanner:
python main.py
2. Enter the target website URL and click the "Start Scan" button.
3. The scanner will scan the website for SQL injection vulnerabilities and display the results.

## How it Works

The scanner uses a simple algorithm to scan the website for SQL injection vulnerabilities. It sends GET and POST requests to the website with various parameters and checks the response for SQL errors. If an error is detected, it is reported as a vulnerability.

## Disclaimer

This scanner is for educational purposes only. Do not use it to scan websites without permission. The author is not responsible for any damages caused by the use of this software.
