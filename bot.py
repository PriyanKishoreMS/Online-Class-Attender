from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import datetime
from cred import email, password
from colors import bcolors

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

driver = webdriver.Chrome(
    options=opt)
URL = "https://teams.microsoft.com/"
driver.get(URL)
time.sleep(10)  # est. time to load the site


def login():
    emailField = emailField = driver.find_element(
        By.XPATH, '//input[@id="i0116"]')
    emailField.click()
    emailField.send_keys(email)
    driver.find_element(By.XPATH, '//input[@id="idSIButton9"]').click()
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}Email entered{bcolors.ENDC}")
    time.sleep(5)  # password scr. est. time
    passwd = driver.find_element(By.XPATH, '//input[@name="passwd"]')
    passwd.click()
    passwd.send_keys(password)
    driver.find_element(By.XPATH, '//input[@id="idSIButton9"]').click()
    print(f"{bcolors.OKGREEN}{bcolors.BOLD}Password Entered{bcolors.ENDC}")
    time.sleep(3)  # stay signed scr. est. time
    driver.find_element(By.XPATH, '//input[@id="idSIButton9"]').click()


def timediff():  # tells the difference between current time and next class time
    count = 0
    now = datetime.datetime.now().strftime("%H.%M")
    for i in tim:
        count = count+1
        if now <= i:
            break

    format = '%H.%M'
    timer = datetime.datetime.strptime(
        tim[count-1], format) - datetime.datetime.strptime(now, format)
    stime = str(timer)
    mins = (int(stime[2:4]))
    return mins


def join(cls, now):
    while True:
        try:
            joinbtn = driver.find_element(
                By.XPATH, '//button[@title="Join call with video"]')
            joinbtn.click()

        except:
            print(
                f"{bcolors.WARNING}Class not sheduled yet!, trying again in 5 mins{bcolors.ENDC}")
            time.sleep(300)
            if timediff() <= 30:  # if class is not scheduled at correct time, retried every 5mins for 20mins
                print(
                    f"{bcolors.FAIL}{bcolors.BOLD}No class Scheduled!{bcolors.ENDC}")
                break

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
            print(f"{bcolors.HEADER}joined class: {cls} at {now}{bcolors.ENDC}")
            break


def leave(cls):
    now = datetime.datetime.now().strftime("%H.%M")
    teamsbtn = driver.find_element(
        By.XPATH, '//button[@id="app-bar-2a84919f-59d8-4441-a975-2a8c2643b741"]')
    try:
        teamsbtn.click()
        time.sleep(3)
        driver.find_element(By.XPATH, '//button[@id="hangup-button"]').click()
        print(f"{bcolors.WARNING}Left from: {cls} at {now}{bcolors.ENDC}\n")
        teamsbtn.click()

    except:
        print(f"{bcolors.WARNING}Left from: {cls} at {now}{bcolors.ENDC}\n")
        teamsbtn.click()
        teamsbtn.click()


def selectClass():
    today = datetime.datetime.now().strftime("%A")
    print('\x1b[6;30;42m' + "Logged in" + '\x1b[0m' + "\n")
    time.sleep(25)  # est. time to show teams
    now = datetime.datetime.now().strftime("%H.%M")
    # now = "14.42"
    count = 0
    for i in tim:
        count = count+1
        if now <= i:
            break
    for cls in timetable[today][count-2:]:
        now = datetime.datetime.now().strftime("%H.%M")
        mins = timediff()
        secs = mins * 60
        print(f"Class: {cls}\nTime duration: {mins}min / {secs}sec")

        if cls == "free":
            print("\nFree Class")
            print(
                f"{bcolors.WARNING}Queued for the next {timediff()}mins{bcolors.ENDC}")
            time.sleep(timediff()*60)
            time.sleep(60)
        elif cls == "break":
            print("\n20 mins Break")
            print(
                f"{bcolors.WARNING}Queued for the next {timediff()}mins{bcolors.ENDC}")
            time.sleep(timediff()*60)
            time.sleep(60)
        else:
            driver.find_element(
                By.XPATH, f'//div[@aria-label="{cls}"]').click()
            time.sleep(20)  # class page est. time
            join(cls, now)
            print(
                f"{bcolors.WARNING}Queued for the next {timediff()}mins{bcolors.ENDC}")
            # class time (current time - next class time)
            time.sleep(timediff()*60)
            leave(cls)
            time.sleep(60)


login()
selectClass()
