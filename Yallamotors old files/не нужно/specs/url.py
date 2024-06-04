import requests
from bs4 import BeautifulSoup
import fake_useragent

def url():
    href_list = []
    for i in range(1, 501):
        href_lists = []

        link = f"https://uae.yallamotor.com/used-cars/pr_1000_100000/km_100_160000/sl_individual?page={i}&sort=updated_desc"
        while len(href_lists) <= 0:
            #Start function
            headers = {
                'User-Agent': fake_useragent.UserAgent().random
            }
            response = requests.get(link, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            items = soup.find_all('div', class_='rightbuttons')
            print()
    #         href_list = []
    #
            for item in items:
                canvas_element = item.find('canvas')
                print(canvas_element)
    #         if len(href_lists) == 0:
    #             pass
    #         else:
    #             print(href_lists)
    # return href_list


if __name__ == '__main__':
    url()