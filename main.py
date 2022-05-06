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

driver = webdriver.Chrome(ChromeDriverManager().install())
categories_file = open("ozon_categories", "r")
category_index = 0
for category_id in categories_file:
    print(f"Category {category_index} done!")
    category_index += 1
    category_id = category_id.strip()
    file_path = f'ozon/{category_id}.csv'
    try:
        if os.path.exists(file_path):
            continue
        csv_file = open(file_path, 'w', newline='', encoding='utf-8')
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    except Exception as e:
        print(f"File opening: {e} in {category_id}")
        continue
    try:
        driver.get(
            f"https://www.ozon.ru/category/{category_id}/?price=0.000%3B1000.000&reviews_count=0.000%3B200.000")
    except Exception as e:
        print(f"Web-page opening: {e} in {category_id}")
        continue
    any_row = False
    page_index = 1
    while True:
        try:
            WebDriverWait(driver, 1).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "ui-n7")))
            # if randint(0, 10) == 0:
            #     time.sleep(0.5 + random())
            # if randint(0, 10) == 0:
            #     driver.execute_script(f"window.scrollBy(0,{randint(500, 1000)});")
        except TimeoutException as e:
            # nothing fount
            break
        except Exception as e:
            print(f"Waiting: {e} in {category_id}")
            break
        try:
            for card in driver.find_elements(By.CLASS_NAME, "i3p"):
                price = card.find_element(By.CLASS_NAME, "ui-s5").text
                link = card.find_element(By.CLASS_NAME, "tile-hover-target").get_attribute("href")
                name = card.find_element(By.CLASS_NAME, "tile-hover-target").find_element(By.CLASS_NAME, "de0").text
                try:
                    reviews = card.find_element(By.CLASS_NAME, "ni6").find_element(By.TAG_NAME, "a").text
                except Exception as e:
                    reviews = 0
                try:
                    seller = card.find_element(By.CLASS_NAME, "io8").find_element(By.CLASS_NAME, "de0").find_element(
                        By.TAG_NAME, "span").text
                except Exception as e:
                    seller = "null"
                csv_writer.writerow([name, str(price), reviews, seller, link])
                any_row = True
        except Exception as e:
            try:
                for card in driver.find_elements(By.CLASS_NAME, "iq6"):
                    price = card.find_element(By.CLASS_NAME, "ui-s5").text
                    link = card.find_element(By.CLASS_NAME, "tile-hover-target").get_attribute("href")
                    try:
                        reviews = card.find_element(By.CLASS_NAME, "yc5").text
                    except Exception as e:
                        reviews = 0
                    name = card.find_element(By.CLASS_NAME, "i7q").find_element(By.CLASS_NAME, "tile-hover-target").find_element(By.TAG_NAME, "span").text
                    try:
                        seller = \
                            card.find_element(By.CLASS_NAME, "i7q").find_element(By.CLASS_NAME, "qi0").find_element(By.CLASS_NAME, "de0").find_elements(
                                By.TAG_NAME, "span")[-1].text
                    except Exception as e:
                        seller = "null"
                    csv_writer.writerow([name, str(price), reviews, seller, link])
                    any_row = True
            except Exception as e:
                print(f"Parsing: {e} in {category_id}")
                break
        try:
            for card in driver.find_elements(By.CLASS_NAME, "p3i"):
                price = card.find_element(By.CLASS_NAME, "ui-s5").text
                link = card.find_element(By.CLASS_NAME, "tile-hover-target").get_attribute("href")
                try:
                    reviews = card.find_element(By.CLASS_NAME, "yc5").text
                except Exception as e:
                    reviews = 0
                name = card.find_element(By.CLASS_NAME, "pi4").find_element(By.CLASS_NAME, "i5p").find_element(
                    By.CLASS_NAME, "tile-hover-target").find_element(By.CLASS_NAME, "de0").text
                try:
                    seller = \
                        card.find_element(By.CLASS_NAME, "io8").find_element(By.CLASS_NAME, "de0").find_elements(
                            By.TAG_NAME,
                            "span")[
                            -1].text
                except Exception as e:
                    seller = "null"
                csv_writer.writerow([name, str(price), reviews, seller, link])
                any_row = True
        except Exception as e:
            print(f"Parsing: {e} in {category_id}")
            break
        try:
            page_index += 1
            driver.get(
                f"https://www.ozon.ru/category/{category_id}/?page={page_index}&price=0.000%3B1000.000&reviews_count=0.000%3B200.000")
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
print("Success!")
