from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import pyfiglet
class color:
   BOLD = '\033[1m'
   END = '\033[0m'

#print intro using pyfiglet
print(pyfiglet.figlet_format("a way home"))
print(color.BOLD + "Weclome to Hong Kong transfer flight searcher" + color.END)


#Selenium setup
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)

total_price_list = []
while True:
  #--------------Flight from London to Hongkong--------------
  
  #url information
  url_UK_HK = f"https://www.cn.kayak.com/flights/STN%2CEDI%2CMAN-HKG/2022-10-01?sort=bestflight_a&fs=legdur=-1440;stops=-2"
  
  #change url based on input date
  date = input("\nwhat date would you like to search: ")
  url_UK_HK = url_UK_HK.replace('2022-10-01', date)
  
  # Load selenium webdriver with the url
  driver.get(url_UK_HK)
  
  # Give some time for the browser to load the content
  time.sleep(3)
  soup = BeautifulSoup(driver.page_source, 'lxml')
  results = soup.find(class_="resultsContainer")
  
  #get the time section information
  time_infos = results.find_all("div", class_="section times")
  
  #create empty lists for depature, arrival time and depature airport
  departure_time_list = []
  departure_airport_list = []
  arrival_time_list = []
  i = 0 
  
  #Get all departure, arrival time and departure airport and store them in corresponding lists
  for time_info in time_infos:
    depart_time = time_info.find("span", class_="depart-time base-time")
    arrival_time = time_info.find("span", class_="arrival-time base-time")
    depart_airport = time_info.find("span", class_= "airport-name")
    depart_time_text = depart_time.getText().strip()
    arrival_time_text = arrival_time.getText().strip()
    depart_airport_text = depart_airport.getText().strip()
    departure_time_list.insert(i,depart_time_text)
    arrival_time_list.insert(i,arrival_time_text)
    departure_airport_list.insert(i,depart_airport_text)
    i += 1
  
  #get the duration information
  duration_infos = results.find_all("div", class_="section duration allow-multi-modal-icons")
  
  #create an empty list for duration
  duration_time_list = []
  i = 0
  
  #Get all durations and store them in the list
  for duration_info in duration_infos:
    duration_time = duration_info.find("div", class_="top")
    duration_time_text = duration_time.getText().strip()
    duration_time_list.insert(i,duration_time_text)
    i += 1
    
  #get the price information
  price_infos = results.find_all("div", class_="multibook-dropdown")
  
  #create an empty list for price
  price_list = []
  i = 0
  
  #Get all prices and store them in a list
  for price_info in price_infos:
    price = price_info.find("span", class_="price-text")
    price_text = price.getText().strip()
    price_list.insert(i,int(re.search(r'\d+', price_text).group()))
    i += 1
    
  #create an empty list for dictionary
  dictionary_list = [{} for sub in range(len(price_list))]
  
  #create dictionary for each flight and add them into the list
  for i in range(0,len(price_list)):
    flight = dict()
    flight['departure airport'] = departure_airport_list[i]
    flight['departure'] = departure_time_list[i]
    flight['arrival'] = arrival_time_list[i]
    flight['duration'] = duration_time_list[i]
    flight['price'] = price_list[i]
    dictionary_list[i] = flight
  
  min_price1 = price_list[0]
  
  #find out the min price
  for i in range(0,len(price_list)):
    if min_price1 > price_list[i]:
      min_price1 = price_list[i]
  
  #obtain the flight information with the cheapest price
  best_choice1  = next(x for x in dictionary_list if x["price"] == min_price1)
  print(best_choice1)
  
  # # #--------------Quarantine Hotel --------------
  #url of 4 star hotel
  url_HK_Hotel_4star = f"https://all.accor.com/ssr/app/accor/rates/3562/index.zh.shtml?dateIn=2022-10-01&nights=7&compositions=1&stayplus=false&snu=false&utm_campaign=hotel_website_search&utm_medium=accor_regional_websites&_ga=2.170505312.1175302382.1659296769-1060047970.1659296769&utm_source=hotelwebsite_3562"
  
  #url of 5 star hotel
  url_HK_Hotel_5star = f"https://www.mandarinoriental.com/reservations/rooms?hotel=556&language=en-GB&arrive=2022-10-01&depart=2022-10-08&rooms=1&adults=1"
  
  #input checkin, checkout date and hotel preference
  checkin_date = input("\nPlease confirm your check-in date for quarantine: ")
  checkout_date = input("Please confirm your check-out date(7 days after check-in): ")
  Hotel_choice = input("please choose your preferred hotel level(4 or 5): ")
  
  #open and scrape different website based on hotel preference
  if Hotel_choice == '4':
    Hotel_Name = "Novotel Hong Kong Century"
    #modify url information based on the checkin date
    url_Hotel_HK_4star = url_HK_Hotel_4star.replace('2022-10-01', checkin_date)
    # Load selenium webdriver with the url
    driver.get(url_HK_Hotel_4star)
    time.sleep(3)
    soup1 = BeautifulSoup(driver.page_source, 'lxml')
    hotel_prices = soup1.find_all("div", class_= "rate-details__price-wrapper")
  
    #obtain hotel prices from website
    room_price_list = []
    i = 0
    for hotel_price in hotel_prices:
      room_price = hotel_price.find("span", class_="booking-price__number")
      room_price_text = room_price.getText().strip()
      room_price_list.insert(i,int(room_price_text))
      i += 1
  
    #find out the min price
    min_price_room = room_price_list[0]
    for i in range(0,len(room_price_list)):
      if min_price_room > room_price_list[i]:
        min_price_room = room_price_list[i]
  
    #change the price from EUR to CNY 
    int_price_CNY = min_price_room * 6.86
    
  elif Hotel_choice == "5":
    Hotel_Name = "The Landmark Mandarin Oriental, Hong Kong"
    #modify url information based on the checkin and checkout date
    url_Hotel_HK_5star = url_HK_Hotel_5star.replace('2022-10-01', checkin_date)
    url_Hotel_HK_5star = url_HK_Hotel_5star.replace('2022-10-08', checkout_date)
    # Load selenium webdriver with the url
    driver.get(url_HK_Hotel_5star)
    time.sleep(3)
    soup1 = BeautifulSoup(driver.page_source, 'lxml')
  
    #find out the price
    hotel_prices = soup1.find(class_= "room-total")
    hotel_prices_text = hotel_prices.getText().strip()
    #obtain int from string element
    int_price = ''.join(x for x in hotel_prices_text if x.isdigit())
  
    #change the price from HKD to CNY 
    int_price_CNY = float(int_price) * 0.86
    
  
  #--------------Flight from HK TO CHN --------------
  #url information
  url_HK_CHN = f"https://www.cn.kayak.com/flights/HKG-CTU,PVG,PEK/2022-10-08?sort=bestflight_a&fs=legdur=-480"
  
  #change url based on checkout date
  url_HK_CHN = url_HK_CHN.replace('2022-10-08', checkout_date)
  
  
  # Load selenium webdriver with the url
  driver.get(url_HK_CHN)
  
  # Give some time for the browser to load the content
  time.sleep(3)
  soup2 = BeautifulSoup(driver.page_source, 'lxml')
  
  results2 = soup2.find(class_="resultsContainer")
  
  #get information from section times
  time_infos2 = results2.find_all("div", class_="section times")
  
  
  #create empty lists for depature, arrival time and arrival airport 
  departure_time_list2 = []
  arrival_time_list2 = []
  arrival_airport_list2 = []
  i = 0 
  
  #Get all departure, arrival time and arrival airports and store them in the lists
  for time_info in time_infos2:
    depart_time = time_info.find("span", class_="depart-time base-time")
    arrival_time = time_info.find("span", class_="arrival-time base-time")
    arrival_airport = time_info.find_all("span", class_="airport-name")
    depart_time_text = depart_time.getText().strip()
    arrival_time_text = arrival_time.getText().strip()
    #locate the right arrival airport information
    arrival_airport_text = arrival_airport[1].getText().strip()
    departure_time_list2.insert(i,depart_time_text)
    arrival_time_list2.insert(i,arrival_time_text)
    arrival_airport_list2.insert(i,arrival_airport_text)
    i += 1
  
  
  #get the duration information
  duration_infos2 = results2.find_all("div", class_="section duration allow-multi-modal-icons")
  
  #create an empty list for duration
  duration_time_list2 = []
  i = 0
  
  #Get all durations and store them in a list
  for duration_info in duration_infos2:
    duration_time = duration_info.find("div", class_="top")
    duration_time_text = duration_time.getText().strip()
    duration_time_list2.insert(i,duration_time_text)
    i += 1
  
  #get the price information
  price_infos2 = results2.find_all("div", class_="multibook-dropdown")
  #print(price_infos)
  
  #create an empty list for price
  price_list2 = []
  i = 0
  
  #Get all prices and store them in a list
  for price_info in price_infos2:
    price = price_info.find("span", class_="price-text")
    price_text = price.getText().strip()
    price_list2.insert(i,int(re.search(r'\d+', price_text).group()))
    i += 1
  
  
  #create an empty list for dictionary
  dictionary_list = [{} for sub in range(len(price_list2))]
  
  #create dictionary for each flight and add them into the list   
  for i in range(0,len(price_list2)):
    flight = dict()
    flight['arrival airport'] = arrival_airport_list2[i]
    flight['departure'] = departure_time_list2[i]
    flight['arrival'] = arrival_time_list2[i]
    flight['duration'] = duration_time_list2[i]
    flight['price'] = price_list2[i]
    dictionary_list[i] = flight
  
  #find out the min price
  min_price2 = price_list2[0]
  for i in range(0,len(price_list2)):
    if min_price2 > price_list2[i]:
      min_price2 = price_list2[i]
  
  #obtain the flight information with the cheapest price
  best_choice2  = next(x for x in dictionary_list if x["price"] == min_price2)
  
  
  #--------------SUMMARY-----------------
  
  #calculate the total expense
  total_expense = min_price1 + min_price2 + int_price_CNY
  
  #print ITINERARY
  print("\n-------------------------------------------------------------YOUR ITINERARY-------------------------------------------------------------")
  print("\n")
  print(best_choice1)
  print("\n")
  print(best_choice2)
  
  print("\nQuarantine Hotel: " + Hotel_Name + "\nCheck in date: " + checkin_date  + "\nCheck out date: " + checkout_date + "\nHotel Expense: "+ str(int_price_CNY) + " CNY")
  
  print(color.BOLD + "\nTotal Expense: "+ str(total_expense) + " CNY" + color.END)

  best_choice = dict()
  best_choice["date"] = date
  best_choice["price"] = str(total_expense)
  total_price_list.append(best_choice)

  question_final = input("would you like to search for another day(yes or no)~ ")
  if question_final == "no":
    break
driver.quit()
print(total_price_list)
  



  
