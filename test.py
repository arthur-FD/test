import pandas as pd
import re
import numpy
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import date
from datetime import time
from datetime import datetime
import pycountry
from utils import * 



class ProcessingData: 
    def __init__(self, ev_volume_csv_path=r'/mnt/c/Users/ArthurJacquemart/FIFTHDELTA/Engineering - Documents/Bart/Data/raw/ev_volume/10-31 Upload of PEV Master 2020-10-31.csv'):
        self.ev_volumes_raw=pd.read_csv(ev_volume_csv_path,sep=';',decimal=',')
        self.months_spelled_wrong={'maj':'may','okt':'oct'}
        self.check_formating_months=0
        self.check_col_names=0
        self.clean_data=0
        self.regex_year = r'^20[0-9]{2}$'
        self.regex_month = r'^[a-z]{3}-[0-9]{2}$'
        self.regex_quarter=r'^[0-9]{4}Q[1-4]{1}$'

    def replacing_col_names(self):
        columns=list(self.ev_volumes_raw.columns)
        for i,col in enumerate(columns):
            for weird_month, right_month in self.months_spelled_wrong.items():
                if weird_month in col:
                    columns[i]=col.replace(weird_month,right_month)
        self.ev_volumes_raw.columns=columns
        self.check_formating_months=1

    def drop_unrelevent_row(self):
        if self.check_formating_months==0:
            self.replacing_col_names()
            self.drop_unrelevent_row()
        else:
            self.ev_volumes_raw.replace(' ',numpy.nan,inplace=True)
            self.ev_volumes_raw.dropna(how='all',inplace=True)
            self.clean_data=1
    def colums_names(self):
        if self.clean_data==0:
            self.drop_unrelevent_row()
            self.colums_names()
        else:
            self.years_available=[col for col in elf.ev_volumes_raw.columns if re.search(self.regex_year, col)]
            self.months_available=[col for col in elf.ev_volumes_raw.columns if re.search(self.regex_month, col)]
            self.other_cols=[col  for col in registration_volumes_EV_columns if (col not in years_available and col not in months_available)]
            self.check_col_names=1

                


            
registration_volumes_EV=pd.read_csv(r'/mnt/c/Users/ArthurJacquemart/FIFTHDELTA/Engineering - Documents/Bart/Data/raw/ev_volume/10-31 Upload of PEV Master 2020-10-31.csv',sep=';',decimal=',')

##REPLACE U.K and USA CSQ REP

columns=list(registration_volumes_EV.columns)

weird_months={'maj':'may','okt':'oct'}

for i,col in enumerate(columns):
    for weird_month, right_month in weird_months.items():
        if weird_month in col:
            columns[i]=col.replace(weird_month,right_month)
        
registration_volumes_EV.columns=columns

registration_volumes_EV.replace(' ',numpy.nan,inplace=True) # use regex to make it more robust
registration_volumes_EV.dropna(how='all',inplace=True)

regex_year = r'^20[0-9]{2}$'
regex_month = r'^[a-z]{3}-[0-9]{2}$'
regex_quarter=r'^[0-9]{4}Q[1-4]{1}$'
registration_volumes_EV_columns=list(map(lambda x: x.lower(),list(registration_volumes_EV.columns)))
registration_volumes_EV.columns=registration_volumes_EV_columns
years_available=[col  for col in registration_volumes_EV_columns if re.search(regex_year, col)]
months_available=[col  for col in registration_volumes_EV_columns if re.search(regex_month, col)]
other_cols=[col  for col in registration_volumes_EV_columns if (col not in years_available and col not in months_available)]
#registration_volumes_EV[['sales country','vehicle production country']]=registration_volumes_EV[['sales country','vehicle production country']].applymap(lambda ctry: ctry_preprocessing(ctry.replace('.','')))

import yaml
filename=r'exception_countries.yml'
with open(filename, "r") as f:
    premap_countries=yaml.load(f)

registration_volumes_EV['sales country']=registration_volumes_EV['sales country'].replace(premap_countries)
registration_volumes_EV['vehicle production country']=registration_volumes_EV['vehicle production country'].replace(premap_countries)


list_of_countries=list(set(list(registration_volumes_EV['sales country'])+list(registration_volumes_EV['vehicle production country'])))
dict_country_mapping={}
for country in list_of_countries:
    dict_country_mapping[country]=pycountry.countries.search_fuzzy(country)[0].alpha_2

registration_volumes_EV['SALES_COUNTRY']=registration_volumes_EV['sales country'].replace(dict_country_mapping)
registration_volumes_EV['PROD_COUNTRY']=registration_volumes_EV['vehicle production country'].replace(dict_country_mapping)
registration_volumes_EV_columns+=['SALES_COUNTRY','PROD_COUNTRY']
other_cols=[col  for col in registration_volumes_EV_columns if (col not in years_available and col not in months_available)]

