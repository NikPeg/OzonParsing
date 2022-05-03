import os

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
categories_file = open("categories", "r")
category_index = 0
for category_id in categories_file:
    category_id = category_id.strip()
    file_path = f'ozon/{category_id}.csv'
    try:
        driver.get(
            f"https://www.ozon.ru/category/{category_id}/?price=0.000%3B1000.000&reviews_count=0.000%3B200.000")
    except Exception as e:
        print(f"Web-page opening: {e} in {category_id}")
        continue
    any_row = False
    try:
        if os.path.exists(file_path):
            continue
        csv_file = open(file_path, 'w', newline='', encoding='utf-8')
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    except Exception as e:
        print(f"File opening: {e} in {category_id}")
        continue
    while True:
        try:
            WebDriverWait(driver, 3).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "y5s")))
            if randint(0, 10) == 0:
                time.sleep(0.5 + random())
            if randint(0, 10) == 0:
                driver.execute_script(f"window.scrollBy(0,{randint(500, 1000)});")
        except Exception as e:
            print(f"Waiting: {e} in {category_id}")
            break
        try:
            for card in driver.find_elements(By.CLASS_NAME, "i3p"):
                price = card.find_element(By.CLASS_NAME, "ui-s2").find_element(By.CLASS_NAME, "ui-s5").text
                link = card.find_element(By.CLASS_NAME, "tile-hover-target").get_attribute("href")
                name = card.find_element(By.CLASS_NAME, "tile-hover-target").find_element(By.CLASS_NAME, "de0").text
                reviews = card.find_element(By.CLASS_NAME, "ni6").find_element(By.TAG_NAME, "a").text
                csv_writer.writerow([name, str(price), reviews, link])
                any_row = True
            for card in driver.find_elements(By.CLASS_NAME, "p3i"):
                price = card.find_element(By.CLASS_NAME, "p4i").find_element(By.CLASS_NAME, "ui-s5").text
                link = card.find_element(By.CLASS_NAME, "tile-hover-target").get_attribute("href")
                reviews = card.find_element(By.CLASS_NAME, "yc5").text
                name = card.find_element(By.CLASS_NAME, "pi4").find_element(By.CLASS_NAME, "i5p").find_element(
                    By.CLASS_NAME, "tile-hover-target").find_element(By.CLASS_NAME, "de0").text
                csv_writer.writerow([name, str(price), reviews, link])
                any_row = True
        except Exception as e:
            print(f"Parsing: {e} in {category_id}")
        try:
            item = WebDriverWait(driver, 3).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, "sy2")))
            item.click()
        except TimeoutException as e:
            break
        except Exception as e:
            print(f"Next button: {e} in {category_id}")
            break
    try:
        csv_file.close()
        if not any_row:
            os.remove(file_path)
    except Exception as e:
        print(f"Can't close file: {e} in {category_id}")
    print(f"Category {category_index} done!")
    category_index += 1
print("Success!")
