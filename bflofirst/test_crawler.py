from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, os, re, sys

from pyvirtualdisplay import Display
from lxml.html import InputElement
from config import MLS_USERNAME, MLS_PASSWORD

display = Display(visible=0, size=(1024, 768))


def headless():
    display.start()


def crawler(date="today"):
    #headless()
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory": "./"}
    chromeOptions.add_experimental_option("prefs", prefs)
    chromedriver = './chromedriver'
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

    driver.get("https://idp.mynysmls.com/idp/Authn/UserPassword")
    driver.find_element_by_css_selector("a[onclick*='buffalo']").click()

    print("Logging in to MLS...")
    time.sleep(3)

    inputElement = driver.find_element_by_id("j_username")
    # inputElement.click()
    inputElement.send_keys(MLS_USERNAME)
    driver.find_element_by_id("loginbtn").click()
    inputElement = driver.find_element_by_id("password")
    inputElement.send_keys(MLS_PASSWORD)
    driver.find_element_by_id("loginbtn").click()

    # InputElement.send_keys(Keys.ENTER)
    time.sleep(3)

    print("Moving to Matrix...")
    # driver.get("http://nys.mlsmatrix.com/Matrix/Search/Residential/SingleFamily")
    driver.get("http://nys.mlsmatrix.com/Matrix/Search/CrossProperty/CrossProperty")

    time.sleep(2)
    print("Searching for expires...")

    if date == "today":
        driver.find_element_by_css_selector("a[id*='m_ucSearchButtons_m_lbSearch']").click()
    # driver.find_element_by_id("m_ucResultsPageTabs_m_pnlResultsTab").click()
    else:
        print("Setting date")
        time.sleep(2)
        date_input = driver.find_element_by_id("FmFm1_Ctrl42_106_Ctrl42_TB")
        date_input.clear()
        date_input.send_keys(date)
        time.sleep(2)
        driver.find_element_by_css_selector("a[id*='m_ucSearchButtons_m_lbSearch']").click()

    current_page = 0
    sources = []
    for nn in range(100):
        time.sleep(3)
        print("Parsing source on page {}".format(current_page))
        source = driver.page_source
        sources.append(source)
        driver.find_element_by_link_text("Next").click()
        current_page += 1

        soup = BeautifulSoup(source, "lxml")
        next_link = str(soup.find_all("a", text="Next")[0])
        if 'disabled' in next_link:
            break
    return sources


def mls_parser(source, forced_date=None):
    soup = BeautifulSoup(source, "lxml")

    rows = soup.find_all("tr", {'class': ['DisplayRegRow', 'DisplayAltRow']})
    print(len(rows))
    print("Starting Posting...")
    for r in rows:
        try:
            cells = r.find_all("td")
            data = {}

            data['address'] = cells[7].get_text()
            data['city'] = cells[24].get_text()
            data['zipcode'] = cells[25].get_text()
            data['owner_name'] = cells[27].get_text() + " " + cells[28].get_text()

            data['owner_address'] = cells[35].get_text()
            data['owner_city'] = cells[34].get_text()
            data['owner_zipcode'] = cells[36].get_text()
        except:
            continue

        if data['owner_address'] == '':
            data['owner_address'] = data['address']
        if data['owner_city'] == '':
            data['owner_city'] = data['city']
        if data['owner_zipcode'] == '':
            data['owner_zipcode'] = data['zipcode']

        if forced_date != None:
            data['date_created'] = forced_date

        data['priority'] = 1.0
        pst = requests.post("http://buffalodataserver.com/leads", json=data)
        try:
            print(pst.json())
        except:
            pass


def yp_crawler():
    print("Starting YP Crawler...")
    r = requests.get("http://buffalodataserver.com/leads/phones")

    url = "http://people.yellowpages.com/whitepages?first={}&last={}&zip={}&state=ny"
    re_address = """<div class="address">\n(.*?)<"""
    re_phone = """<div class="phone">\n(.*?)<"""

    for lead in r.json():
        print(lead)
        try:
            first_name = lead['owner_name'].split(' ')[0]
            last_name = lead['owner_name'].split(' ')[-1]
            zipcode = lead['owner_zipcode']
            street = lead['owner_address'].split(' ')[1]
        except:
            continue

        ypr = requests.get(url.format(first_name, last_name, zipcode))

        addresses = re.findall(re_address, ypr.text)
        phones = re.findall(re_phone, ypr.text)
        results = zip(addresses, phones)

        phone = None
        for n in results:
            if street in n[0].lstrip().rstrip():
                phone = n[1].lstrip().rstrip()
        if phone:
            print('\t{}'.format(phone))
            post_data = {'owner_phone': phone, 'phone_status': 'found'}
            pst = requests.post("http://buffalodataserver.com/leads/{}".format(lead['id']), json=post_data)
        else:
            post_data = {'phone_status': 'not_found'}
            pst = requests.post("http://buffalodataserver.com/leads/{}".format(lead['id']), json=post_data)
        time.sleep(2)


def get_historical(m0, d0, y0, m1=None, d1=None, y1=None):
    if m1 != None:
        date_range = '{}/{}/{}-{}/{}/{}'.format(m0, d0, y0, m1, d1, y1)
    else:
        date_range = '{}/{}/{}'.format(m0, d0, y0)

    forced_date = '{}-{}-{}'.format(y0, m0, d0)
    print(forced_date)
    try:
        sources = crawler(date_range)
        for s in sources:
            mls_parser(s, forced_date)
    except:
        e = sys.exc_info()[0]
        print(e)
        print("Error @ {}\n".format(forced_date))

    yp_crawler()

print("Starting...")
sources = crawler()
for s in sources:
    mls_parser(s)
yp_crawler()
