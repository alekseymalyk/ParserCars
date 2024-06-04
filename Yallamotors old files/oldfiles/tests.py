# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
#
# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# options.add_argument("--disable-blink-features=AutomationControlled")
# driver = webdriver.Chrome(options=options)
# driver.get('https://uae.yallamotor.com/used-cars/pr_1000_100000/km_100_160000/sl_individual?page=1&sort=updated_desc')


import pyautogui
import time
import keyboard
# Задержка, чтобы успеть переключиться на нужное окно
time.sleep(2)

for i in range(1000):
    # Нажать и удерживать клавишу 'command'
    keyboard.write("/start@TopSaverBot")
    keyboard.press('enter')