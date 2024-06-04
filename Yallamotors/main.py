import aiohttp
import asyncio
import logging
import ssl
import certifi
import random
import re
import json
from bs4 import BeautifulSoup
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_retries = 1000
max_concurrent_requests = 1
car_list = []
current_web_links = [f"https://uae.yallamotor.com/used-cars/pr_1000_100000/km_100_160000/sl_individual?page={i}&sort=updated_desc" for i in range(1, 501)]

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
]

def time_posted(word):
    date_regex = r'/(\d{4})/(\d{1,2})/(\d{1,2})/'
    match = re.search(date_regex, word)
    if match:
        year, month, day = match.groups()
        return f"{year}-{int(month):02d}-{int(day):02d}"
    else:
        return None
async def fetch_page(session, url, retries=0):
    headers = {'User-Agent': random.choice(user_agents)}
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.text()
                logger.info(f"Fetched page {url} with status {response.status}")
                return data
            else:
                logger.error(f"Error fetching page {url}: {response.status}")
                if retries < max_retries:
                    logger.info(f"Retrying page {url} ({retries + 1}/{max_retries})")
                    await asyncio.sleep(1)  # небольшая пауза перед повторной попыткой
                    return await fetch_page(session, url, retries + 1)
                else:
                    logger.error(f"Max retries exceeded for page {url}")
                    return None
    except aiohttp.ClientError as e:
        logger.error(f"Client error on page {url}: {e}")
        if retries < max_retries:
            logger.info(f"Retrying page {url} ({retries + 1}/{max_retries})")
            await asyncio.sleep(1)  # небольшая пауза перед повторной попыткой
            return await fetch_page(session, url, retries + 1)
        else:
            logger.error(f"Max retries exceeded for page {url}")
            return None

async def page_contact(session, url):
    headers = {'User-Agent': random.choice(user_agents)}
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                scripts = soup.find_all('script')
                for script in scripts:
                    script_str = str(script)
                    phone_numbers = re.findall(r'\+\d{12}', script_str)
                    if phone_numbers:
                        return phone_numbers
            else:
                logger.error(f"Error fetching contact page {url}: {response.status}")
    except aiohttp.ClientError as e:
        logger.error(f"Client error on contact page {url}: {e}")
    return []

async def process_page(session, link, retries=0):
    data = await fetch_page(session, link)
    if data:
        soup = BeautifulSoup(data, 'html.parser')
        items = soup.find_all('div', class_='singleSearchCard m24t p12 bg-w border-gray border8')
        initial_car_count = len(car_list)
        for item in items:
            scripts = item.find_all('script', type='application/ld+json')
            item_locations = item.find_all('div', class_='p12l p8r')
            for script, item_location in zip(scripts, item_locations):
                item_location_text = item_location.find_all('div', class_='m4l')
                location = item_location_text[0].text.strip()
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
                    "posted": time_posted(data["image"]),
                    "reg_specs": "Local regional specs" if "Local regional specs" in data["description"] else "Non-local",
                    "location": location,
                    "year": data["modelDate"],
                    # "contact": await page_contact(session, f'https://uae.yallamotor.com{data["offers"]["url"]}')
                }

                logger.info(f"Car data: {car_data}")
                car_list.append(car_data)

        if len(car_list) == initial_car_count and retries < max_retries:
            logger.info(f"No cars found on {link}, retrying ({retries + 1}/{max_retries})")
            await process_page(session, link, retries + 1)

async def main():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = aiohttp.TCPConnector(limit=max_concurrent_requests, ssl=ssl_context)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [process_page(session, url) for url in current_web_links]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time/60} minutes")
    print(f"Total number of cars: {len(car_list)}")
