# Storing html of Printer search page from amazon

import requests
import os

def fetchAndSaveFile(content, path):
    with open(path, "w") as f:  # Use "wb" for writing binary data
        f.write(content)

url = 'https://www.amazon.in/s?k=printer&crid=B629TTBSAOXK&sprefix=%2Caps%2C232&ref=nb_sb_ss_recent_1_0_recent'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

response = requests.get(url, headers=headers)

fetchAndSaveFile(response.text, os.getcwd() + "/index.html")
