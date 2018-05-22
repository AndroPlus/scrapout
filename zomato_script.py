from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import time
# create a new Firefox session
#cap = DesiredCapabilities().FIREFOX
#cap["marionette"] = False
class MyTest(object):
	
	def __init__(self):
		self.pageNo = 1
		self.storeUrl = []
		self.storeName = []
		options = Options()
		self.driver = webdriver.Firefox(firefox_options=options, executable_path='D:\Ram\geckodriver.exe')

	def getParentUrls(self):	
		print ("start scrap --"+"https://www.zomato.com/puducherry/restaurants?page="+str(self.pageNo))
		self.driver.get("https://www.zomato.com/puducherry/restaurants?page="+str(self.pageNo))
		self.driver.implicitly_wait(10)
		self.driver.maximize_window()

		lists = self.driver.find_elements_by_class_name("content")
		# get the number of elements found
		print ("Found " + str(len(lists)))

		# iterate through each element and print the text that is
		# name of the search
		for listitem in lists[1:2]:	
			searchObj  = re.search(r'<a class="result-title[^\"]+" href=\"([^\"]+)\" title=\"([^\"]+)\"', listitem.get_attribute('innerHTML'),re.M|re.I)
			if  searchObj:
				print ("Store Url : ", searchObj.group(1))
				self.storeUrl.append(searchObj.group(1))
				print ("Store Name : ", searchObj.group(2))
				self.storeName.append(searchObj.group(2))			
			else:
				print ("No match!!")

			addressObj  = re.search(r'<div[^>]*class=\"[^\"]+search-result-address[^\"]+\"\s*title=\"([^\"]+)\"', listitem.get_attribute('innerHTML'),re.M|re.I)
			if  addressObj:
				print ("address : ", addressObj.group(1))			
			else:
				print ("No match!!")

			ratingObj  = re.search(r'<div[^>]*class=\"rating-popup[^\"]+\">([^>]+)<\/div>', listitem.get_attribute('innerHTML'),re.M|re.I)
			if  ratingObj:
				print ("ratingObj : ", ratingObj.group(1).strip())				

			CUISINES  = re.findall(r'<a\s*title=\"([^\"]+)\"', listitem.get_attribute('innerHTML'),re.M|re.I)
			for CUISINE in CUISINES:
				print ("CUISINE--"+CUISINE)	


	def getImageUrls(self):		
		for storeurl in self.storeUrl:
			self.driver.get(storeurl+"/menu")
			self.driver.implicitly_wait(10)
			time.sleep(5) # wait for 5 secondscls
			menuHTMLBody = self.driver.find_element_by_tag_name("body")	
			menuImageUrls  = re.findall(r'\"url\":\"([^\"]+)\"', menuHTMLBody.get_attribute('innerHTML'),re.M|re.I)
			
			for menuImageUrl in menuImageUrls:
				print ("menuImageUrl--"+menuImageUrl)

	
	def browserQuit(self):		
		# close the browser window
		self.driver.quit()

test =  MyTest()

for i in range(1):	
	test.getParentUrls()
	#test.getImageUrls()
	print("scrap for page "+str(test.pageNo) + " done..")
	test.pageNo = test.pageNo + 1
	test.storeUrl = []
	test.storeName = []

test.browserQuit()		

