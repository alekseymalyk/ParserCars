from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

link = "https://uae.yallamotor.com/used-cars/pr_1000_100000/km_100_160000/sl_individual?sort=updated_desc"

# Инициализация драйвера Chrome
driver = webdriver.Chrome()

# Загрузка страницы
driver.get(link)

try:


finally:
    # Закрываем браузер после выполнения
    driver.quit()
