import requests
from bs4 import BeautifulSoup
import fake_useragent
import json
import concurrent.futures
import time_main

def process_page(link):
    check_lists = []

    while len(check_lists) <= 0:
        headers = {'User-Agent': fake_useragent.UserAgent().random}
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', class_='singleSearchCard m24t p12 bg-w border-gray border8')

        for item in items:
            scripts = item.find_all('script', type='application/ld+json')
            item_locations = item.find_all('div', class_='p12l p8r')

            for script, item_location in zip(scripts, item_locations):
                item_location_text = item_location.find_all('div', class_='m4l')
                location = item_location_text[0].text
                check_lists.append(location)

                json_ld_script = script.string
                start_index = json_ld_script.find('{')
                end_index = json_ld_script.rfind('}')
                json_str = json_ld_script[start_index:end_index+1]
                data = json.loads(json_str)

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

# List to hold URLs for processing
current_web_links = [f"https://uae.yallamotor.com/used-cars/pr_1000_100000/km_100_160000/sl_individual?page={i}&sort=updated_desc" for i in range(1, 501)]

start_time = time.time()

# Use ThreadPoolExecutor for concurrent processing
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    res = executor.map(
        process_page,
        current_web_links,
    )

end_time = time.time()
execution_time = end_time - start_time
print(f"Total execution time: {execution_time/60} minutes")
