import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
file = h5py.File('data.h5','r')

temperature = np.array(file['websites/temperature'])

date = np.array(file['websites/date'])

date = re.findall('\d\d\d\d/\d\d/\d\d',str(date))

gas =  np.array(file['websites/gas_prices'])

milk = np.array(file['websites/milk_price'])

t = pd.DataFrame(temperature,columns =['temperature_now','predicted_max','predict_min','humidity_now','humidity_afternoon','humidity_evening'],index=date)

m = pd.DataFrame(milk,columns=['Butter','Cheddar_Block','Cheddar_Barrel','NDM_Grade_A(powder_milk)','Dry_Whey'],index=date)

g = pd.DataFrame(gas,columns=['Regular','Mid-Grade','Premium','Diesel'],index=date)



fig1, (ax1,ax2,ax3,ax4) = plt.subplots(4)
fig1.suptitle('Gas prices')
fig1.set_figheight(15)
fig1.set_figwidth(8)
ax1.plot(g['Regular'],color='black')
ax2.plot(g['Diesel'],color='turquoise')
ax3.plot(g['Premium'],color = 'olive')
ax4.plot(g['Mid-Grade'],color ='cyan')
ax1.title.set_text('Regular')
ax2.title.set_text('Diesel')
ax3.title.set_text('Premium')
ax4.title.set_text('Mid-Grade')
fig1.savefig('gas.png')



fig1, (ax1,ax2) = plt.subplots(1,2)
ax1.plot(t['humidity_afternoon'],label='humidity_afternoon',color='powderblue')
ax1.plot(t['humidity_evening'],label='humidity_evening',color='cadetblue')
ax1.plot(t['humidity_now'],label='humidity_morning',color='dodgerblue')
ax1.grid()
ax1.title.set_text('Humidity')
plt.setp(ax1,yticks=np.arange(0, 100, step=10))
ax2.plot(t['predicted_max'],label='Predicted Max_temperature',color='tomato')
ax2.plot(t['predict_min'],label='Predicted Min_temperature',color='lightsalmon')
ax2.plot(t['temperature_now'],label='Temperature_Now',color='lime')
ax2.grid()
ax2.title.set_text('Temperature')
plt.setp(ax2,yticks=np.arange(15,35,step=2))
fig1.set_figwidth(25)
fig1.set_figheight(8)
fig1.suptitle('Humidity and Temperature')
ax1.legend()
ax2.legend()
fig1.savefig('temperature.png')

fig1, (ax1,ax2,ax3) = plt.subplots(3)
fig1.suptitle('Milk and Cheese')
fig1.set_figheight(15)
fig1.set_figwidth(8)
ax1.plot(m['NDM_Grade_A(powder_milk)'],label = 'Powder_Milk',color='black')
ax2.plot(m['Cheddar_Block'],label='Cheddar',color='turquoise')
ax3.plot(m['Butter'],label='Butter',color = 'olive')
ax1.title.set_text('Powder_Milk')
ax2.title.set_text('Cheddar')
ax3.title.set_text('Butter')
fig1.savefig('milk.png')



file.close()