registration_volumes_EV[years_available+months_available]=registration_volumes_EV[years_available+months_available].astype(float)
registration_volumes_EV_columns=list(registration_volumes_EV.columns)


# ##START CHECK###

# ###check on annual data
# print('CHECK ANUAL DATA TO CUM DATA')
# diff_annual_cum=registration_volumes_EV[years_available].sum(axis=1)-registration_volumes_EV['cumulative sales'].fillna(0.0)
# boolean_check_annual_cum=registration_volumes_EV[years_available].sum(axis=1)==registration_volumes_EV['cumulative sales'].fillna(0.0)
# boolean_check_annual_cum=pd.DataFrame(boolean_check_annual_cum,columns=['bool'])
# false_index_annual_cum=boolean_check_annual_cum[boolean_check_annual_cum['bool']==False].index
# diff_annual_cum=pd.DataFrame(diff_annual_cum.loc[false_index_annual_cum].abs().sort_values(ascending=False),columns=['diff'])
# info_false_cum_annual=registration_volumes_EV.loc[false_index_annual_cum][['sales country','oem group','brand','make model']]



# ERRROR_ANNUAL_DF=pd.concat([info_false_cum_annual,diff_annual_cum],axis=1)
# ERRROR_ANNUAL_DF['cummulative_sales']=registration_volumes_EV['cumulative sales'].loc[false_index_annual_cum]
# ERRROR_ANNUAL_DF['cummulative_computed']=registration_volumes_EV[years_available].sum(axis=1).loc[false_index_annual_cum]
# print(ERRROR_ANNUAL_DF.head(20))


# ###check on monthly data
# import pandas as pd
# import openpyxl
# import xlsxwriter
# print('CHECK MONTHLY DATA TO ANNUAL DATA')
# months_to_check=[]
# years_available_with_month=years_available
# registration_volumes_EV.fillna(0,inplace=True)
# sum_by_year={}
# Excelwriter = pd.ExcelWriter("ERROR_BY_YEAR.xlsx",engine="xlsxwriter")
# for year in years_available:
#     if find_col(year[2:],months_available)==[]:
#         years_available_with_month.remove(year)
#     else:
#         months_to_check+=(find_col(year[2:],months_available))
        
#         sum_by_year[year]=pd.DataFrame(registration_volumes_EV[find_col(year[2:],months_available)].sum(axis=1))
#         sum_by_year[year].columns=['sum_computed_'+year]
#         sum_by_year[year]['diff']=sum_by_year[year]['sum_computed_'+year]-registration_volumes_EV[year]
#         sum_by_year[year][year]=registration_volumes_EV[year]
#         info_false_cum_month=registration_volumes_EV.loc[sum_by_year[year].index][['sales country','oem group','brand','make model']]
#         sum_by_year[year]=sum_by_year[year][sum_by_year[year]['diff']!=0]
#         info_false_cum_month=registration_volumes_EV.loc[sum_by_year[year].index][['sales country','oem group','brand','make model']]
#         sum_by_year[year]=pd.concat([info_false_cum_month,sum_by_year[year]],axis=1)
#         sum_by_year[year].to_excel(Excelwriter, sheet_name=year , freeze_panes=(1,1))
# Excelwriter.save()


###END CHECK###

registration_volumes_EV_quarterly=registration_volumes_EV[months_available].applymap(float)
registration_volumes_EV_quarterly.columns=pd.to_datetime(registration_volumes_EV_quarterly.columns,format='%b-%y')
registration_volumes_EV_quarterly=registration_volumes_EV_quarterly.groupby(pd.to_datetime(registration_volumes_EV_quarterly.columns).to_period('Q'),1).sum()
registration_volumes_EV_quarterly.columns=list(registration_volumes_EV_quarterly.columns.map(str))
registration_volumes_EV=pd.concat([registration_volumes_EV,registration_volumes_EV_quarterly],axis=1)
registration_volumes_EV.reset_index(inplace=True)
registration_volumes_EV.drop(['index'],axis=1,inplace=True)
quarter_available=list(registration_volumes_EV_quarterly.columns)
# sales_volumes=[col  for col in registration_volumes_EV_columns if ('sales' in col or 'volumes' in col)]
# registration_volumes_EV.iloc[:100]
spec_cars=[col for col in registration_volumes_EV_columns if (col not in years_available+quarter_available+months_available ) ]


registration_volumes_EV_transformed=registration_volumes_EV.set_index(spec_cars)

registration_volumes_EV_transformed.columns.name='DATE'
registration_volumes_EV_transformed=registration_volumes_EV_transformed.stack()
registration_volumes_EV_transformed.name='VALUE'
registration_volumes_EV_transformed=registration_volumes_EV_transformed.reset_index()
# len(registration_volumes_EV_transformed)==len(registration_volumes_EV_transformed.drop_duplicates())


