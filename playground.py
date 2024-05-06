import os
import json

data = []
with open('printer_product_links.json', 'r') as f:
    data = json.load(f)

    

print(data[0])