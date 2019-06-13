#Packages used in this program
import SeleniumLibrary
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

#All the xpath used in the file.
loginbutton = "//button[@id='SignIn']"
username = "//input[@id='username']"
password = "//input[@id='loginPassword']"
UN = "xxxxxxx"
PW = "xxxxxxx"
rstab = "//a[@id='Search-RecentSearches']"
listpaper = "//div[@class='modal-header ng-scope']"
listselected = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/select[1]/option[22]" #Change the number in option[] to select the list. 
applysearch = "//button[@id='Search-RecentSearches-ApplyButton']"
mapbutton = "//button[@class='btn btn-primary view-map-btn ng-binding']"
companybutton = "//button[@id='Search-Results-Companies']"
#updatecom = "/html[1]/body[1]/div[1]/div[1]/div[1]/span[1]/ng-include[1]/div[1]/div[1]/form[1]/div[2]/label[1]"
updatecom = "/html[1]/body[1]/div[1]/div[1]/div[1]/span[1]/ng-include[1]/div[1]/div[1]/form[1]/div[2]/label[1]/input[1]"
#uploadnewcom = "/html[1]/body[1]/div[1]/div[1]/div[1]/span[1]/ng-include[1]/div[1]/div[1]/form[1]/div[1]/label[1]"
uploadnewcom = "/html[1]/body[1]/div[1]/div[1]/div[1]/span[1]/ng-include[1]/div[1]/div[1]/form[1]/div[1]/label[1]/input[1]"
resultbody = "/html[1]/body[1]/section[1]/section[1]/article[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[3]"
uploadbutton = "//a[@class='btn btn-primary upload-upload-btn ng-binding ng-scope']"
cancelbutton = "//a[@class='btn btn-default upload-cancel-btn']"
uppapertext = "//th[contains(text(),'DiscoverOrg')]"
nextpage = "//a[contains(text(),'Next')]"

#Chrome is used here.
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://go.discoverydb.com/eui/#/login")

#Login process
def loginpage(username,password,UN,PW):
    loginpage = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, loginbutton)))
    uninput = driver.find_element_by_xpath(username)
    uninput.send_keys(UN)
    pwinput = driver.find_element_by_xpath(password)
    pwinput.send_keys(PW)
    loginpage.click()
    time.sleep(5)
    
loginpage(username,password,UN,PW)

#Open 'result search'
changetab = WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH, rstab)))
time.sleep(5)
changetab.click()

#Choose the destinated search result in the list.
selectsr = WebDriverWait(driver,20).until(ec.visibility_of_element_located((By.XPATH,listpaper)))
time.sleep(2)
targetsr = driver.find_element_by_xpath(listselected)
targetsr.location_once_scrolled_into_view
targetsr.click()

#Apply the search result
asbutton = driver.find_element_by_xpath(applysearch)
asbutton.click()
time.sleep(3)

#Show all the companies in the selected search result.
companys = WebDriverWait(driver,10).until(ec.visibility_of_element_located((By.XPATH,companybutton)))
companys = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,companybutton)))
companys.click()
tablebody = WebDriverWait(driver,30).until(ec.visibility_of_element_located((By.XPATH,mapbutton)))

#Record all the companies need an upload action, as well as the companies updated
comlist = []
updatelist = []

#Find the total number of pages (100 per page)
comnum = driver.find_element_by_xpath("//a[@id='Search-ActiveCriteria']//span[@class='badge ng-binding']").text
comnum = int(comnum)
rnum = int(comnum//100)

#Create a function to update the 100 companies in current page one by one.
def cloudshow(i):
    cloud = "/html[1]/body[1]/section[1]/section[1]/article[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[%i]/div[1]/div[1]/div[1]/div[1]/i[3]"%i
    cloudbutton = WebDriverWait(driver,60).until(ec.visibility_of_element_located((By.XPATH,cloud)))
    cloudbutton = driver.find_element_by_xpath(cloud)
    driver.execute_script("window.scrollBy(0,30)")
    cloudbt = WebDriverWait(driver,60).until(ec.element_to_be_clickable((By.XPATH, cloud)))
    return cloud,cloudbt

def updaterecordbypage(pagenum):
    for i in range(1,101):
        rbody = WebDriverWait(driver,60).until(ec.visibility_of_element_located((By.XPATH,resultbody)))
        cloud,cloudbt = cloudshow(i)
        
        try:
            cloudbuttonon = cloudbt#show(cloud)
        except NoSuchElementException or StaleElementReferenceException:
            time.sleep(10)
            cloudbutton = WebDriverWait(driver,60).until(ec.element_to_be_clickable((By.XPATH, cloud)))
            cloudbutton = cloudbt#show(cloud)
            
        try:
            cloudbt.click()
        except ElementClickInterceptedException:
            time.sleep(10)
            cloudbt = WebDriverWait(driver,60).until(ec.element_to_be_clickable((By.XPATH, cloud)))
            cloudbt.click()
            
        uploadcom = WebDriverWait(driver,60).until(ec.visibility_of_element_located((By.XPATH,uploadnewcom)))
        updatepage = driver.find_element_by_xpath(updatecom)
        uploadcomname = driver.find_element_by_xpath("//label[contains(text(),'Upload New Company')]").text
        
        try:
            #updatebt = WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, updatecom)))
            updatepage.click()
            updatelist.append(str(uploadcomname))
            updateshow = WebDriverWait(driver,60).until(ec.element_to_be_clickable((By.XPATH, cloud)))
            time.sleep(2)
        except ElementNotVisibleException:
            comlist.append(str(uploadcomname))
            time.sleep(2)
            
        targetbt = driver.find_element_by_xpath(uploadbutton)
        targetbt.location_once_scrolled_into_view  
        dis_data = targetbt.get_attribute('disabled')
        
        if dis_data is None:
            is_clickable = True
        else:
            is_clickable = False
            
        if is_clickable == False:
            tarcancel = driver.find_element_by_xpath(cancelbutton)
            tarcancel.click()
        else:
            targetbt.click()
        time.sleep(2)
        
    pagenum = driver.find_element_by_xpath("//li[@class='pagination-page ng-scope active']").text
    return comlist,updatelist
    
#Turn to the next page and use the function to update companies in current page.
for i in range(1,rnum):
    try: 
        newpage = WebDriverWait(driver,30).until(ec.visibility_of_element_located((By.XPATH,companybutton)))
        uploadlist,updatelist = updaterecordbypage(i)
        time.sleep(5)
        nextbutton = driver.find_element_by_xpath(nextpage)
        driver.execute_script("return arguments[0].scrollIntoView(true);", nextbutton)
        nextbutton = WebDriverWait(driver,30).until(ec.element_to_be_clickable((By.XPATH,nextpage)))
        nextbutton.click()
        pagenum = driver.find_element_by_xpath("//li[@class='pagination-page ng-scope active']").text
        p = int(pagenum)
        print("Checking %ith page"%p)
        dis_next = nextbutton.get_attribute('disabled')
        
        if dis_next is None:
            is_clickable = True
        else:
            is_clickable = False
            
        if is_clickable == False:
            print("Last page")
            break
        time.sleep(2)
        
    except TimeoutException or ElementClickInterceptedException:
        print("Get stuck on page %i"%p)
        break 

#Print out all the companies need a upload action. Check them manully.
print(uploadlist)
print(updatelist)
        
