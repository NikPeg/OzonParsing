import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from webdriver_manager.chrome import ChromeDriverManager
from random import random
from random import randint
import csv


def hard_to_int(words):
    for word in words.split():
        if word.isdigit():
            return int(word)
    return 0


driver = webdriver.Chrome(ChromeDriverManager().install())
categories_file = open("kazan_categories", "r")
category_index = 0
for category_id in categories_file:
    category_id = category_id.strip()
    file_path = f'kazan/{category_id}.csv'
    try:
        driver.get(
            f"https://kazanexpress.ru/category{category_id}?filters=filter%3DRV-0%3A0~1000%26")
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
            WebDriverWait(driver, 3).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, "tap-noselect")))
            if randint(0, 10) == 0:
                time.sleep(0.5 + random())
            if randint(0, 10) == 0:
                driver.execute_script(f"window.scrollBy(0,{randint(500, 1000)});")
        except Exception as e:
            print(f"Waiting: {e} in {category_id}")
            break
        try:
            for card in driver.find_elements(By.CLASS_NAME, "tap-noselect"):
                card.click()
                WebDriverWait(driver, 3).until(
                    expected_conditions.presence_of_element_located((By.CLASS_NAME, "currency")))
                price = card.find_element(By.CLASS_NAME, "currency").text
                link = driver.current_url
                name = card.find_element(By.CLASS_NAME, "text__product-name").text
                reviews = hard_to_int(card.find_element(By.CLASS_NAME, "text__quantity-of-reviews").text)
                bought = hard_to_int(card.find_element(By.CLASS_NAME, "text__product-orders").text)
                seller = card.find_element(By.CLASS_NAME, "link__product-seller").text
                stock = hard_to_int(card.find_element(By.CLASS_NAME, "text__product-quantity").text)
                if reviews <= 200 and bought <= 2000 and stock <= 3000:
                    csv_writer.writerow([name, price, reviews, bought, stock, seller, link])
                    any_row = True
                driver.execute_script("window.history.go(-1)")
        except Exception as e:
            print(f"Parsing: {e} in {category_id}")
        try:
            item = WebDriverWait(driver, 3).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, "pagination-navigation")))
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
