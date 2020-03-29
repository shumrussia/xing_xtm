from collections import OrderedDict
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

# Initialize the driver, visit the main page
driver = webdriver.Firefox()
driver.get("https://www.xing.com/xtm/search")

time.sleep(random.uniform(0.5, 1.5))
el_username = driver.find_element_by_xpath("//input[@id='login_form_username']")
el_password = driver.find_element_by_xpath("//input[@id='login_form_password']")
el_submit = driver.find_element_by_xpath("//input[@type='submit']")

time.sleep(random.uniform(1.2, 2.4))
el_username.send_keys("brhohmann")
time.sleep(random.uniform(1.3, 2.5))
el_password.send_keys("victoria20")
time.sleep(random.uniform(0.7, 1.8))
el_submit.click()

def parse_page(path_to_file):
    iter_collected_data = OrderedDict({
    "Firma": [],
    "Ort": [],
    "Vorname": [],
    "Nachname": [],
    "Original-Positionsbezelchnung": [],
    "Xing": []
                } )
    no_of_cards = len(driver.find_elements_by_xpath("//section[contains(@id, 'candidate')]")) + 1
    for i in range(1, no_of_cards):
        iter_el_card = driver.find_element_by_xpath("//section[contains(@id, 'candidate')][{}]".format(str(i)))
        iter_el_info = iter_el_card.find_element_by_xpath(".//div[contains(@class, 'h-info')]")
        iter_el_title = iter_el_info.find_element_by_xpath(".//div[contains(@class, 'nameContainer')][1]")
        iter_el_link = iter_el_title.find_element_by_xpath(".//a[1]")
        iter_text_title = iter_el_link.text.split()
        iter_text_surname = iter_text_title.pop()
        iter_text_name = " ".join(iter_text_title,)
        iter_text_link = iter_el_link.get_attribute('href')
        try:
            iter_el_position = iter_el_info.find_element_by_xpath(".//div[2]/div[1]")
            iter_text_position = iter_el_position.text
        except NoSuchElementException:
            iter_text_position = "not specified"
        try: 
            iter_el_company = iter_el_info.find_element_by_xpath(".//div[3]/div[1]")
            iter_text_company = iter_el_company.text
        except NoSuchElementException:
            iter_text_company = "not specified"
        try:
            iter_el_address = iter_el_info.find_element_by_xpath(".//div[3]/div[2]")
            iter_list_address = iter_el_address.text.split(",", 1)
            iter_text_city = iter_list_address[0]
        except NoSuchElementException:
            iter_text_city = "not specified"
        with open(path_to_file, "a+") as fo:
            fo.write("{};".format(iter_text_name.encode('utf-8')))
            fo.write("{};".format(iter_text_surname.encode('utf-8')))
            fo.write("{};".format(iter_text_position.encode('utf-8')))
            fo.write("{};".format(iter_text_company.encode('utf-8')))
            fo.write("{};".format(iter_text_link.encode('utf-8')))
            fo.write("{};".format(iter_text_city.encode('utf-8')))
            fo.write("\n")
            fo.close()

def scroll_page():
    el_pagination = driver.find_element_by_xpath("//ol[contains(@class, 'pagination')]")
    el_scroll = el_pagination.find_elements_by_xpath(".//li")[-1]
    el_scroll.click()
    time.sleep(random.uniform(3.2, 4.5))

try:
    el_popup = driver.find_element_by_xpath("//div[contains(@class, 'dialog ui-draggable')]")
    time.sleep(random.uniform(0.3, 0.9))
    el_button_close = el_popup.find_element_by_xpath(".//button[contains(@class, 'button js-close-dialog')]")
    el_button_close.click()
except NoSuchElementException:
    pass
finally:
    el_search = driver.find_element_by_xpath("//input[@id='keywords']")
    el_search.send_keys("Sales Manager")
    el_zip = driver.find_element_by_xpath("//input[@id='zip']")
    el_zip.send_keys("10115")
    el_radius = driver.find_element_by_xpath("//select[@id='radius']")
    el_radius.click()
    el_radius_value = driver.find_element_by_xpath("//option[@value='50']")
    el_radius_value.click()
    # Additional search criteria
    el_current_company = driver.find_element_by_xpath("//input[@name='current_company']")
    el_current_title = driver.find_element_by_xpath("//input[@name='current_title']")
    el_previous_company = driver.find_element_by_xpath("//input[@name='previous_company']")
    ###
    el_search_button = driver.find_element_by_xpath("//button[contains(@class, 'search')]")
    time.sleep(random.uniform(0.2, 1.1))
    el_search_button.click()
    time.sleep(random.uniform(2.7, 4.3))
    el_pagination = driver.find_element_by_xpath("//ol[contains(@class, 'pagination')]")
    el_last_page = el_pagination.find_elements_by_xpath(".//li")[-2]
    no_of_scrolls = int(el_last_page.text) - 1
    file_path = "C:\\Users\\Azat\\Desktop\\test.txt"
    with open(file_path, "w+", encoding='utf-8') as file_object:
        for key in collected_data.keys():
            file_object.write("{};".format(key))
        file_object.write("\n")
        file_object.close()
    parse_page(file_path)
    for j in range(no_of_scrolls):
        scroll_page()
        parse_page(file_path)
    with open(file_path, "r", encoding='utf-8') as file_object:
        file_object.close()
    driver.quit()

import pandas as pd
df = pd.read_csv(file_path, sep = ';', encoding='utf-8', error_bad_lines = False, quoting=0)
df.to_excel("C:\\Users\\Azat\\Desktop\\test.xlsx")