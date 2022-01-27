# Online Class Attender Bot (MS teams)
 Attends all your classes for the  day at scheduled time in the order of your time-table.

![demo ms teams attender2](https://user-images.githubusercontent.com/80768547/151298089-78f1dc5e-615f-4e07-935a-1283e4f91444.png)

## Pre-requisites
* Python
* Chrome
* Selenium
* [ChromeDriver](https://chromedriver.chromium.org/downloads) 


## Windows config
```cmd
pip3 install -U selenium
pip3 install webdriver_manager
```
* Enter the path to ChromeDriver.exe in *windowsbot.py*
* Enter credentials in *cred.py*
* Tweak your timetable and timings in *timateable.py*
* Run *windowsbot.py*

## Linux config
* Setup ChromeDriver
* Enter credentials in *cred.py*
* Tweak your timetable and timings in *timateable.py*
* Run *bot.py*

> ### Note:
> Reduce the number in *time.sleep()* functions at required places, if your network connection is strong.