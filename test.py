import pandas as pd
import re
import numpy
import matplotlib.pyplot as plt

registration_volumes_EV=pd.read_csv(r'10-31 Upload of PEV Master 2020-10-31.csv',sep=';')
registration_volumes_EV.replace(' ',numpy.nan,inplace=True) # use regex to make it more robust
registration_volumes_EV.dropna(how='all',inplace=True)

regex_year = r'^20[0-9]{2}$'
regex_month = r'^[a-z]{3}-[0-9]{2}$'

registration_volumes_EV_columns=list(map(lambda x: x.lower(),list(registration_volumes_EV.columns)))
registration_volumes_EV.columns=registration_volumes_EV_columns


years_available=[col  for col in registration_volumes_EV_columns if re.search(regex_year, col)]
months_available=[col  for col in registration_volumes_EV_columns if re.search(regex_month, col)]
# sales_volumes=[col  for col in registration_volumes_EV_columns if ('sales' in col or 'volumes' in col)]

spec_cars=[col for col in registration_volumes_EV_columns if (col not in years_available and col not in months_available ) ]

registration_volumes_EV_transformed=registration_volumes_EV.set_index(spec_cars)

registration_volumes_EV_transformed.columns.name='DATE'
registration_volumes_EV_transformed=registration_volumes_EV_transformed.stack()
registration_volumes_EV_transformed.name='VALUE'
registration_volumes_EV_transformed=registration_volumes_EV_transformed.reset_index()

registration_volumes_EV_transformed['GRANULARITY']=''
registration_volumes_EV_transformed.GRANULARITY[registration_volumes_EV_transformed.DATE.str.contains(regex_year)]='YEAR'
registration_volumes_EV_transformed.GRANULARITY[registration_volumes_EV_transformed.DATE.str.contains(regex_month)]='MONTH'

# check if cumulative data is matching the sum of monthly/annual

test=registration_volumes_EV_transformed[(registration_volumes_EV_transformed['make model']=='Audi A3 PHEV') & (registration_volumes_EV_transformed['GRANULARITY']=='YEAR') & (registration_volumes_EV_transformed['sales country']=='USA') ]
plt.plot(list(test.DATE),list(test.VALUE))
plt.show()