import cloudscraper
import logging
from bs4 import BeautifulSoup
import re
import time
import fake_useragent
import json
import concurrent.futures
list_cars = []
def fetch_page(url, headers):
    scraper = cloudscraper.create_scraper()
    while True:
        response = scraper.get(url, headers=headers)
        if response.status_code == 200:
            return response
        headers['User-Agent'] = fake_useragent.UserAgent().random
        time.sleep(1)

def time_posted(url):
    match = re.search(r'/(\d{4})/(\d{1,2})/(\d{1,2})/', url)
    if match:
        year, month, day = match.groups()
        month = str(int(month))
        day = str(int(day))
        return f"{day}-{month}-{year}"
    return None

def page_contact(headers, url):
    try:
        response = fetch_page(url, headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        scripts = soup.find_all('script')
        phone_numbers = re.findall(r'\+\d{12}', str(scripts))
        return phone_numbers if phone_numbers else []
    except Exception as e:
        logging.error(f"Error in fetching contact: {e}")
        return []

def process_item(item, headers):
    script = item.find('script', type='application/ld+json')
    if script:
        data = json.loads(script.string)
        url = f'https://uae.yallamotor.com{data["offers"]["url"]}'
        contact = page_contact(headers, url)
        car_data = {
            "url": url,
            "brand": data["brand"]["name"],
            "model": data["model"],
            "color": data["color"],
            "photo": data["image"],
            "price": data["offers"]["price"],
            "kms": data["mileageFromOdometer"]["value"],
            "posted": time_posted(data["image"]),
            "reg_specs": "Local regional specs" if "Local regional specs" in data["description"] else "Non-local",
            "location": item.find('div', class_='p12l p8r').find('div', class_='m4l').text,
            "year": data["modelDate"],
            "contact": contact[0] if contact else None
        }
        print(car_data)
        list_cars.append(car_data)
def process_page(i):
    headers = {'User-Agent': fake_useragent.UserAgent().random}
    link = f"https://uae.yallamotor.com/used-cars/pr_1000_100000/km_100_160000/sl_individual?page={i}&sort=updated_desc"
    response = fetch_page(link, headers)
    print(f"Status code: {response.status_code} for page {i}")
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('div', class_='singleSearchCard m24t p12 bg-w border-gray border8')
    while not items:
        print("Retrying to scrape page..")
        response = fetch_page(link, headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('div', class_='singleSearchCard m24t p12 bg-w border-gray border8')
    for j, item in enumerate(items):
        process_item(item, headers)
        print(f"Processed item {j} on page {i}")

def main():
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_page, range(1, 3))

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time / 60:.2f} minutes")
    print(len(list_cars))
if __name__ == "__main__":
    main()