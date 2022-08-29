import h5py

file = h5py.File('data.h5','w')

dt = h5py.special_dtype(vlen=str)

group = file.create_group('websites')

dataset1 = file['websites'].create_dataset('gas_prices',(0,4),maxshape=(None,4),dtype='float')

dataset2 = file['websites'].create_dataset('temperature',(0,6),maxshape=(None,6),dtype='float')

dataset3 = file['websites'].create_dataset('milk_price',(0,5),maxshape=(None,5),dtype='float')

dataset4 = file['websites'].create_dataset('date',(0,1),maxshape=(None,1),dtype=dt)

dataset1.attrs['info'] = 'Used to store daily gas prices in Alabama'

dataset1.attrs['columns'] = 'The values in each column correspond to : Regular, Mid-Grade, Premium, Diesel'

dataset2.attrs['info'] = 'Used to store recorded temperature and Humidity in Alabama daily'

dataset2.attrs['columns'] = 'The values in each column correspond to : Temperature now, Maximum Temperature forecast, Minimum Temperature forecast, Humidity, Afternoon Humidity, Evening Humidity'

dataset3.attrs['info'] = 'Used to store daily powdered milk derivatives prices in the USA'

dataset3.attrs['columns'] = 'The values in each column correspond to prices of : Butter, Cheddar Block, Cheddar Barrel, Powdered Milk (NDM Grade A), Dry Whey'

dataset4.attrs['info'] = 'Used to store the date'

file.close()
