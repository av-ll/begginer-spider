import h5py

file = h5py.File('data.h5','w')

dt = h5py.special_dtype(vlen=str)

dataset1 = file.create_dataset('gas_prices',(0,4),maxshape=(None,4),dtype='float')

dataset2 = file.create_dataset('temperature',(0,1),maxshape=(None,1),dtype='float')

dataset3 = file.create_dataset('milk_price',(0,1),maxshape=(None,1),dtype='float')

dataset4 = file.create_dataset('date',(0,1),maxshape=(None,1),dtype=dt)

dataset1.attrs['info'] = '''Used to store daily gas prices in Alabama
the columns correspond to Regular, Mid-Grade, Premium and Diesel respectively '''

dataset2.attrs['info'] = 'Used to store recorded temperature in Alabama daily'

dataset3.attrs['info'] = 'Used to store daily powdered milk prices in the USA'

dataset4.attrs['info'] = 'Used to store the date'

file.close()
