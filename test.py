import requests
from bs4 import BeautifulSoup
import os
import json

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

data = []

# Function to scrape a single page
def scrape_page(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        anchor_tag = soup.find_all(class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")

        for i in anchor_tag:
            data.append('https://amazon.in/' + i['href'])

        # Return the URL of the next page if it exists
        next_button = soup.select('.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator')
        if next_button:
            next_button = next_button[0]
            return 'https://amazon.in/' + next_button['href']
    else:
        print("Failed to fetch page:", url)

# Main function to scrape multiple pages
def scrape_multiple_pages(start_url):
    current_url = start_url
    while current_url:
        print("Scraping:", current_url)
        current_url = scrape_page(current_url)

# Example usage
start_url = "https://www.amazon.in/s?k=printer&crid=B629TTBSAOXK&sprefix=%2Caps%2C232&ref=nb_sb_ss_recent_1_0_recent"
scrape_multiple_pages(start_url)

with open(os.getcwd() + "/data.json", "w") as f:
    json.dump(data, f)