import requests
from bs4 import BeautifulSoup

# URL страницы с автомобилем
url = "https://www.zoll-auktion.de/auktion/produkt/1_VW_Transporter_T5_Pritsche_Doppelkabine/851370"

# Выполнение запроса к странице
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")


# Функция для извлечения данных
def extract_vehicle_data(soup):
    data = {}
    data["Ссылка"] = url

    # Функция для безопасного извлечения данных
    def safe_find(text):
        element = soup.find("span", string=text)
        return element.find_next("span").text.strip() if element else "Не найдено"

    data["Бренд"] = safe_find("Hersteller:")
    data["Модель"] = safe_find("Modell:")
    data["Тип транспортного средства"] = safe_find("Fahrzeugart:")
    data["Первая регистрация"] = safe_find("Erstzulassung:")
    data["Пробег"] = safe_find("Kilometerstand:")
    data["Тип топлива"] = safe_find("Kraftstoffart:")
    data["Тип привода"] = safe_find("Antriebsart:")
    data["Трансмиссия"] = safe_find("Getriebe:")
    data["Цвет"] = safe_find("Farbe:")
    data["Обивка/цвет"] = safe_find("Polsterfarbe:")
    data["Количество дверей"] = safe_find("Anzahl Türen:")

    return data


# Извлечение данных
vehicle_data = extract_vehicle_data(soup)

# Вывод данных
for key, value in vehicle_data.items():
    print(f"{key}: {value}")
