import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
from time import sleep


class WhatsApp:
    __version = "2.3000.1014080102"
    __firefox_path = "C:/Program Files/Mozilla Firefox/firefox.exe"
    __url = "https://web.whatsapp.com"
    __driver = webdriver.Firefox()

    def init_webm(self):
        self.__driver.get(self.__url)

    def search_contact(self, msisdn):
        found = False

        try:

            button = WebDriverWait(self.__driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="new-chat-outline"]')))
            button.click()
            search_area = WebDriverWait(self.__driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Текстовое поле поиска"]')))
            self.insert_text(search_area, msisdn)
            fmsisdn = self.__reformat_msisdn(msisdn)
            time.sleep(3)
            print("SEARCH WAIT")
            time.sleep(3)
            contact = WebDriverWait(self.__driver, 30).until(EC.presence_of_element_located((By.XPATH, '//span[@title="' + fmsisdn +'"]')))
            contact.click()
            found = True
        except Exception as err:
            print(err)

        return found

    def back(self):
        path = '//div[@aria-label="Назад"]'
        btn = WebDriverWait(self.__driver, 20).until(EC.element_to_be_clickable((By.XPATH, path)))
        btn.click()

    def insert_text(self, elm, text):

        elm.click()

        for i in text:
            elm.send_keys(i)
            f = random.uniform(0.1, 0.3)
            sleep(f)

    def __reformat_msisdn(self, msisdn):
        return "+" + msisdn[0] + " " + msisdn[1:4] + " " + msisdn[4:7] + " " + msisdn[7:len(msisdn)]

    def send_message(self, message):
        path = '//div[@aria-label="Введите сообщение"]'
        insert = WebDriverWait(self.__driver, 20).until(EC.element_to_be_clickable((By.XPATH, path)))
        insert.click()
        self.insert_text(insert, message)
        insert.send_keys(Keys.ENTER)

    def get_version(self):
        return self.__version