from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import datetime
from cred import email, password

from timetable import timetable, tim

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 1
})
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
    print("Email entered")
    time.sleep(3)
    passwd = driver.find_element(By.XPATH, '//input[@name="passwd"]')
    passwd.click()
    passwd.send_keys(password)
    driver.find_element(By.XPATH, '//input[@id="idSIButton9"]').click()
    print("Password Entered")
    time.sleep(3)
    driver.find_element(By.XPATH, '//input[@id="idSIButton9"]').click()


def join(cls, now):
    try:
        joinbtn = driver.find_element(
            By.XPATH, '//button[@title="Join call with video"]')
        joinbtn.click()

    except:
        i = 1
        while(i <= 15):
            print("Meeting hasn't started yet, trying again")
            time.sleep(60)
            driver.refresh()
            join(cls, now)
            i += 1
            print(f"{cls} is not scheduled today!")

    else:
        time.sleep(4)
        webcam = driver.find_element(
            By.XPATH, '//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button/span[1]')
        if(webcam.get_attribute('title') == 'Turn camera off'):
            webcam.click()
        time.sleep(1)

        microphone = driver.find_element(By.XPATH,
                                         '//*[@id="preJoinAudioButton"]/div/button/span[1]')
        if(microphone.get_attribute('title') == 'Mute microphone'):
            microphone.click()

        time.sleep(1)
        joinnowbtn = driver.find_element(By.XPATH,
                                         '//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button')
        joinnowbtn.click()
        print(f"joined class: {cls} at {now}")


def jointest(cls, now):
    print(f"Joined cls: {cls} at {now}")


def leave(cls):
    teamsbtn = driver.find_element(
        By.XPATH, '//button[@id="app-bar-2a84919f-59d8-4441-a975-2a8c2643b741"]')
    try:
        driver.find_element(By.XPATH, '//button[@id="hangup-button"]').click()
        print(f"Left from: {cls}")
        teamsbtn.click()
        teamsbtn.click()

    except:
        print(f"Left from: {cls}")
        teamsbtn.click()
        teamsbtn.click()


def selectClass():
    today = datetime.datetime.now().strftime("%A")
    print("Logged in")
    time.sleep(20)
    now = datetime.datetime.now().strftime("%0H.%M")
    # now = "14.42"
    count = 0
    for i in tim:
        count = count+1
        if now <= i:
            break
    for cls in timetable[today][count-2:]:
        now = datetime.datetime.now().strftime("%0H.%M")
        # now = "14.42"
        count = 0
        for i in tim:
            count = count+1
            if now <= i:
                break

        format = '%H.%M'
        timer = datetime.datetime.strptime(
            tim[count-1], format) - datetime.datetime.strptime(now, format)
        # print(timer)
        ftime = str(timer)
        stime = (int(ftime[2:4]))
        ftime = stime * 60
        print(f"Class time duration: {stime}min / {ftime}sec")

        if cls == "free":
            print("\nFree Class\n")
            time.sleep(ftime)
        elif cls == "break":
            print("\n20 mins Break\n")
            time.sleep(ftime)
        else:
            driver.find_element(
                By.XPATH, f'//div[@aria-label="{cls}"]').click()
            time.sleep(20)
            jointest(cls, now)
            print(f"Attending class for the next {stime}mins")
            time.sleep(ftime)
            leave(cls)
            # driver.find_element(
            #     By.XPATH, f'//button[@aria-label="Go back to all teams"]').click()
            time.sleep(60)


login()
selectClass()
