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
categories_file = open("wb_categories", "r")
category_index = 0
for category_id in categories_file:
    category_id = category_id.strip()
    file_path = f'wb/{category_id.replace("/", "_")}.csv'
    try:
        driver.get(
            f"https://www.wildberries.ru/catalog/{category_id}/?priceU=0%3B100000")
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
                expected_conditions.presence_of_element_located((By.CLASS_NAME, "product-card__wrapper")))
            if randint(0, 10) == 0:
                time.sleep(0.5 + random())
            if randint(0, 10) == 0:
                driver.execute_script(f"window.scrollBy(0,{randint(500, 1000)});")
        except Exception as e:
            print(f"Waiting: {e} in {category_id}")
            break
        try:
            for card in driver.find_elements(By.CLASS_NAME, "product-card__wrapper"):
                card.click()
                WebDriverWait(driver, 3).until(
                    expected_conditions.presence_of_element_located((By.CLASS_NAME, "price-block__final-price")))
                price = card.find_element(By.CLASS_NAME, "price-block__final-price").text
                link = driver.current_url
                name = card.find_element(By.CLASS_NAME, "same-part-kt__header").text
                reviews = hard_to_int(card.find_element(By.CLASS_NAME, "same-part-kt__count-review").text)
                bought = hard_to_int(card.find_element(By.CLASS_NAME, "same-part-kt__order-quantity").text)
                seller = card.find_element(By.CLASS_NAME, "seller-details__title-wrap").find_element(By.TAG_NAME,
                                                                                                     "a").text
                if reviews <= 200 and bought <= 2000:
                    csv_writer.writerow([name, price, reviews, bought, seller, link])
                    any_row = True
                driver.execute_script("window.history.go(-1)")
        except Exception as e:
            print(f"Parsing: {e} in {category_id}")
        try:
            item = WebDriverWait(driver, 3).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, "pagination-next")))
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
