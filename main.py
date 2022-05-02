from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from pynput import keyboard
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from webdriver_manager.chrome import ChromeDriverManager
from random import random
from random import randint
import csv

driver = webdriver.Chrome(ChromeDriverManager().install())
category_id = "posuda-dlya-prigotovleniya-19005"
driver.get(
    f"https://www.ozon.ru/category/{category_id}/?price=79.000%3B1000.000&reviews_count=1.000%3B200.000")
WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "sy2")))
time.sleep(1 + random())
csv_file = open('ozon.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
while True:
    try:
        for card in driver.find_elements(By.CLASS_NAME, "i3p"):
            price = card.find_element(By.CLASS_NAME, "ui-s2").find_element(By.CLASS_NAME, "ui-s5").text
            link = card.find_element(By.CLASS_NAME, "tile-hover-target").get_attribute("href")
            name = card.find_element(By.CLASS_NAME, "tile-hover-target").find_element(By.CLASS_NAME, "de0").text
            reviews = card.find_element(By.CLASS_NAME, "ni6").find_element(By.TAG_NAME, "a").text
            csv_writer.writerow([name, str(price), reviews, link])
        item = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "sy2")))
        item.click()
        WebDriverWait(driver, 3).until(
            expected_conditions.presence_of_element_located((By.ID, "layoutPage")))
        time.sleep(1 + random())
        if randint(0, 10) == 0:
            driver.execute_script(f"window.scrollBy(0,{randint(500, 1000)});")
    except TimeoutException as e:
        break
csv_file.close()
