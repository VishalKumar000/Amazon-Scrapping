import requests
from bs4 import BeautifulSoup
import html
import re
import random
import uuid

# CONSTANTS
obj = {}
exchange_rate_usd_to_inr = 83.38


with open('index.html', 'r') as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, 'html.parser')

# id
random_uuid = uuid.uuid4()
obj['id'] = str(random_uuid)

# title
title = soup.select_one('#productTitle')
title = title.string.strip()
title = html.unescape(title)
obj['title'] = title

# price
price = soup.select('span.a-price-whole')
price = price[0].get_text().replace(',', '').replace('.', '')
price = int(price) / exchange_rate_usd_to_inr
price = round(price, 2)
obj['price'] = price

# image
images = soup.select('.a-button-text>img')
images = map(lambda x: x['src'], images)
images = list(images)
images = filter(lambda url: url.endswith('.jpg') and not url.endswith('_V192234675_.gif'), images)
images = list(images)
obj['images'] = images

# link
link = title.lower()
link = link.replace(' ', '-')
link = re.sub(r'[^a-z0-9-]', '', link)
link = re.sub(r'-+', '-', link)
link = f"/product-detail/{link}"
obj['link'] = link

# tag || brand
tags = soup.select('.a-size-base.po-break-word')
tags = tags[0]
tags = tags.get_text()
tags = [tags.lower()]
obj['tags'] = tags

# rating
rating = soup.select('.a-popover-trigger.a-declarative>span')
rating = rating[0]
rating = rating.get_text(strip=True)
obj['rating'] = rating

# number of review
numberOfReviews = soup.select('#acrCustomerReviewLink')
numberOfReviews = numberOfReviews[0]
numberOfReviews = numberOfReviews.get_text()
numberOfReviews = re.findall(r'\d+', numberOfReviews)
numberOfReviews = ''.join(numberOfReviews)
numberOfReviews = int(numberOfReviews)
obj['numberOfReviews'] = numberOfReviews

# category
categories = soup.select('.a-color-secondary.a-size-base.prodDetSectionEntry')
category = None
for _category in categories:
    if (_category.get_text(strip=True) == "Generic Name"):
        category = _category

if (category):
    category = category.parent
    category = category.select('td')
    category = category[0]
    category = category.get_text(strip=True)

obj['category'] = category

# Status
status_data  =  ["New in", "", "", "50% Discount", "", "",  "limited edition", "", ""]
obj['status'] = status_data[random.randint(0, len(status_data) - 1)]

# Static Attribute
DEMO_VARIANTS = []

obj['type'] = "printer"
obj['variants'] = DEMO_VARIANTS
obj['variantType'] = "image"
obj['sizes'] = ["XS", "S", "M", "L", "XL"]
obj['allOfSizes'] = ["XS", "S", "M", "L", "XL", "2XL", "3XL"]

# Features
features = soup.select('ul.a-unordered-list.a-vertical.a-spacing-mini > li')
for idx, feature in enumerate(features):




# https://www.amazon.in/Brother-DCP-T426W-Wi-Fi-Multifunction-Printer/dp/B0B38NFCCQ/ref=sr_1_17_sspa?crid=B629TTBSAOXK&dib=eyJ2IjoiMSJ9.6w4t-HmMeyH7FZI4dH81cnylxYEht9zvUZ03XV_xiLLGjHj071QN20LucGBJIEps.AQBOZbypl-wGnaTvFiQfktlfoJqpfL8az3NfKtH4fs8&dib_tag=se&keywords=printer&qid=1714675686&sprefix=%2Caps%2C232&sr=8-17-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGZfbmV4dA&th=1