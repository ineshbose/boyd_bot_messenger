from selenium import webdriver
import os
import selenium.common.exceptions as error
import time, datetime


## Constants
URL = "https://www.gla.ac.uk/apps/timetable/#/login"
weekdayMapping = {"MONDAY":0, "TUESDAY":1, "WEDNESDAY":2, "THURSDAY":3, "FRIDAY":4}
###


## Selenium Stuff
options = webdriver.ChromeOptions()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--log-level=3')
browsers = {}
###


def login(guidd,passww):
    
    browsers[guidd] = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    browsers[guidd].get(URL)
    browsers[guidd].find_element_by_id("guid").send_keys(guidd)
    browsers[guidd].find_element_by_id("password").send_keys(passww)
    browsers[guidd].find_element_by_xpath("//*[@id='app']/div/main/button").click()
    time.sleep(4)
    
    try:
        browsers[guidd].find_element_by_xpath("//*[@id='app']/div/div[1]/div[1]/a").click()
        time.sleep(1)
        if browsers[guidd].current_url == "https://www.gla.ac.uk/apps/timetable/#/timetable":
            return 1
    
    except error.UnexpectedAlertPresentException as e:
        browsers[guidd].quit()
        return 2
    
    except error.NoSuchElementException as load:
        browsers[guidd].quit()
        return 3


def format_table(guidd):
    
    class_data = []
    
    for i in range(1,8):
        class_data.append(browsers[guidd].find_element_by_xpath("//*[@id='eventModal']/div/div/div[2]/table/tr[{}]/td".format(str(i))).text)
    
    return class_data[0] + " ({}) ".format(class_data[2]) + "\nfrom {} to {} ".format(class_data[4],class_data[5]) + "\nat {}.".format(class_data[1])


def read_day(guidd):
    
    message = ""
    time.sleep(1)
    classes = browsers[guidd].find_elements_by_class_name("fc-time-grid-event.fc-event.fc-start.fc-end")
    
    if classes == []:
        message+= "There seem to be no classes."
    
    else:
        message+= "You have..\n\n"
        for clas in classes:
    
            try:
                clas.click()
                time.sleep(1)
                table = browsers[guidd].find_element_by_class_name("dialogueTable")
                message+=format_table(guidd)+"\n\n"
                browsers[guidd].find_element_by_class_name("close.text-white").click()
    
            except error.ElementNotInteractableException as e:
                message+="(Unable to fetch class)\n"
                continue
    
    return message


def specific_day(date_entry, guidd):
    
    try:
        year, month, day = map(int, date_entry.split('-'))
        date1 = datetime.date(year, month, day)
        message = loop_days((date1 - datetime.date.today()).days, guidd)
        return message

    except ValueError as ve:
        return "The date seems invalid."


def loop_days(n,guidd):

    if n < 365 and n>=0:
        for i in range(n):
            browsers[guidd].find_element_by_class_name("fc-next-button.fc-button.fc-button-primary").click()

        message = read_day(guidd)
        browsers[guidd].find_element_by_class_name("fc-today-button.fc-button.fc-button-primary").click()
        return message

    else:
        return "That seems way too far out."


def close(guidd):

    browsers[guidd].find_element_by_class_name("btn.btn-primary.btn-block.nav-button.router-link-active").click()
    browsers[guidd].find_element_by_class_name("btn.btn-primary.btn-rounded").click()
    browsers[guidd].quit()