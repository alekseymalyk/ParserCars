import requests
from bs4 import BeautifulSoup
import concurrent.futures
import random
import time
import openai

# Set up your OpenAI API key
openai.api_key = 'sk-proj-sj4DqwBjGLPrVt6SeZkyT3BlbkFJOhc0eKFKrPgAmTK7gMYN'

base_url = "https://www.zoll-auktion.de/auktion/auktionsuebersicht.php"
params = {
    'n2': '',
    'n1[]': ['1166', '1124', '217', '1161', '216', '215', '1102'],
    'n6': '',
    'n4': '2',
    'n8': '',
    'n7': '',
    'ca': '',
    'c10': '',
    'cf': '',
    'cc': '',
    'cb': '',
    'ce': '',
    'cd': '',
    'c9': '',
    'n0': 'search',
    's': '12',
    't': 't1'
}


def fetch_html(url, params=None, retries=3, timeout=30):
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
        ])
    }
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(2)
    return None


def get_total_pages(soup):
    page_info = soup.find('span', class_='page-link text-dark')
    if page_info:
        total_pages_str = page_info.text.split('/')[1].strip().split()[0]
        return int(total_pages_str)
    return 1


def extract_auction_links(soup):
    auction_links = []
    for item in soup.select('div.kachel_auktion_link.mb-2 a'):
        link = item['href']
        full_link = f"https://www.zoll-auktion.de{link}"
        auction_links.append(full_link)
    return auction_links


def truncate_html(html_content, max_length=15000):
    if len(html_content) > max_length:
        return html_content[:max_length]
    return html_content


def extract_vehicle_data_with_openai(html_content):
    # Truncate HTML content to fit within token limit
    truncated_html_content = truncate_html(html_content)

    # Prompt for OpenAI API
    messages = [
        {"role": "system", "content": "You are an assistant that extracts vehicle information from HTML content."},
        {"role": "user", "content": f"Extract the vehicle information from the following HTML content:\n\n{truncated_html_content}\n\nThe data should be in the following JSON format:\n{{\n    \"brand\": \"\",\n    \"model\": \"\",\n    \"vehicle_type\": \"\",\n    \"first_registration\": \"\",\n    \"mileage\": \"\",\n    \"fuel_type\": \"\",\n    \"drive_type\": \"\",\n    \"transmission\": \"\",\n    \"color\": \"\",\n    \"upholstery_color\": \"\",\n    \"number_of_doors\": \"\",\n    \"description\": \"\"\n}}"}
    ]

    # Use OpenAI's chat completion API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500
    )

    try:
        vehicle_data = eval(response.choices[0].message['content'].strip())
    except (SyntaxError, NameError):
        vehicle_data = {}

    return vehicle_data


first_page_html = fetch_html(base_url, params)
if first_page_html:
    soup = BeautifulSoup(first_page_html, 'html.parser')
    total_pages = get_total_pages(soup)
    print(f"Total pages: {total_pages}")

    all_auction_links = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_html, base_url, {**params, 'pagination': page}) for page in
                   range(1, total_pages + 1)]
        for future in concurrent.futures.as_completed(futures):
            page_html = future.result()
            if page_html:
                soup = BeautifulSoup(page_html, 'html.parser')
                auction_links = extract_auction_links(soup)
                all_auction_links.extend(auction_links)

    print(f"Total auction links found: {len(all_auction_links)}")

    all_auction_data = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_html, link) for link in all_auction_links]
        for future in concurrent.futures.as_completed(futures):
            auction_page_html = future.result()
            if auction_page_html:
                auction_data = extract_vehicle_data_with_openai(auction_page_html)
                if auction_data.get("brand") and auction_data.get("model"):
                    all_auction_data.append(auction_data)
                    print(f"Extracted data: {auction_data}")

    print(f"Total vehicles with data: {len(all_auction_data)}")
    for data in all_auction_data[:5]:
        print(data)
else:
    print("Failed to fetch the first page.")
