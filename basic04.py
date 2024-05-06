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
obj['description'] = title

# price
price = soup.select('span.a-price-whole')
price = price[0].get_text().replace(',', '').replace('.', '')
price = int(price) / exchange_rate_usd_to_inr
price = round(price, 2)
obj['price'] = price

# image
# images = soup.select('.a-button-text>img')
# images = map(lambda x: x['src'], images)
# images = list(images)
# images = filter(lambda url: url.endswith('.jpg')
#                 and not url.endswith('_V192234675_.gif'), images)
# images = list(images)
# obj['images'] = images
images = soup.select_one('.a-dynamic-image.a-stretch-vertical')
images = [images['src']]
print('images :: ', images)

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
status_data = ["New in", "", "", "50% Discount",
               "", "",  "limited edition", "", ""]
obj['status'] = status_data[random.randint(0, len(status_data) - 1)]

# Static Attribute
DEMO_VARIANTS = []

obj['type'] = "printer"
obj['variants'] = DEMO_VARIANTS
obj['variantType'] = "image"
obj['sizes'] = ["XS", "S", "M", "L", "XL"]
obj['allOfSizes'] = ["XS", "S", "M", "L", "XL", "2XL", "3XL"]

# Features
featuresArr = soup.select('ul.a-unordered-list.a-vertical.a-spacing-mini > li')

features = '''
<ul class="list-disc list-inside leading-7">
'''
for idx, feature in enumerate(featuresArr):
    featuresArr[idx] = feature.get_text()
    featuresArr[idx] = html.unescape(featuresArr[idx])
    features += f'''
    <li>
        {featuresArr[idx]}
    </li>
    '''

features += '''</ul>'''
obj['features'] = features

# Reviews
reviews_data = [
    {
        "imgUrl": "https://images-eu.ssl-images-amazon.com/images/S/amazon-avatars-global/default._CR0,0,1024,1024_SX460_.png",
        "comment": "thats printer print quality is very good and poor weight and also its value for money and ease of use there compatibility is very good",
        "name": "Aman",
        "starPoint": 5,
        "date": "29 March 2024",
    },
    {
        "imgUrl": "https://images-eu.ssl-images-amazon.com/images/S/amazon-avatars-global/default._CR0,0,1024,1024_SX460_.png",
        "comment": "Printer is good one but wifi is not available in the same.",
        "name": "Mahesh",
        "starPoint": 3,
        "date": "28 March 2024",
    },
    {
        "imgUrl": "https://images-eu.ssl-images-amazon.com/images/S/amazon-avatars-global/default._CR0,0,1024,1024_SX460_.png",
        "comment": "I've replaced my 8 year old hp printer which was costing me a lot of money when it comes to ink and cartridges with this one. It's working just how I expected, I'm using it since 2 weeks now. The tank takes up all the 70ml colour inks at once which were sent apart from the black one (170ml) which is half consumed. I also got an additional bottle of black ink with it.",
        "name": "Kunal",
        "starPoint": 5,
        "date": "31 October 2022",
    },
    {
        "imgUrl": "https://images-eu.ssl-images-amazon.com/images/S/amazon-avatars-global/default._CR0,0,1024,1024_SX460_.png",
        "comment": "It's a good printer at this price point... However it's not a wifi printer as everyone might think by hearing the name, 'smart' I got very disappointed as soon as I found out it's not wifi...",
        "name": "Ryan",
        "starPoint": 4,
        "date": "28 March 2024",
    },
    {
        "imgUrl": "https://images-eu.ssl-images-amazon.com/images/S/amazon-avatars-global/default._CR0,0,1024,1024_SX460_.png",
        "comment": "The print quality is top notch. Takes at least an hour to self install. Once done everything is breeze.",
        "name": "JHK",
        "starPoint": 4,
        "date": "12 January 2024",
    },

    {
        "imgUrl": "https://images-eu.ssl-images-amazon.com/images/S/amazon-avatars-global/default._CR0,0,1024,1024_SX460_.png",
        "comment": "Good printer 🖨️ with this budget ☺️. But speed in colour is little slow. Overall instead of taking in shop this is 1000000 times better! Saves lakhs of money.",
        "name": "JSW",
        "starPoint": 5,
        "date": "24 October 2023",
    },

    {
        "imgUrl": "https://images-eu.ssl-images-amazon.com/images/S/amazon-avatars-global/default._CR0,0,1024,1024_SX460_.png",
        "comment": "This Brother printer is a superstar. Earlier my experience with other printers was frustrating. But this one is real star.",
        "name": "Avinash",
        "starPoint": 5,
        "date": "16 March 2024",
    },

    {
        "imgUrl": "https://images-eu.ssl-images-amazon.com/images/S/amazon-avatars-global/default._CR0,0,1024,1024_SX460_.png",
        "comment": "Printer is good , but WiFi connectivity to slow",
        "name": "Nikhil",
        "starPoint": 3,
        "date": "14 December 2023",
    },

    {
        "imgUrl": "https://images-eu.ssl-images-amazon.com/images/S/amazon-avatars-global/default._CR0,0,1024,1024_SX460_.png",
        "comment": "This printer works perfectly for home usage. Print quality is good for both mono and color printing.",
        "name": "Loganathan T",
        "starPoint": 5,
        "date": "25 January 2024",
    },
    {
        "imgUrl": "https://images-eu.ssl-images-amazon.com/images/S/amazon-avatars-global/default._CR0,0,1024,1024_SX460_.png",
        "comment": "but some time i face the many problem for connect this printer to wifi. wifi is working good but first use with wifi it have many struggle",
        "name": "Rock Star",
        "starPoint": 4,
        "date": "13 December 2023",
    },
    {
        "imgUrl": "https://images-eu.ssl-images-amazon.com/images/S/amazon-avatars-global/default._CR0,0,1024,1024_SX460_.png",
        "comment": "We've been using it since a couple of months. No issues so far. Works smoothly, overall a good printer.",
        "name": "Leena",
        "starPoint": 4,
        "date": "29 November 2023",
    },
    {
        "imgUrl": "https://images-eu.ssl-images-amazon.com/images/S/amazon-avatars-global/default._CR0,0,1024,1024_SX460_.png",
        "comment": "Highly recommended to have one.",
        "name": "Satheesh Kumar",
        "starPoint": 5,
        "date": "4 March 2024",
    },
]

obj['reviews'] = random.sample(reviews_data, 4)

# print(obj)


# https://www.amazon.in/Brother-DCP-T426W-Wi-Fi-Multifunction-Printer/dp/B0B38NFCCQ/ref=sr_1_17_sspa?crid=B629TTBSAOXK&dib=eyJ2IjoiMSJ9.6w4t-HmMeyH7FZI4dH81cnylxYEht9zvUZ03XV_xiLLGjHj071QN20LucGBJIEps.AQBOZbypl-wGnaTvFiQfktlfoJqpfL8az3NfKtH4fs8&dib_tag=se&keywords=printer&qid=1714675686&sprefix=%2Caps%2C232&sr=8-17-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGZfbmV4dA&th=1