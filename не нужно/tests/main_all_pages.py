import requests
from bs4 import BeautifulSoup
import fake_useragent
import json

for i in range(1, 501):     #From first to last page
    check_lists = []

    link = f"https://uae.yallamotor.com/used-cars/pr_1000_100000/km_100_160000/sl_individual?page={i}&sort=updated_desc"
    while len(check_lists) <= 0:
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
                    #Func location
                    item_location_text = item_location.find_all('div', class_='m4l')
                    location = item_location_text[0].text
                    check_lists.append(location)

                    #Func json processing
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

                    #Check for epmty list. If epmty -> restart func to restart proccessing site.
                    if len(check_lists) == 0:
                        pass
                    else:
                        print(car_data)