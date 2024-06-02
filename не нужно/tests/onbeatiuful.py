import requests
from bs4 import BeautifulSoup
import fake_useragent
link = "https://uae.yallamotor.com/used-cars/pr_1000_100000/km_100_160000/sl_individual?sort=updated_desc"
headers = {
        'User-Agent': fake_useragent.UserAgent().random
    }

response = requests.get(link, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
items = soup.find_all('a', class_ = 'ym_lazy lazy_used_car_search')
href_list = []

# Проходим по всем элементам 'a' с классом 'ym_lazy lazy_used_car_search'
for item in items:
    # Извлекаем значение атрибута href и добавляем его в список
    href = item.get('href')
    href_list.append(f'https://uae.yallamotor.com{href}')
    print(f'https://uae.yallamotor.com{href}')
print(href_list)


# comps = []
# for item in items:
#     comps.append({
#         'title': item.find('span', class_ = 'goods-tile__title').get_text(strip=True),
#         'price': item.find('span', class_ = 'goods-tile__price-value').get_text(strip=True),
#         'link': item.find('a', class_ = 'goods-tile__heading ng-star-inserted'). get('href')
#     })
#     for comp in comps:
#         print(f"{comp['title']} по цене -> {comp['price']}, ссылка -> {comp['link']}\n")
# for i in range(1, len(comps)+1):
#     pass
# print(i)