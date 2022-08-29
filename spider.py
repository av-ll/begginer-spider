#!/usr/local/Caskroom/miniconda/base/bin/python3
from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import unidecode
import h5py
from datetime import date



date_today = np.array([date.today().strftime('%Y/%m/%d')])


# link to check gas prices in Alabama
url = 'https://gasprices.aaa.com/?state=AL'

# required headers
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36'}

# get the response
response = requests.get(url,headers=headers)

# get the html with BeautifulSoup
soup = BeautifulSoup(response.content)

#find the element with class ~
table = soup.find(class_ = 'table-mob')

#find all td (which contain numerical data)
table_values = table.find_all('td')

#find all th (which contain the labels of table_values)
table_feature = table.find_all('th')

#get each the text of the th elements
text_feature = [a.getText() for a in table_feature]

text_feature.remove('')

#use a regular expression to find values that correspond
#to amounts in dollars $
regex = re.compile('^\$')

table_values = [a.find(text = regex) for a in table_values]

#split the list of values in order to retrieve only the data for today
splited_values = np.array_split(table_values,table_values.count(None))

splited_values = splited_values[0]

splited_values = splited_values[splited_values != None]

splited_values = [a.replace('$','') for a in splited_values]

splited_values = [float(a) for a in splited_values]

splited_values = np.array(splited_values)

final_gas = splited_values.reshape(1,4)






#url to retrieve temperature for Alabama
url_temp = 'https://www.timeanddate.com/weather/usa/montgomery'

response_temperature = requests.get(url_temp,headers)

temp_soup = BeautifulSoup(response_temperature.content)

temp_div = temp_soup.find(class_ = 'h2')

temperature = temp_div.get_text()

temperature = unidecode.unidecode(temperature)

regex_temp = re.findall('\d+',temperature)
regex_temp = [float(a) for a in regex_temp]
regex_temp = np.array(regex_temp)

temp_humd = temp_soup.find_all('tr')

humidity = [x for x in temp_humd if 'Humidity' in str(x)]

humidity_reg = [re.findall('\d+',str(x)) for x in humidity]

humidity_reg = [humidity_reg[0][0],humidity_reg[1][0],humidity_reg[1][1]]

humidity_reg = np.array(humidity_reg,dtype='float')



range_temp = temp_soup.find_all('span')
range_temp = [x for x in range_temp if 'Forecast' in str(x)]

range_temp =  np.array(re.findall('\d+',str(range_temp)),dtype='float')

final_weather = np.concatenate((regex_temp,range_temp,humidity_reg))

final_weather = final_weather.reshape(1,6)

keys = np.array(('Temperature_now','T_max','T_min','Humidity_now','H_max','H_min'))



#url to retrieve daily milk powder price
url_milk = 'https://www.dailydairyreport.com/'


response_milk = requests.get(url_milk,headers)

milk_soup = BeautifulSoup(response_milk.content)

milk_tables = milk_soup.find_all('td')

milk_keys = ['Butter','Cheddar Block','Cheddar Barrel','Powder Milk','Dry Whey']

milk_info = [x for x in milk_tables if 'Final' in str(x)]
#milk_tables_data = [a.find_all('td') for a in milk_tables]

milk_info = milk_info[:5]

milk_data = [re.findall('\d+\.\d+',str(x)) for x in milk_info]

final_milk = np.array(milk_data,dtype=float).reshape(1,5)


#append the retrieved data to the hdf5
file = h5py.File('data.h5','a')



file['websites/temperature'].resize((file['websites/temperature'].shape[0]+final_weather.shape[0]), axis=0)

file['websites/temperature'][-final_weather.shape[0]:] = final_weather

file['websites/milk_price'].resize((file['websites/milk_price'].shape[0]+final_milk.shape[0]), axis=0)

file['websites/milk_price'][-final_milk.shape[0]:] = final_milk

file['websites/gas_prices'].resize((file['websites/gas_prices'].shape[0]+final_gas.shape[0]), axis=0)

file['websites/gas_prices'][-final_gas.shape[0]:] = final_gas


file['websites/date'].resize((file['websites/date'].shape[0]+date_today.shape[0]), axis=0)

file['websites/date'][-date_today.shape[0]:] = date_today


file.close()
