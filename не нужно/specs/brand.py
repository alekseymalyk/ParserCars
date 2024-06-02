import requests
from bs4 import BeautifulSoup
import fake_useragent
from url import url
link = "https://uae.yallamotor.com/used-cars/pr_1000_100000/km_100_160000/sl_individual?sort=updated_desc"
headers = {
        'User-Agent': fake_useragent.UserAgent().random
    }

response = requests.get(link, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

