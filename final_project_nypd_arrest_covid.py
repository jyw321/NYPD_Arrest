# -*- coding: utf-8 -*-


from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np

# %pip install --upgrade --quiet plotly
import plotly.express as px

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import requests


url_2020 = '/content/drive/MyDrive/Colab Notebooks/NYPD_Arrests_Data__2020mar-dec.csv'
df_20 = pd.read_csv(url_2020)
df_20


# modify the arrest date to yyyy-mm-dd format.

df_20['ARREST_DATE'] = pd.to_datetime(df_20['ARREST_DATE'], format='%m/%d/%Y')
df_20


crime_type = df_20.groupby(['LAW_CAT_CD'])
crime_counts_day = crime_type.resample('D', on='ARREST_DATE').size().reset_index(name='day_counts')
crime_counts_day


fig = px.line(crime_counts_day,x='ARREST_DATE',y='day_counts', color='LAW_CAT_CD',title='Arrest Types During Covid by Day 2020')
fig.show()


crime_counts_week_20 = crime_type.resample('W', on='ARREST_DATE').size().stack().reset_index(name='week_counts')
crime_counts_week_20

fig = px.line(crime_counts_week_20,x='ARREST_DATE',y='week_counts', color='LAW_CAT_CD',title='Arrest Types During Covid by Week 2020')
fig.show()



url_2019 = '/content/drive/MyDrive/Colab Notebooks/NYPD_Arrests_Data__2019mar-dec.csv'
df_19 = pd.read_csv(url_2019)
df_19

df_19['ARREST_DATE'] = pd.to_datetime(df_19['ARREST_DATE'], format='%m/%d/%Y')
df_19


crime_type_19 = df_19.groupby(['LAW_CAT_CD'])
crime_counts_week_19 = crime_type_19.resample('W', on='ARREST_DATE').size().reset_index(name='week_counts_19')
crime_counts_week_19



crime_counts_week_20_felony = crime_counts_week_20[crime_counts_week_20['LAW_CAT_CD'] == 'F']
crime_counts_week_20_felony

crime_counts_week_19_felony = crime_counts_week_19[crime_counts_week_19['LAW_CAT_CD'] == 'F']
crime_counts_week_19_felony



crime_counts_comp_felony = crime_counts_week_20_felony.merge(crime_counts_week_19_felony, how='left', left_index=True, right_index=True)
crime_counts_comp_felony = crime_counts_comp_felony.rename(columns={"week_counts": "week_counts_20"})
crime_counts_comp_felony



crime_counts_comp_felony['change_percentage'] = (crime_counts_comp_felony['week_counts_20'] - crime_counts_comp_felony['week_counts_19'])/crime_counts_comp_felony['week_counts_19']*100
crime_counts_comp_felony



crime_counts_comp_felony['time_stamp'] = crime_counts_comp_felony.index
crime_counts_comp_felony

time_stamp = crime_counts_comp_felony['time_stamp']
week_counts_19 = crime_counts_comp_felony['week_counts_19']
week_counts_20 = crime_counts_comp_felony['week_counts_20']

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=time_stamp, y=week_counts_19, name='weekly felony-reasoned arrests 2019'),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=time_stamp, y=week_counts_20, name='weekly felony-reasoned arrests 2020'),
    secondary_y=True,
)

# Add figure title
fig.update_layout(
    title_text='Felony-reasoned Arrest Weekly Count 2019-20 Comparison'
)

# Set x-axis title
fig.update_xaxes(title_text="Week")

# Set y-axes titles
fig.update_yaxes(title_text="weekly felony-reasoned arrests 2019", secondary_y=False)
fig.update_yaxes(title_text="weekly felony-reasoned arrests 2020", secondary_y=True)

fig.show()



df_20_felony = df_20[df_20['LAW_CAT_CD'] == 'F']
df_20_felony

df_20_felony['OFNS_DESC'].unique()



df_20_felony_type = df_20_felony.groupby('OFNS_DESC').size().reset_index(name='counts')
df_20_felony_type.sort_values('counts', ascending=False)



df_20_mis = df_20[df_20['LAW_CAT_CD'] == 'M']
df_20_mis

df_20_mis['OFNS_DESC'].unique()



df_20_mis_type = df_20_mis.groupby('OFNS_DESC').size().reset_index(name='counts')
df_20_mis_type.sort_values('counts', ascending=False)



df_20_felony_race = df_20_felony.groupby(['PERP_RACE']).size()
df_20_felony_race.sort_values(ascending=False)



df_20_mis_race = df_20_mis.groupby(['PERP_RACE']).size()
df_20_mis_race.sort_values(ascending=False)



df_20_felony_sex = df_20_felony.groupby(['PERP_SEX']).size()
df_20_felony_sex.sort_values(ascending=False)

df_20_mis_sex = df_20_mis.groupby(['PERP_SEX']).size()
df_20_mis_sex.sort_values(ascending=False)



df_20_felony_age = df_20_felony.groupby(['AGE_GROUP']).size()
df_20_felony_age.sort_values(ascending=False)

