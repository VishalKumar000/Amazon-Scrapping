import os
import json

with open('printer_product_links.json', 'r') as f:
    data = json.load(f)
    print(data[0])