registration_volumes_EV_transformed['GRANULARITY']=''
registration_volumes_EV_transformed.GRANULARITY[registration_volumes_EV_transformed.DATE.str.contains(regex_year)]='YEAR'
registration_volumes_EV_transformed.GRANULARITY[registration_volumes_EV_transformed.DATE.str.contains(regex_month)]='MONTH'
registration_volumes_EV_transformed.GRANULARITY[registration_volumes_EV_transformed.DATE.str.contains(regex_quarter)]='QUARTER'

registration_volumes_EV_transformed['MODEL_ID']=registration_volumes_EV_transformed['make model']+'/'+registration_volumes_EV_transformed['propulsion']+'/'+registration_volumes_EV_transformed['global segment']+'/'+registration_volumes_EV_transformed['battery kwh']


registration_volumes_EV_transformed_monthly=registration_volumes_EV_transformed[registration_volumes_EV_transformed['GRANULARITY']=='MONTH']
registration_volumes_EV_transformed_monthly.DATE=pd.to_datetime(registration_volumes_EV_transformed_monthly.DATE,format='%b-%y')
registration_volumes_EV_transformed_monthly.DATE=registration_volumes_EV_transformed_monthly.DATE.apply(lambda month_start: date(month_start.year,month_start.month,numberOfDays(month_start.year,month_start.month)))



registration_volumes_EV_transformed_year=registration_volumes_EV_transformed[registration_volumes_EV_transformed['GRANULARITY']=='YEAR']
registration_volumes_EV_transformed_year.DATE=registration_volumes_EV_transformed_year.DATE.apply(lambda year:date(int(year),12,31))

registration_volumes_EV_transformed_quarterly=registration_volumes_EV_transformed[registration_volumes_EV_transformed['GRANULARITY']=='QUARTER']
registration_volumes_EV_transformed_quarterly.DATE=registration_volumes_EV_transformed_quarterly.DATE.apply(lambda quarter: get_last_day_quarter(int(quarter[-1]),int(quarter[:4])))

registration_volumes_EV_transformed=pd.concat([registration_volumes_EV_transformed_quarterly,registration_volumes_EV_transformed_monthly,registration_volumes_EV_transformed_year])

registration_volumes_EV_transformed['FORECAST_RELEASE_DATE']=date.today()



#pycountry.countries.search_fuzzy('England')[0].alpha_2



filename=r'columns_mapping.yml'
with open(filename, "r") as f:
    columns_mapping=yaml.load(f)


tables_to_import={}
for TABLE_NAME, cols_map_TABLE in columns_mapping.items():
    if TABLE_NAME != 'GEO_COUNTRY_TEST':
        temp=registration_volumes_EV_transformed[list(cols_map_TABLE.keys())].copy()
        temp.columns=list(cols_map_TABLE.values())
        print(temp)
        tables_to_import[TABLE_NAME]=temp.drop_duplicates()
        
    else:
        sales_countries=registration_volumes_EV_transformed[['sales region','SALES_COUNTRY']].copy()
        sales_countries.columns=list(cols_map_TABLE.values())
        production_countries=registration_volumes_EV_transformed[['vehicle production region','PROD_COUNTRY']]
        production_countries.columns=list(cols_map_TABLE.values())
        temp=pd.concat([sales_countries,production_countries]).drop_duplicates()
        temp=temp[temp.REGION != 0]
        tables_to_import[TABLE_NAME]=temp
    tables_to_import[TABLE_NAME].to_csv(f'FINAL_CSV/{TABLE_NAME}.csv',index=False)   

#####################################################




#VOLUME CHECK IN THE UK PER BRAND

total_brand_UK=registration_volumes_EV_transformed[(registration_volumes_EV_transformed['sales country']=='UK')  & (registration_volumes_EV_transformed['GRANULARITY']=='MONTH')][['DATE','brand','VALUE']]
total_brand_UK=total_brand_UK.groupby(['brand','DATE']).sum()
total_brand_UK.reset_index(inplace=True)

total_brand_UK.DATE=pd.to_datetime(total_brand_UK.DATE,format='%b-%y')
total_brand_UK.index=total_brand_UK.DATE
total_brand_UK.drop(['DATE'],inplace=True,axis=1)
total_brand_UK.VALUE=total_brand_UK.VALUE.apply(float)

brands=list(set(total_brand_UK.brand))
fig = make_subplots(rows=1,cols=1)
for brand in brands:
    temp=total_brand_UK[total_brand_UK['brand']==brand]
    fig.add_trace(
    go.Scatter(x=temp.index, y=temp.VALUE,name=brand),
    row=1, col=1
    )
fig.update_layout(height=800, width=1500)
fig.show()


#VOLUME CHECK IN THE UK for mercedes

