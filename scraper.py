from selenium import webdriver
import os
import selenium.common.exceptions as error
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time, datetime, pytz


## Constant (URL)
URL = "https://www.gla.ac.uk/apps/timetable/#/login"


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
    
    try:
        element_present = EC.presence_of_element_located((By.XPATH, "//*[@id='app']/div/div[1]/div[1]/a"))
        WebDriverWait(browsers[guidd], 4).until(element_present)
        browsers[guidd].find_element_by_xpath("//*[@id='app']/div/div[1]/div[1]/a").click()
        if browsers[guidd].current_url == "https://www.gla.ac.uk/apps/timetable/#/timetable":
            return 1
    
    except error.UnexpectedAlertPresentException:
        browsers[guidd].quit()
        return 2
    
    except:
        browsers[guidd].quit()
        return 3

def check_browser(guidd):
    
    try:
        if browsers[guidd].current_url == "https://www.gla.ac.uk/apps/timetable/#/timetable":
            return True
        return True
    except error.WebDriverException:
        return False
    except KeyError:
        return False
    return True

def format_table(guidd):
    
    class_data = []
    
    for i in range(1,8):
        class_data.append(browsers[guidd].find_element_by_xpath("//*[@id='eventModal']/div/div/div[2]/table/tr[{}]/td".format(str(i))).text)
    
    return class_data[0] + " ({}) ".format(class_data[2]) + "\nfrom {} to {} ".format(class_data[4],class_data[5]) + "\nat {}.".format(class_data[1])


def read_day(guidd):
    
    message = ""
    try:
        element_present = EC.visibility_of_all_elements_located((By.CLASS_NAME, "fc-time-grid-event.fc-event.fc-start.fc-end"))
        WebDriverWait(browsers[guidd], 1).until(element_present)
        classes = browsers[guidd].find_elements_by_class_name("fc-time-grid-event.fc-event.fc-start.fc-end")
        message+= "You have..\n\n"
        
        for clas in classes:
            try:
                clas.click()
                element_present = EC.visibility_of_element_located((By.CLASS_NAME, "dialogueTable"))
                WebDriverWait(browsers[guidd], 1).until(element_present)
                table = browsers[guidd].find_element_by_class_name("dialogueTable")
                message+=format_table(guidd)+"\n\n"
                browsers[guidd].find_element_by_class_name("close.text-white").click()
    
            except error.ElementNotInteractableException:
                browsers[guidd].implicitly_wait(3)
                clas.click()
                element_present = EC.visibility_of_element_located((By.CLASS_NAME, "dialogueTable"))
                WebDriverWait(browsers[guidd], 1).until(element_present)
                table = browsers[guidd].find_element_by_class_name("dialogueTable")
                message+=format_table(guidd)+"\n\n"
                browsers[guidd].find_element_by_class_name("close.text-white").click()
            
            except:
                message+="(Unable to fetch class)\n"
                continue
    
    except error.TimeoutException:
        message+="There seem to be no classes."
    
    return message


def read_now(guidd):  # Yet to Test
    message = ""
    try:
        element_present = EC.visibility_of_all_elements_located((By.CLASS_NAME, "fc-time-grid-event.fc-event.fc-start.fc-end"))
        WebDriverWait(browsers[guidd], 1).until(element_present)
        classes = browsers[guidd].find_elements_by_class_name("fc-time-grid-event.fc-event.fc-start.fc-end")
        message+= "Up next, you have..\n\n"
        
        for clas in classes:
            try:
                clas.click()
                element_present = EC.visibility_of_element_located((By.CLASS_NAME, "dialogueTable"))
                WebDriverWait(browsers[guidd], 1).until(element_present)
                table = browsers[guidd].find_element_by_class_name("dialogueTable")
                class_data = []
                
                for i in range(1,8):
                    class_data.append(browsers[guidd].find_element_by_xpath("//*[@id='eventModal']/div/div/div[2]/table/tr[{}]/td".format(str(i))).text)                
                
                tyme = str(datetime.datetime.now(tz=pytz.timezone('Europe/London')).date()) + " {}".format(class_data[4])
                classtime = datetime.datetime.strptime(tyme, '%Y-%m-%d %I:%M %p')
                
                if(datetime.datetime.now(tz=pytz.timezone('Europe/London')) <= classtime):
                    message+=((class_data[0] + " ({}) ".format(class_data[2]) + "\nfrom {} to {} ".format(class_data[4],class_data[5]) + "\nat {}.".format(class_data[1])) + "\n\n")
                    break
                browsers[guidd].find_element_by_class_name("close.text-white").click()
            
            except error.ElementNotInteractableException:
                browsers[guidd].implicitly_wait(3)
                clas.click()
                element_present = EC.visibility_of_element_located((By.CLASS_NAME, "dialogueTable"))
                WebDriverWait(browsers[guidd], 1).until(element_present)
                table = browsers[guidd].find_element_by_class_name("dialogueTable")
                class_data = []
                
                for i in range(1,8):
                    class_data.append(browsers[guidd].find_element_by_xpath("//*[@id='eventModal']/div/div/div[2]/table/tr[{}]/td".format(str(i))).text)                
                
                tyme = str(datetime.datetime.now(tz=pytz.timezone('Europe/London')).date()) + " {}".format(class_data[4])
                classtime = datetime.datetime.strptime(tyme, '%Y-%m-%d %I:%M %p')
                
                if(datetime.datetime.now(tz=pytz.timezone('Europe/London')) <= classtime):
                    message+=((class_data[0] + " ({}) ".format(class_data[2]) + "\nfrom {} to {} ".format(class_data[4],class_data[5]) + "\nat {}.".format(class_data[1])) + "\n\n")
                    break
                browsers[guidd].find_element_by_class_name("close.text-white").click()
            
            except:
                message+="(Unable to fetch class)\n"
                continue
    
    except error.TimeoutException:
        message+="There seem to be no classes."
    
    if message == "Up next, you have..\n\n":
        return "No class. :) "
        
    return message


def specific_day(date_entry, guidd):
    
    try:
        year, month, day = map(int, date_entry.split('-'))
        date1 = datetime.date(year, month, day)
        message = loop_days((date1 - datetime.date.today()).days, guidd)
        return message

    except ValueError:
        return "The date seems invalid."


def loop_days(n,guidd):

    if n < 365 and n>=0:
        for i in range(n):
            browsers[guidd].find_element_by_class_name("fc-next-button.fc-button.fc-button-primary").click()

        message = read_day(guidd)
        browsers[guidd].find_element_by_class_name("fc-today-button.fc-button.fc-button-primary").click()
        return message

    elif n<0 and n > -365:
        for i in range((n*(-1))):
            browsers[guidd].find_element_by_class_name("fc-prev-button.fc-button.fc-button-primary").click()
        message = read_day(guidd)
        browsers[guidd].find_element_by_class_name("fc-today-button.fc-button.fc-button-primary").click()
        return message

    else:
        return "That seems way too far out."


def close(guidd):

    browsers[guidd].find_element_by_class_name("btn.btn-primary.btn-block.nav-button.router-link-active").click()
    browsers[guidd].find_element_by_class_name("btn.btn-primary.btn-rounded").click()
    browsers[guidd].quit()