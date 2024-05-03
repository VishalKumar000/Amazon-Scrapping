# Storing html of particular printer search page from amazon

import requests
import os

def fetchAndSaveFile(content, path):
    with open(path, "w") as f:  # Use "wb" for writing binary data
        f.write(content)

url = 'https://www.amazon.in/Brother-DCP-T426W-Wi-Fi-Multifunction-Printer/dp/B0B38NFCCQ/ref=sr_1_17_sspa?crid=B629TTBSAOXK&dib=eyJ2IjoiMSJ9.6w4t-HmMeyH7FZI4dH81cnylxYEht9zvUZ03XV_xiLLGjHj071QN20LucGBJIEps.AQBOZbypl-wGnaTvFiQfktlfoJqpfL8az3NfKtH4fs8&dib_tag=se&keywords=printer&qid=1714675686&sprefix=%2Caps%2C232&sr=8-17-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGZfbmV4dA&psc=1'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

response = requests.get(url, headers=headers)

fetchAndSaveFile(response.text, os.getcwd() + "/index.html")
