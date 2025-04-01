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
    browser.add_cookie({"name": "MUSIC_U", "value": "00D2C4DB8CAFA24743B18964B6C0EC8F2E35733E758D375190D7FE49EE18045F3BB4FBCB740FCA164A56D874ECC44F326B31610B6B545972F2746B9E606EB1B7D63280EAA4F281D93E90A9FE03EF74B149C34835BCD97C3395AD03A773CDA010D72E6ADDE6B565906DF3706745FB3AACBD839F173CCC2C3760619B2CD43E398537BCD89444354DAB553B006FBD505F845ED0391E6B87616CA1A66D1C32A462E026B07F73EEDFD0C01D880974A58382D1E29881FE8A50935288ADB8D641848893E4ED56360BCA9F606160349431FC6293BFE19E385333F53ABEFD687171C17C7D9BA712728240FE00785D42B8A74241C6EA6E53B40A8172058459124B385977EEC32B6647D89E724E3303113F720B011763A23EAFF0A07F8E9363BF6829F6A9EFDA8297244CC228982BA7C4230D02BB4243CD8E8A292A45E73C79BC2C8A5F420BA649F6D716EFD48F94B27F691A668CC3D20B754157C45E54CBBADF8719732CF8C9"})
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
