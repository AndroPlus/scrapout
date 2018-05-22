from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import time
import csv
import urllib.request
import os
from urllib.parse import urlparse
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
			storeUrl = ""
			storeName = ""
			storeAddress = ""
			storeRating = ""
			storeCuisines = []
			searchObj  = re.search(r'<a class="result-title[^\"]+" href=\"([^\"]+)\" title=\"([^\"]+)\"', listitem.get_attribute('innerHTML'),re.M|re.I)
			if  searchObj:
				storeUrl = searchObj.group(1)
				storeName = searchObj.group(2)

				print ("Store Url : ", storeUrl)
				self.storeUrl.append(storeUrl)

				print ("Store Name : ", storeName)
				self.storeName.append(storeName)			
			else:
				print ("No match!!")

			addressObj  = re.search(r'<div[^>]*class=\"[^\"]+search-result-address[^\"]+\"\s*title=\"([^\"]+)\"', listitem.get_attribute('innerHTML'),re.M|re.I)
			if  addressObj:
				storeAddress = addressObj.group(1)
				print ("address : ", storeAddress)			
			else:
				print ("No match!!")

			ratingObj  = re.search(r'<div[^>]*class=\"rating-popup[^\"]+\">([^>]+)<\/div>', listitem.get_attribute('innerHTML'),re.M|re.I)
			if  ratingObj:
				storeRating = ratingObj.group(1).strip()
				print ("ratingObj : ", storeRating)				

			CUISINES  = re.findall(r'<a\s*title=\"([^\"]+)\"', listitem.get_attribute('innerHTML'),re.M|re.I)
			for CUISINE in CUISINES:
				print ("CUISINE--"+CUISINE)	
				storeCuisines.append(CUISINE)

			with open('restaurant_data.csv', 'a') as csvfile:
				spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
				spamwriter.writerow([storeName, storeUrl, storeAddress, storeRating, storeCuisines])


	def getImageUrls(self):		
		for storeurl in self.storeUrl:
			self.driver.get(storeurl+"/menu")
			self.driver.implicitly_wait(10)
			time.sleep(5) # wait for 5 secondscls
			menuHTMLBody = self.driver.find_element_by_tag_name("body")	
			menuImageUrls  = re.findall(r'\"url\":\"([^\"]+)\"', menuHTMLBody.get_attribute('innerHTML'),re.M|re.I)
			
			for menuImageUrl in menuImageUrls:
				
				menuImageUrl = menuImageUrl.replace("\\", "")
				print ("menuImageUrl--"+menuImageUrl)
				a = urlparse(menuImageUrl)
				fileName = os.path.basename(a.path)
				urllib.request.urlretrieve(menuImageUrl, fileName)
				time.sleep(3) # wait for 3 secondscls

	
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

