# checking selector of product link and next button in pagination from store html as data source

import requests
from bs4 import BeautifulSoup

with open('index.html', 'r') as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, 'html.parser')

# print(soup.prettify())
# .a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal

print(soup.title)
print(soup.title.name)
print(soup.title.string)

anchor_tag = soup.find_all(class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")

for i in anchor_tag:
    # print('https://amazon.in/' + i['href'])
    pass

print(len(anchor_tag))

arr = soup.select('.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator')

print(arr[0].get('href'))