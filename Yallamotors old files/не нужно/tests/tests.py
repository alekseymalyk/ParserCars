# # import requests
# # from bs4 import BeautifulSoup
# # import fake_useragent
# # import json
# # link = "https://uae.yallamotor.com/used-cars/pr_1000_100000/km_100_160000/sl_individual?sort=updated_desc"
# # headers = {
# #         'User-Agent': fake_useragent.UserAgent().random
# #     }
# #
# # response = requests.get(link, headers=headers)
# # soup = BeautifulSoup(response.content, 'html.parser')
# # items = soup.find_all('div', class_='singleSearchCard m24t p12 bg-w border-gray border8')
# #
# # for item in items:
# #     item_divs = item.find_all('div', class_='p12l p8r')
# #     for item_div in item_divs:
# #         item_div_pluses = item_div.find_all('div', class_='m4l')
# #         print(item_div_pluses[0].text)
# #         # for item_div_pluse in item_div_pluses:
# #         #     text_div = item_div_pluse.find_all("div", class_= "m4l")
# #         #     print(text_div)
# #
# #
# #     # scripts = item.find_all('script', type='application/ld+json')
# #     # locations = item.find_all('div', class_='m4l')
# #     # print(locations)
#
#
# import concurrent.futures
#
# with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#             res = executor.map(
#                 self.get_car_dict_from_url,
#                 current_web_links,
# import requests
# from fake_useragent import UserAgent
# import json
# from bs4 import BeautifulSoup
# import re
#
# # Создание случайного юзер-агента
# ua = UserAgent()
#
# # URL сайта, на который вы хотите отправить запрос
# url = "https://uae.yallamotor.com/used-cars/nissan/x-trail/2020/used-nissan-x-trail-2020-dubai-1599460"
# # Подготовка заголовков запроса с использованием случайного юзер-агента
# headers = {
#     "User-Agent": ua.random,
#     "Content-Type": "application/json"
# }
#
# # Данные запроса в формате JSON
#
#
# # Отправка POST-запроса на сайт
# response = requests.post(url, headers=headers)
# print(response)
#
# # Проверка успешности запроса
# if response.status_code == 200:
#     html_code = response.text
#     soup = BeautifulSoup(html_code, 'html.parser')
#     print(soup.prettify())
#     # phone_number = re.search(r'\+\d{12}', script_text).group()
#
#     print("Seller Phone Number:")
#
# else:
#     print("Ошибка при отправке запроса:", response.status_code)

# from bs4 import BeautifulSoup
# import requests
#
# url = "https://uae.yallamotor.com//used-cars/nissan/x-trail/2020/used-nissan-x-trail-2020-dubai-1599460"
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')
#
# sellerPhone = soup.find('div', {'class': 'contact-seller-info'})
#
# vehicleUrl = url
#
# print(f"Seller Phone: {sellerPhone}")
# print(f"Vehicle Url: {vehicleUrl}")

# import re
#
script = """
<script>
   $(document).on('turbolinks:load',function() {
      $('.iframe-cappasity').remove();
      $('.iframe-cappasity-lightbox').remove();
  });

  $(document).on('turbolinks:load',function() {
        dataLayer.push({'vehicleId': '1599460','vehicleUrl': 'https://uae.yallamotor.com//used-cars/nissan/x-trail/2020/used-nissan-x-trail-2020-dubai-1599460', 'vehicleName': "Used Nissan X-Trail  2.5 SL 4WD (7-Seater) 2020", 'sellerPhone': "+971502795640", 'city': "Dubai", 'sellerEmail': "mohammad_abusad@yahoo.com", 'sellerLastName': "" , 'sellerFirstName':"", 'vehicleBrand': 'Nissan', 'vehiclePrice': '82500'})
  });
</script>
"""
#
# # Используем регулярное выражение для поиска номера телефона
# phone_numbers = re.findall(r'\+\d{12}', script)
#
# if phone_numbers:
#     print("Найдены номера телефонов:")
#     for phone_number in phone_numbers:
#         print(phone_number)
# else:
#     print("Номера телефонов не найдены.")

# import re
# from bs4 import BeautifulSoup
# from selenium import webdriver
#
# driver = webdriver.Chrome()
#
# driver.get("https://uae.yallamotor.com//used-cars/nissan/x-trail/2020/used-nissan-x-trail-2020-dubai-1599460")
# html_code = driver.page_source
# driver.quit()
# soup = BeautifulSoup(html_code, 'html.parser')
# scripts = soup.find_all('script')
# count = 0
# for i in range(len(scripts)):
#     script = str(scripts[count])
#     count += 1
#     phone_numbers = re.findall(r'\+\d{12}', script)
#
#     if phone_numbers:
#         print(phone_numbers[0])
#         break
#     else:
#         pass

# import re
# from bs4 import BeautifulSoup
# import requests
# url = "https://uae.yallamotor.com//used-cars/nissan/x-trail/2020/used-nissan-x-trail-2020-dubai-1599460"
# response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
# soup = BeautifulSoup(response.text, 'html.parser')
# scripts = soup.find_all('script')
# count = 0
# for i in range(len(scripts)):
#     script = str(scripts[count])
#     count += 1
#     phone_numbers = re.findall(r'\+\d{12}', script)
#
#     if phone_numbers:
#         print(phone_numbers[0])
#         break
#     else:
#         pass

import re

# URL изображения
url = "https://ymimg1.b8cdn.com/resized/used_car/2023/10/25/1522412/pictures/11089329/slide_show_Mercedes-Benz_C-Class_2017_in_Dubai_1522412_5.jpg"

# Регулярное выражение для поиска даты в URL
date_regex = r'/(\d{4})/(\d{2})/(\d{2})/'

# Поиск даты в URL
match = re.search(date_regex, url)

if match:
    # Извлечение года, месяца и дня из совпадения
    year = match.group(1)
    month = match.group(2)
    day = match.group(3)

    # Форматирование даты в нужный вид
    formatted_date = f"{year}-{month}-{day}"

    # Вывод результата
    print("Дата в URL:", match.group(0))
    print("Дата после преобразования:", formatted_date)
else:
    print("Дата не найдена в URL")