df_20_mis_age = df_20_mis.groupby(['AGE_GROUP']).size()
df_20_mis_age.sort_values(ascending=False)



df_20_felony_boro = df_20_felony.groupby(['ARREST_BORO']).size().reset_index(name='counts')
df_20_felony_boro.sort_values('counts', ascending=False)



df_covid_date = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/covid-data-by-day.csv')
df_covid_date

df_covid_date['date_of_interest'] = pd.to_datetime(df_covid_date['date_of_interest'], format='%m/%d/%Y')
df_covid_date



df_covid_date_2020 = df_covid_date[(df_covid_date['date_of_interest'] > '2020-2-29') & (df_covid_date['date_of_interest'] < '2021-1-1')] 
df_covid_date_2020



df_covid_date_2020_boro = df_covid_date_2020[['date_of_interest', 'BX_CASE_COUNT', 'BK_CASE_COUNT', 'MN_CASE_COUNT', 'QN_CASE_COUNT', 'SI_CASE_COUNT']]
df_covid_date_2020_boro



print(sum(df_covid_date_2020_boro['BX_CASE_COUNT']))
print(sum(df_covid_date_2020_boro['BK_CASE_COUNT']))
print(sum(df_covid_date_2020_boro['MN_CASE_COUNT']))
print(sum(df_covid_date_2020_boro['QN_CASE_COUNT']))
print(sum(df_covid_date_2020_boro['SI_CASE_COUNT']))



print(round((80385/1418207) * 100000)) #Bronx population
print(round((114977/2559903) * 100000)) #Brooklyn population
print(round((55134/1628706) * 100000)) #Manhattan population
print(round((116851/2253858) * 100000)) #Queens population
print(round((32610/476143) * 100000)) #StatenIsland population

# make a dataframe of Covid infection rate in differnet boroughs
d = {'Boro': ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'StatenIsland'], 'Covid Rate': [5668, 4491, 3385, 5184, 6849]}
df_covid_boro = pd.DataFrame(data=d)
df_covid_boro



def boro(row):
  if row.ARREST_BORO == 'K':
    return 'Brooklyn'
  elif row.ARREST_BORO == 'M':
    return 'Manhattan'
  elif row.ARREST_BORO == 'Q':
    return 'Queens'
  elif row.ARREST_BORO == 'B':
    return 'Bronx'
  elif row.ARREST_BORO == 'S':
    return 'StatenIsland'

# add a new column to the NYPD data which contains the full names of the boroughs

df_20_felony_boro['Boro'] = df_20_felony_boro.apply(boro, axis=1)
df_20_felony_boro

# calculate the felony-reasoned arrest rate (arrest per 100,000 population) in different boroughs based on the 2020 NYPD arrest dataset

print(round((11110/1418207) * 100000)) #Bronx population
print(round((15882/2559903) * 100000)) #Brooklyn population
print(round((11568/1628706) * 100000)) #Manhattan population
print(round((11193/2253858) * 100000)) #Queens population
print(round((2334/476143) * 100000)) #StatenIsland population

d = {'Boro': ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'StatenIsland'], 'Arrest Rate': [783,620,710,497,490]}
df_arrest_boro = pd.DataFrame(data=d)
df_arrest_boro



df_20_felony_covid_boro = df_arrest_boro.merge(df_covid_boro, left_on='Boro', right_on='Boro')
df_20_felony_covid_boro



boro = df_20_felony_covid_boro['Boro']
arrest = df_20_felony_covid_boro['Arrest Rate']
covid = df_20_felony_covid_boro['Covid Rate']


fig = go.Figure()
fig.add_trace(go.Bar(x=boro, y=arrest, marker_color='rgb(0,102,204)'))

fig.update_layout(title_text='Felony-reasoned Arrest Rate in NYC Boroughs 2020')
fig.show()



fig = go.Figure()
fig.add_trace(go.Bar(x=boro, y=covid, marker_color='rgb(204,0,102)'))

fig.update_layout(title_text='Covid Infection Rate in NYC Boroughs 2020')
fig.show()



df_20_felony_precinct = df_20_felony.groupby(['ARREST_PRECINCT']).size().reset_index(name='counts')
df_20_felony_precinct.sort_values('counts', ascending=False)



geojson = 'https://data.cityofnewyork.us/api/geospatial/78dh-3ptz?method=export&format=GeoJSON'
response = requests.get(geojson)
response.json()

fig = px.choropleth_mapbox(df_20_felony_precinct,
                           geojson=geojson,
                           locations='ARREST_PRECINCT',
                           featureidkey='properties.precinct',
                           color='counts',
                           color_continuous_scale='oranges',
                           center = {'lat': 40.73, 'lon': -73.98},
                           hover_data=['ARREST_PRECINCT'],
                           zoom=9,
                           mapbox_style='carto-positron', title='Felony-reasoned Arrests by NY Precinct 2020')

fig.update_layout(height=650)
fig.show()



