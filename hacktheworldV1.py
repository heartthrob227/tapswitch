from twilio.rest import TwilioRestClient
import pandas as pd
import requests
import datetime
# from datetime import date
# from datetime import timedelta
# from datetime import datetime
import csv
from collections import defaultdict
barexternalid = input('What is the bar external id? ')


count = 0
beer_brands = []

with open('runout.csv', encoding='Latin1') as consumption_data:
    runout_data = pd.read_csv(consumption_data)
    external_id_given = str(barexternalid);
    beer_brands = runout_data.loc[runout_data['external_id']==39524 , 'brand_name']

#print(beer_brands)

with open('brands-ps.csv', encoding='Latin1') as brand_data:
    rating_data = pd.read_csv(brand_data)
    for i in beer_brands:
        rating_data.loc[rating_data['brand_name'] == i , 'priority_score' ] = rating_data['priority_score']+1
        rating_data.to_csv("brands-ps.csv",index=False)

def weather():
    with open('lineexternallocation.csv', encoding='Latin1') as external_id_file:
        external_id_data = pd.read_csv(external_id_file)
        #print(external_id_data)
        external_id_variable = int(barexternalid)
        #print (external_id_variable)
        latitude_value = external_id_data.loc[external_id_data['external_id']==external_id_variable , 'Latitude']
        #print (latitude_value)
        longitude_value = external_id_data.loc[external_id_data['external_id']==external_id_variable , 'Longitude']

    latitude = latitude_value[0] #insert the variable of latitude here
    longitude = longitude_value[0] #insert the variable for longitude here

    url = "http://api.openweathermap.org/data/2.5/forecast/daily?lat="+str(latitude)+"&lon="+str(longitude)+"&cnt=16&APPID=d341df03ce08fb4cfd9b8a352264cdca"

    response = requests.get(url)

    response_geology = response.json()
    list_of_data = response_geology['list']
    today_date = date.today()

    for i in list_of_data:
        print("Date:" , today_date.strftime("%A %d. %B %Y"))
        print("Temperature:")
        print(i['temp'])
        print("Pressure:" , i['pressure'])
        print("Humidity:" , i['humidity'])
        weather_exact = i['weather']
        print("Weather:")
        for j in weather_exact:
            print("Status:" ,j['main'])
            print("Description:" , j['description'])

        print("Speed:" , i['speed'])
        print("Degree:" , i['deg'])
        print("Cloud:" , i['speed'])
        today_date = today_date + timedelta(days=1)

def trigger():
    with open('brands-ps.csv') as priorityfile:
        df = pd.read_csv(priorityfile)
        df['priority_score'] = df['priority_score'].astype(str).convert_objects(convert_numeric=True)
        main_list = df[(df['priority_score']>0)]
        sortedlist = main_list.sort('priority_score', ascending=False)
        #print(sortedlist)
        beerlist = sortedlist['brand_name'].values.tolist()
        #print(beerlist)
        indexes = [0,1,2,3,4]
        beer = [beerlist[x] for x in indexes]
        print (beer)
        beers = '\n'.join(map(str, beer))
        #twilio info
        ACCOUNT_SID = "AC9bd9aba5122b22735f866d5e366bd73d"
        AUTH_TOKEN = "40b7f03ac9dfcc9fdb8960df2f7fbe66"
        #Write the text
        textmessage = "We noticed you're running low on beer! \nHere are our recommended beers to restock: \n%s\nText 'Reorder' to place your refill with the beers above!" % (beers)
        #print (textmessage)
        client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

        client.messages.create(
            to="+12012070322",
            from_="+16466062468",
            body=textmessage,
            )

def flags():
    with open('lineexternallocation.csv', encoding='Latin1') as qfile:
        df1 = pd.read_csv(qfile)
    with open('Draught Table2.csv') as file:
        df = pd.read_csv(file)
        df['serve_ends1']= pd.to_datetime(df['serve_ends'])
        df['serve_ends2'] = df['serve_ends1'].dt.date
        print(df)
        date = datetime.date(2017,3,20)
        print (date)
        dt = df[df['serve_ends2'] == date]
        print(dt)
        merged = pd.merge(dt, df1, on ='line_id', how='left')
        print (merged)
        aggconsump = merged.groupby(['serve_ends2','external_id','brand_name'])['consumption'].sum()
        print (aggconsump)
        aggdf = aggconsump.to_frame()
        print (aggdf)
        reorder = aggdf[(aggdf['consumption'] > 10)]
        print(reorder)
        runout = reorder.astype(int)
        runout.to_csv('runout.csv')
flags()
#weather()
trigger()
