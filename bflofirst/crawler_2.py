from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, os, re
from email_logger import send_log

from pyvirtualdisplay import Display
from lxml.html import InputElement
display = Display(visible=0, size=(1024, 768))

def headless():
    display.start()
    
def start_driver():
    headless()
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : "./"}
    chromeOptions.add_experimental_option("prefs",prefs)
    chromedriver = './chromedriver'
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)
    return driver

def parcel_crawler(driver, sbl):
    #Take us to main search page, searches for sbl
    driver.get("https://paytax.erie.gov/webprop/index.asp")
    driver.find_element_by_name('txtsbl').send_keys(str(sbl)+'.\n')
    overflow = 0
    log = ""
    while overflow < 1000:
        overflow += 1
        time.sleep(1)
        driver.save_screenshot('log.png')
        links = driver.find_elements_by_tag_name('a')
        l = None
        for l in links:
            try:
                link = l.get_attribute('href')
                if 'KEY' in link:
                    sbl = re.findall('sbl=(.*)&', link)[0]
                    key = re.findall('KEY=(.*)', link)[0]
                    log += sbl + "," + key + '\n'
            except:
                pass
        if driver.find_elements_by_tag_name('p')[0].text == '**** Last Record Found ****':
            break
        else:
            if l != None:
                l.click()
            else:
                break
    return log
            
if __name__ == "__main__":
    try:
        tmp = open('parcel_links.csv')
        tmp.close()
    except:
        tmp = open('parcel_links.csv','w')
        tmp.close()
    wait_time = 10.
    driver = start_driver()
    for i in range(90,1000):
        while True:
            print "Attempting: " + str(i)
            data = open('parcel_links.csv','a')
            try:
                res = parcel_crawler(driver, i)
                data.write(res)
                print "Success.\n"
                if wait_time > 10:
                    wait_time /= 2
                break
            except:
                print "Failure: " + str(i)
                print "Sending Log to nathanmargaglio@gmail.com"
                send_log()
                #time.sleep(wait_time)
                if wait_time < 600:
                    wait_time *= 2
                print "Current Wait Time: " + str(wait_time)
                time.sleep(wait_time)
            data.close()
