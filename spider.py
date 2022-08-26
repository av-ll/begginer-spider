from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import unidecode
import h5py
from datetime import date



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

splited_values = splited_values.reshape(1,4)
#url to retrieve temperature for Alabama
url_temp = 'https://www.timeanddate.com/weather/usa/alabama'

response_temperature = requests.get(url_temp,headers)

temp_soup = BeautifulSoup(response_temperature.content)

temp_div = temp_soup.find(class_ = 'h2')

temperature = temp_div.get_text()

temperature = unidecode.unidecode(temperature)

regex_temp = re.findall('\d+',temperature)
regex_temp = [float(a) for a in regex_temp]
regex_temp = np.array(regex_temp)

#url to retrieve daily milk powder price
url_milk = 'https://www.dailydairyreport.com/'


response_milk = requests.get(url_milk,headers)

milk_soup = BeautifulSoup(response_milk.content)

milk_tables = milk_soup.find_all('tr')

milk_tables_data = [a.find_all('td') for a in milk_tables]


milk_data = milk_tables_data[4]

milk_data_value = str(milk_data[1])

milk_data_value

milk_data = re.findall('\d+\.\d+',milk_data_value)

milk_data = [float(a) for a in milk_data]

milk_data = np.array(milk_data)


#append the retrieved data to the hdf5
file = h5py.File('data.h5','a')

file['temperature'].resize((file['temperature'].shape[0]+regex_temp.shape[0]), axis=0)

file['temperature'][-regex_temp.shape[0]:] = regex_temp

file['milk_price'].resize((file['milk_price'].shape[0]+milk_data.shape[0]), axis=0)

file['milk_price'][-milk_data.shape[0]:] = milk_data

file['gas_prices'].resize((file['gas_prices'].shape[0]+splited_values.shape[0]), axis=0)

file['gas_prices'][-splited_values.shape[0]:] = splited_values

date_today = np.array([date.today().strftime("%Y/%m/%d")])

file['date'].resize((file['date'].shape[0]+date_today.shape[0]), axis=0)

file['date'][-date_today.shape[0]:] = date_today


file.close()
