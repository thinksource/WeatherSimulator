import json

import random, time
from datetime import datetime
from utility import *
import config


weather=config.weather
conf=config.conf
def generate_place(lat, lng):
    re={}
    humidity=0

    ele=float(format(get_height(lat,lng),'.2f'))
    re["address"]=get_address(lat,lng)
    date=random_date(config.conf["start_time"], config.conf["end_time"]).strftime('%Y-%m-%dT%H:%M:%SZ')
    # temperture on summer every 100 meters above will reduce 0.6 degree，while in winter every 100 meters will reduce 0.36 degree
    # so on average is reduce 0.48 degree on every 100 meteres
    if(ele>=0):
        temperture=random_temp(lat,conf)-ele/100*0.48
    else:
        temperture=random_temp(lat,conf)
    day=""
    # temperture below -10 degree will just snow
    # temperture between -10 to 5 degree will have all weather
    # temperture over 5 degree will only have rain
    if(temperture<-10):
        day=weather[random.randrange(len(weather)-1)]
    elif(temperture<5):
        day=weather[random.randrange(len(weather))]
    else:
        day=weather[random.randrange(1, len(weather))]

    pressure=format(random_pressure(ele),'.1f')
    humidity=random_humidity(day)
    if(temperture>=0):
        tstr="+"+format(temperture,'.1f')
    else:
        tstr=format(temperture,'.1f')
    re["location"]=str(lat)+","+str(lng)+","+str(ele)
    re["date"]=date
    re["day"]=day
    re["temperture"]=tstr
    re["pressure"]=pressure
    re["humidity"]=humidity
    return re

if __name__ == '__main__':
    re=[]
    conf=config.conf
    weather=config.weather
    for i in range(random.randrange(8,16)):
        lat=float(format(random.uniform(-90,90),'.2f'))
        lng=float(format(random.uniform(-180,180),'.2f'))
        print("|".join(map(str,generate_place(lat, lng).values())))
