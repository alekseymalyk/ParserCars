import requests
from bs4 import BeautifulSoup
import fake_useragent
import json
link = "https://uae.yallamotor.com/used-cars/pr_1000_100000/km_100_160000/sl_individual?sort=updated_desc"
headers = {
        'User-Agent': fake_useragent.UserAgent().random
    }

response = requests.get(link, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

items = soup.find_all('div', class_='singleSearchCard m24t p12 bg-w border-gray border8')
for item in items:
    scripts = item.find_all('script', type='application/ld+json')
    item_locations = item.find_all('div', class_='p12l p8r')
    for script in scripts:
        for item_location in item_locations:
            item_location_text = item_location.find_all('div', class_='m4l')
            location = item_location_text[0].text

            json_ld_script = script.string
            start_index = json_ld_script.find('{')
            end_index = json_ld_script.rfind('}')
            json_str = json_ld_script[start_index:end_index+1]
            data = json.loads(json_str)
            # print(json.dumps(data, indent=2))
            car_data = {
                "url": f'https://uae.yallamotor.com{data["offers"]["url"]}',
                "brand": data["brand"]["name"],
                "model": data["model"],
                "color": data["color"],
                "photo": data["image"],
                "price": data["offers"]["price"],
                "kms": data["mileageFromOdometer"]["value"],
                "posted": "",
                "reg_specs": "Local regional specs" if "Local regional specs" in data["description"] else "Non-local",
                "location": location,
                "year": data["modelDate"],
                "contact": ""
            }

        print(car_data)