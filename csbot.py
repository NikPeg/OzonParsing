from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from pynput import keyboard
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time


def on_press(key):
    pass


def on_release(key):
    global last_released
    try:
        if key.value.vk == 120: #key.vk == 87 and last_released == 9:
            # Stop listener
            return False
        last_released = key.value.vk
    except:
        pass
    try:
        last_released = key.value.vk
    except:
        pass

# element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "myDynamicElement")))
try:
    print("В открывшемся окне войдите в свой аккаунт.\nЗатем выберите нужные параметры и нажмите f9.\nБот будет покупать скины сразу после их появления.\nНе меняйте размер окна.\nДа пребудет с Вами сила.\n")
    driver = webdriver.Chrome()
    driver.get("https://steamcommunity.com/openid/login?openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.return_to=https%3A%2F%2Fcsgo.trade%2Fafter_auth_new&openid.realm=https%3A%2F%2Fcsgo.trade%2F")
    last_released = None
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    # print("OKEY")
    derived = False
except:
    pass
    # print("Что-то пошло не так1.")
while True:
    i = 0
    try:
        try:
            refresh = WebDriverWait(driver, 1).until(
                expected_conditions.presence_of_element_located((By.ID, "refresh_bot_inventory")))
            refresh.click()
            # print("обновляюсь...")
        except:
            pass
        while True:
            i += 1
            try:
                try:
                    theme = WebDriverWait(driver, 1).until(
                        expected_conditions.presence_of_element_located((By.ID, "header-numb")))
                    theme.click()
                except:
                    pass
                while len(driver.find_elements_by_xpath("//*[@id='offer_inventory_bot']/*")) > 0:
                    try:
                        selected = WebDriverWait(driver, 1).until(
                            expected_conditions.presence_of_element_located(
                                (By.XPATH, "//*[@id='offer_inventory_bot']/*[1]")))
                        selected.click()
                    except:
                        pass
                # print("Clicked1")
                while len(driver.find_elements_by_xpath("//*[@id='offer_inventory_bot']/*")) == 0:
                    item = WebDriverWait(driver, 10).until(
                        expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='inventory_bot']/*[{0}]".format(i))))
                    item.click()
                # print("ITEM")
                trade = WebDriverWait(driver, 1).until(
                    expected_conditions.presence_of_element_located((By.ID, "trade-btn")))
                trade.click()
                # print("Clicked")
                time.sleep(2)
            except: # (exceptions.NoSuchElementException, exceptions.TimeoutException):
                # print("NSEE")
                break
            while True:
                try:
                    close = WebDriverWait(driver, 2).until(
                        expected_conditions.presence_of_element_located((By.XPATH, "//div[@id='trade-popup']/a[1]")))
                    close.click()
                except:
                    break
            # print(i)
    except:
        pass
        # print("Что-то пошло не так2.")
driver.close()