from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from cred import email, password

opt = Options()
prefs = {"credentials_enable_service": False,
         "profile.password_manager_enabled": False}
opt.add_argument("--disable-infobars")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")
opt.add_experimental_option("prefs", prefs)
opt.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(options=opt)
URL = "https://teams.microsoft.com/"
driver.get(URL)
time.sleep(5)


def login():
    emailField = emailField = driver.find_element(
        By.XPATH, '//input[@id="i0116"]')
    emailField.click()
    emailField.send_keys(email)
    driver.find_element(By.XPATH, '//input[@id="idSIButton9"]').click()
    time.sleep(3)
    passwd = driver.find_element(By.XPATH, '//input[@name="passwd"]')
    passwd.click()
    passwd.send_keys(password)
    driver.find_element(By.XPATH, '//input[@id="idSIButton9"]').click()
    time.sleep(3)
    driver.find_element(By.XPATH, '//input[@id="idSIButton9"]').click()


login()