mercedes_UK=registration_volumes_EV_transformed[(registration_volumes_EV_transformed['brand']=='Mercedes-Benz') & (registration_volumes_EV_transformed['GRANULARITY']=='MONTH') & (registration_volumes_EV_transformed['sales country']=='UK') ][['make model','DATE','VALUE']]
mercedes_UK.DATE=pd.to_datetime(mercedes_UK.DATE,format='%b-%y')
mercedes_UK.VALUE=mercedes_UK.VALUE.apply(float)
mercedes_UK.groupby(['make model','DATE']).sum()
mercedes_UK.reset_index(inplace=True)
mercedes_UK.index=mercedes_UK.DATE

mercedes_UK.drop(['DATE','index'],inplace=True,axis=1)

models_mercedes=list(set(mercedes_UK['make model']))
fig = make_subplots(rows=1,cols=1)
for model in models_mercedes:
    temp=mercedes_UK[mercedes_UK['make model']==model]
    fig.add_trace(
    go.Scatter(x=temp.index, y=temp.VALUE,name=model),
    row=1, col=1
    )

fig.update_layout(height=800, width=1500)
fig.show()


#VOLUME CHECK IN THE UK for audi

Audi_UK=registration_volumes_EV_transformed[(registration_volumes_EV_transformed['brand']=='Audi') & (registration_volumes_EV_transformed['GRANULARITY']=='MONTH') & (registration_volumes_EV_transformed['sales country']=='UK') ][['make model','DATE','VALUE']]
Audi_UK.DATE=pd.to_datetime(Audi_UK.DATE,format='%b-%y')
Audi_UK.VALUE=Audi_UK.VALUE.apply(float)
Audi_UK.groupby(['make model','DATE']).sum()
Audi_UK.reset_index(inplace=True)
Audi_UK.index=Audi_UK.DATE

Audi_UK.drop(['DATE','index'],inplace=True,axis=1)

models_Audi=list(set(Audi_UK['make model']))
fig = make_subplots(rows=1,cols=1)
for model in models_Audi:
    temp=Audi_UK[Audi_UK['make model']==model]
    fig.add_trace(
    go.Scatter(x=temp.index, y=temp.VALUE,name=model),
    row=1, col=1
    )

fig.update_layout(height=800, width=1500)
fig.show()

#VOLUME CHECK IN THE UK for Renault

Renault_UK=registration_volumes_EV_transformed[(registration_volumes_EV_transformed['brand']=='Renault') & (registration_volumes_EV_transformed['GRANULARITY']=='MONTH') & (registration_volumes_EV_transformed['sales country']=='UK') ][['make model','DATE','VALUE']]
Renault_UK.DATE=pd.to_datetime(Renault_UK.DATE,format='%b-%y')
Renault_UK.VALUE=Renault_UK.VALUE.apply(float)
Renault_UK.groupby(['make model','DATE']).sum()
Renault_UK.reset_index(inplace=True)
Renault_UK.index=Renault_UK.DATE

Renault_UK.drop(['DATE','index'],inplace=True,axis=1)

models_Renault=list(set(Renault_UK['make model']))
fig = make_subplots(rows=1,cols=1)
for model in models_Renault:
    temp=Renault_UK[Renault_UK['make model']==model]
    fig.add_trace(
    go.Scatter(x=temp.index, y=temp.VALUE,name=model),
    row=1, col=1
    )

fig.update_layout(height=800, width=1500)
fig.show()



audi_A3=registration_volumes_EV_transformed[(registration_volumes_EV_transformed['make model']=='Audi A3 PHEV') & (registration_volumes_EV_transformed['GRANULARITY']=='MONTH') & (registration_volumes_EV_transformed['sales country']=='USA') ]

audi_A3.DATE=pd.to_datetime(audi_A3.DATE,format='%b-%y')
plt.plot(list(audi_A3.DATE),list(audi_A3.VALUE))
plt.show()




fig = make_subplots(rows=12,cols=1)


for i,year in enumerate(years_available):
    temp= audi_A3[(pd.datetime(int(year),1,1)<=audi_A3['DATE']) & (audi_A3['DATE']<pd.datetime(int(year)+1,1,1))]
    fig.add_trace(
    go.Scatter(x=temp.DATE, y=temp.VALUE),
    row=i+1, col=1
    )

fig.update_layout(height=2000, width=800, title_text="Side By Side Subplots")
fig.show()

from functest.utils.config_loader import ConfigLoader
with open("conf/parameter.yml", "r") as file:
    parameters = yaml.load(file, Loader=ConfigLoader)


    
conn = snowflake.connector.connect(
    user=r'PYTHON_TEST',
    password=r'qFPkPD)d4_NHD#w^9^wh',
    account=r'cl19237.west-europe.azure',
    **parameters["snowflake_config"]
)    