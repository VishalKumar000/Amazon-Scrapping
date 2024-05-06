import requests
from bs4 import BeautifulSoup
import os
import json
import html
import re
import random
import uuid
from colorama import Fore, Back

exchange_rate_usd_to_inr = 83.38

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

data = []
urls = []

with open('printer_product_links.json', 'r') as f:
    urls = json.load(f)


def scrape_page(url, _idx):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        obj = {}

        try:
            # id
            random_uuid = uuid.uuid4()
            obj['id'] = str(random_uuid)
        except Exception as e:
            print(f"Error fetching id: {e}")
            obj['id'] = ''

        try:
            # title
            title = soup.select_one('#productTitle')
            if title:
                title = title.string.strip()
                title = html.unescape(title)
                obj['title'] = title
                obj['description'] = title
            else:
                obj['title'] = ''
                obj['description'] = ''
        except Exception as e:
            print(f"Error fetching title: {e}")
            obj['title'] = ''
            obj['description'] = ''

        try:
            # price
            price = soup.select('span.a-price-whole')
            if price:
                price = price[0].get_text().replace(',', '').replace('.', '')
                price = int(price) / exchange_rate_usd_to_inr
                price = round(price, 2)
                obj['price'] = price
            else:
                obj['price'] = 0.0
        except Exception as e:
            print(f"Error fetching price: {e}")
            obj['price'] = 0.0

        try:
            # image
            images = soup.select_one('.a-dynamic-image.a-stretch-vertical')
            if images: 
                images = [images['src']]
                obj['images'] = images
        except Exception as e:
            print(f"Error fetching images: {e}")
            obj['images'] = []

        try:
            # link
            if title:
                link = title.lower()
                link = link.replace(' ', '-')
                link = re.sub(r'[^a-z0-9-]', '', link)
                link = f"/product-detail/{link}"
                obj['link'] = link
            else:
                obj['link'] = ''
        except Exception as e:
            print(f"Error fetching link: {e}")
            obj['link'] = ''

        try:
            # tag || brand
            tags = soup.select('.a-size-base.po-break-word')
            if tags:
                tags = tags[0]
                tags = tags.get_text()
                tags = [tags.lower()]
                obj['tags'] = tags
            else:
                obj['tags'] = []
        except Exception as e:
            print(f"Error fetching tags: {e}")
            obj['tags'] = []

        try:
            # rating
            rating = soup.select('.a-popover-trigger.a-declarative>span')
            if rating:
                rating = rating[0]
                rating = rating.get_text(strip=True)
                obj['rating'] = rating
            else:
                obj['rating'] = ''
        except Exception as e:
            print(f"Error fetching rating: {e}")
            obj['rating'] = ''

        try:
            # number of review
            numberOfReviews = soup.select('#acrCustomerReviewLink')
            if numberOfReviews:
                numberOfReviews = numberOfReviews[0]
                numberOfReviews = numberOfReviews.get_text()
                numberOfReviews = re.findall(r'\d+', numberOfReviews)
                numberOfReviews = ''.join(numberOfReviews)
                numberOfReviews = int(numberOfReviews)
                obj['numberOfReviews'] = numberOfReviews
            else:
                obj['numberOfReviews'] = 0
        except Exception as e:
            print(f"Error fetching number of reviews: {e}")
            obj['numberOfReviews'] = 0

        try:
            # category
            categories = soup.select(
                '.a-color-secondary.a-size-base.prodDetSectionEntry')
            category = None
            for _category in categories:
                if (_category.get_text(strip=True) == "Generic Name"):
                    category = _category

            if (category):
                category = category.parent
                category = category.select('td')
                category = category[0]
                category = category.get_text(strip=True)

            obj['category'] = category if category else ''
        except Exception as e:
            print(f"Error fetching category: {e}")
            obj['category'] = ''

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
        try:
            featuresArr = soup.select(
                'ul.a-unordered-list.a-vertical.a-spacing-mini > li')

            features = '<ul class="list-disc list-inside leading-7">'
            for idx, feature in enumerate(featuresArr):
                featuresArr[idx] = feature.get_text()
                featuresArr[idx] = html.unescape(featuresArr[idx])
                features += f'<li>{featuresArr[idx]}</li>'

            features += '</ul>'
            obj['features'] = features
        except Exception as e:
            print(f"Error fetching features: {e}")
            obj['features'] = ''

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

        data.append(obj)
        
        print(f'{Fore.GREEN}Response <200> OK {_idx}')
        # print(f'{Fore.WHITE}{Back.GREEN}Response <200> OK {idx}')
        
        with open(os.getcwd() + "/product_data.json", "a") as f:
            json.dump(obj, f)
            f.write(",")

    else:
        # print(f'{Fore.WHITE}{Back.RED}Response <500> ERROR {idx}')
        print(f'{Fore.RED}Response <500> ERROR {_idx}')


for _idx, url in enumerate(urls):
    scrape_page(url, _idx)
    pass

