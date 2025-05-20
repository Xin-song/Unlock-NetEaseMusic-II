# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0004B6BA2F6E9BEE45B65E81D888B6C46F77CD415B4DDBDDC499F7FEADB99F18B7F27ECA0554DD4A261FD0447AD06F7E958E94B5D280DCE57D1C3EF0B124F5D57136559B0C4AC31AE593732A5DF794BA138610176B25C898BD07852AC6849C7E2CD444C23EB58FE3C7F4E4E671D42767A592116F91AEBA02DBCBB3894EF77701884E117FB5C8C58D44A7918EEE49A6E147C213B1F5DC7DAD5AE22D11CEF0B4AB65D2FF1881C136BBB828CB943DD256D803F36FD4FE7668167E8D4A9690DF208842FCBF28E73475EA95F4D4C68C4366CD6DA76C8EF3AF2173C389AB29ED57B352517A5F210D7539C725DACCC10872DC549E6B326F596EBE242AD76EB96DDA6233D0C526894AAB7A4E2359800B20F5D9FCC789F341A572B8C71115007B0B3E47DC9A797CFFB6073A5874413135CF6408E43B9CDB87582D7FAE3B15E23815C7F99D277C44E9F7CBA3B8A1D2542F18D9BDFBBA"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
