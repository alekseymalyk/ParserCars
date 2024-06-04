# https://uae.yallamotor.com/used-cars/pr_1000_100000/km_100_160000/sl_individual?page=1&sort=updated_desc
#3376
import logging
from bs4 import BeautifulSoup
import requests
import re
import time
import fake_useragent
import json
import concurrent.futures
def time_posted(url):
    match = re.search(r'/(\d{4})/(\d{1,2})/(\d{1,2})/', url)
    if match:
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)

        month = str(int(month))
        day = str(int(day))

        return f"{day}-{month}-{year}"
    return None

# def page_contact(headers, url):
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, 'html.parser')
#         scripts = soup.find_all('script')
#         phone_numbers = []
#         for script in scripts:
#             phone_numbers.extend(re.findall(r'\+\d{12}', str(script)))
#         return phone_numbers
#     except Exception as e:
#         logging.error(f"Error in fetching contact: {e}")
#         return []

def process_page(link, output_file):
    try:
        headers = {'User-Agent': fake_useragent.UserAgent().random}
        response = requests.get(link, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', class_='singleSearchCard m24t p12 bg-w border-gray border8')
        for item in items:
            scripts = item.find_all('script', type='application/ld+json')
            item_locations = item.find_all('div', class_='p12l p8r')


            for script, item_location in zip(scripts, item_locations):
                item_location_text = item_location.find_all('div', class_='m4l')
                location = item_location_text[0].text
                data = json.loads(script.string)
                car_data = {
                    "url": f'https://uae.yallamotor.com{data["offers"]["url"]}',
                    "brand": data["brand"]["name"],
                    "model": data["model"],
                    "color": data["color"],
                    "photo": data["image"],
                    "price": data["offers"]["price"],
                    "kms": data["mileageFromOdometer"]["value"],
                    "posted": time_posted(data["image"]),
                    "reg_specs": "Local regional specs" if "Local regional specs" in data["description"] else "Non-local",
                    "location": location,
                    "year": data["modelDate"]
                    # "contact": page_contact(headers, f'https://uae.yallamotor.com{data["offers"]["url"]}')[0]
                }
                output_file.write(json.dumps(car_data) + '\n')
                print(car_data)
                time.sleep(0.5)

    except Exception as e:
        logging.error(f"Error in processing page {link}: {e}")

current_web_links = [f"https://uae.yallamotor.com/used-cars/pr_1000_100000/km_100_160000/sl_individual?page={i}&sort=updated_desc" for i in range(1, 501)]

start_time = time.time()

with open('gptmain.json', 'w') as output_file:
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        res = executor.map(lambda link: process_page(link, output_file), current_web_links)

end_time = time.time()
execution_time = end_time - start_time
print(f"Total execution time: {execution_time/60} minutes")
