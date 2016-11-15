from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, os

from pyvirtualdisplay import Display
from lxml.html import InputElement
display = Display(visible=0, size=(1024, 768))

def headless():
	display.start()

def crawler(date="today"):
	try:
		os.remove("full_data.csv")
	except:
		pass
	headless()
	chromeOptions = webdriver.ChromeOptions()
	prefs = {"download.default_directory" : "./"}
	chromeOptions.add_experimental_option("prefs",prefs)
	chromedriver = './chromedriver'
	driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)
	
	#driver = webdriver.PhantomJS()
	#driver = webdriver.Firefox(executable_path='./geckodriver')

	driver.get("https://idp.mynysmls.com/idp/Authn/UserPassword")
	driver.find_element_by_css_selector("a[onclick*='buffalo']").click()
	
	print "Logging in to MLS..."
	time.sleep(3)

	inputElement = driver.find_element_by_id("j_username")
	#inputElement.click()
	inputElement.send_keys('smithray')
	driver.find_element_by_id("loginbtn").click()
	inputElement = driver.find_element_by_id("password")
	inputElement.send_keys('queen1986')
	driver.find_element_by_id("loginbtn").click()
	
	#InputElement.send_keys(Keys.ENTER)
	time.sleep(3)
	
	print "Moving to Matrix..."
	#driver.get("http://nys.mlsmatrix.com/Matrix/Search/Residential/SingleFamily")
	driver.get("http://nys.mlsmatrix.com/Matrix/Search/CrossProperty/CrossProperty")
	
	time.sleep(2)
	print "Searching for expires..."
	
	if date == "today":
		driver.find_element_by_css_selector("a[id*='m_ucSearchButtons_m_lbSearch']").click()
		#driver.find_element_by_id("m_ucResultsPageTabs_m_pnlResultsTab").click()
	else:
		print "Setting date"
		driver.find_element_by_id("FmFm9_Ctrl42_106_Ctrl42_TB").clear()
		driver.find_element_by_id("FmFm9_Ctrl42_106_Ctrl42_TB").send_keys(date)
		time.sleep(2)
		driver.find_element_by_css_selector("a[id*='m_ucSearchButtons_m_lbSearch']").click()

	#time.sleep(2)
	#driver.find_element_by_css_selector("a[id*='m_lnkCheckAllLink']").click()

	time.sleep(2)
	driver.find_element_by_css_selector("a[id*='m_lbExport']").click()

	time.sleep(2)
	print "Exporting..."
	link = driver.find_element_by_css_selector("a[id*='m_btnExport']").click()
	print link
	
	print "Done!"
	time.sleep(5)
	driver.quit()
	
def facebook_leads():
	url = "https://www.facebook.com/ads/manager/ad/ads/?act=38483350&pid=p2&ids=6053884652368&date=lifetime"
	chromeOptions = webdriver.ChromeOptions()
	prefs = {"download.default_directory" : "./"}
	chromeOptions.add_experimental_option("prefs",prefs)
	chromedriver = './chromedriver'
	driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)
	
	driver.get(url)
	driver.find_element_by_id("email").send_keys("nathanmargaglio@gmail.com")
	driver.find_element_by_id("pass").send_keys("margaglio22")
	driver.find_element_by_id("loginbutton").click()
	
	raw_input()

if __name__ == "__main__":
	crawler()
