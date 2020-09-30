#Importing Necessary libraries.
# NOTE: We could use EC.wait_until methods, for simplicity, I have gone with sleep method.
#You can increase or decrease parameter of sleep depending on your bandwidth so as to ensure, page loads up before scraping data.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd

#Starting the driver.
PATH = "C:\Program Files (x86)\chromedriver.exe"
opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
driver = webdriver.Chrome(PATH, options= opt)
driver.get("https://www.tripadvisor.com/")
sleep(3)

#Selecting and clicking on Hotels.
try:
    hotels = driver.find_element_by_xpath('//*[@id="lithium-root"]/main/div[1]/div[1]/div/div/div[1]/a')
    hotels.click()
except:
    sleep(2)
    hotels = driver.find_element_by_xpath('//*[@id="lithium-root"]/main/div[1]/div[1]/div/div/div[1]/a')
    hotels.click()
sleep(5)
#Searching for New Delhi Hotels.
try:
    search = driver.find_element_by_xpath('/html/body/div[4]/div/form/input[1]')
    search.send_keys("New Delhi")
    sleep(2)
    search.send_keys(Keys.ENTER)
    print("This worked")
except:
    search = search = driver.find_element_by_xpath('/html/body/div[3]/div/form/input[1]')
    search.send_keys("New Delhi")
    sleep(2)
    search.send_keys(Keys.ENTER)
    print("Exception worked")

sleep(10)
#Initializing Lists to store required Data
hotelnametext = []
amenities = []
priceval = []
imagelinks = []
ratings = []

#Scraping Data from Homepage
hotelnames = driver.find_elements_by_class_name("listing_title")
amen = driver.find_elements_by_class_name("icons_list.easyClear.vertical")
price2 = driver.find_elements_by_class_name("price-wrap ")
reviews = driver.find_elements_by_class_name("ui_bubble_rating")

#Formatting data and storing them in appropriate lists
for i in range(len(hotelnames)):
        hotelnametext.append(hotelnames[i].text)
        price = price2[i].text
        if "\n" in price:
            idx = price.index("\n")
            price = price[idx+1:]
        priceval.append(price)
        ratings.append(reviews[i+1].get_attribute('alt'))


for i in range(0,len(amen),2):
        amenities.append(amen[i].text.replace("\n", "+"))

#print("before loop")
#print(len(hotelnames), len(price2), len(amen), len(reviews))
pagenums = driver.find_element_by_xpath('//*[@id="taplc_main_pagination_bar_dusty_hotels_resp_0"]/div/div/div/div/a[7]')
pagenums = pagenums.text

#Scraping data from 20 pages. We could change the argument to however many pages we want,
for i in range(1,20):
    url = "https://www.tripadvisor.com/Hotels-g304551-" + "oa"+str(30*i)+"-New_Delhi_National_Capital_Territory_of_Delhi-Hotels.html"
    driver.get(url)
    sleep(13)
    try:
        hotelnames = driver.find_elements_by_class_name("listing_title")
    except:
        sleep(5)
        hotelnames = driver.find_elements_by_class_name("listing_title")
    try:
        amen = driver.find_elements_by_class_name("icons_list.easyClear.vertical")
    except:
        sleep(5)
        amen = driver.find_elements_by_class_name("icons_list.easyClear.vertical")
    try:
        price2 = driver.find_elements_by_class_name("price-wrap ")
    except:
        sleep(5)
        price2 = driver.find_elements_by_class_name("price-wrap ")
    try:
        reviews = driver.find_elements_by_class_name("ui_bubble_rating")
    except:
        sleep(5)
        reviews = driver.find_elements_by_class_name("ui_bubble_rating")

    #Formatting Data and storing it.
    for i in range(len(hotelnames)):
        hotelnametext.append(hotelnames[i].text)
        price = price2[i].text
        if "\n" in price:
            idx = price.index("\n")
            price = price[idx+1:]
        priceval.append(price)
        ratings.append(reviews[i+1].get_attribute('alt'))
    for i in range(0,len(amen),2):
        amenities.append(amen[i].text.replace("\n", "+"))


#print(len(hotelnametext), len(priceval), len(amenities), len(ratings))

driver.close()
#Creating a dictionary object to pass in as an argument for creating a Pandas Dataframe.
di = {
    'Hotel Name': hotelnametext,
    'Price' : priceval,
    'Amenities': amenities,
    'Reviews' : ratings,
}
#Converting scraped data as a DataFrame using Pandas.
df = pd.DataFrame(di)
#Converting the dataframe to a csv file using Pandas.
df.to_csv('hoteldata.csv', sep = '\t')
