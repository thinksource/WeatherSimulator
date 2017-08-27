import json
import argparse
import pandas as pd
import random, time
import os
from datetime import datetime
import math
import requests
from scipy import misc
import urllib


def str_time_prop(start, end, format, prop):
    '''Get a time at a proportion of a range of two formatted times.
    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    '''
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    # print(ptime)
    # return time.strftime(format, time.localtime(ptime))
    return datetime.fromtimestamp(ptime).strftime('%Y-%m-%dT%H:%M:%SZ')

def random_date(start, end):
    return str_time_prop(start, end, "%d/%m/%Y", random.random())

def readconfig(file):
    with open(file) as jsondata:
        d=json.load(jsondata)
        return d

def random_temp(lat, conf):
    temp_conf=conf["longitude_temp"]
    if(lat>=80):
        return random.normalvariate(temp_conf["80"][0],temp_conf["80"][1]*0.68)
    elif(lat<=80):
        return random.normalvariate(temp_conf["-80"][0],temp_conf["-80"][1]*0.68)
    else:
        ceil=math.ceil(lat/10)*10
        floor=math.floor(lat/10)*10
        mu=(temp_conf[str(ceil)][0]*(ceil-lat)+temp_conf[str(floor)][0]*(lat-ceil))/(ceil-floor)
        sigma=(temp_conf[str(ceil)][1]*(ceil-lat)+temp_conf[str(floor)][1]*(lat-ceil))/(ceil-floor)*0.68
        return random.normalvariate(mu, sigma)


def random_pressure(elevation):
    mid=1013.25
    sigma=12
    # on average every 9 meters will reduce 100 Pa
    p=random.normalvariate(mid,sigma)-elevation/9*0.1
    return p

def random_humidity(day):
    humidity=0
    if(day==weather[0] or day==weather[-1]):
        humidity=random.normalvariate(65, 20)
    elif(day=="cloud"):
        humidity=random.normalvariate(50,20)
    else:
        humidity=random.normalvariate(30,20)
    if humidity<0:
        humidity=0
    return int(humidity)

def isint(value):
  try:
    int(value)
    return True
  except:
    return False

def get_address(lat, lng):
    args={"latlng":str(lat)+","+str(lng),"key":googlekey}
    url="https://maps.googleapis.com/maps/api/geocode/json?{}".format(urllib.parse.urlencode(args))
    r=requests.get(url)
    #print(str(lat)+","+str(lng))
    if(r.status_code==200):
        re=json.loads(r.text)
        if(re["status"]=="ZERO_RESULTS"):
            return ""
        if(len(re["results"])==0):
            return ""
        address=re["results"][0]["address_components"]
        for i in address:
            if "administrative_area_level_1" in i["types"]:
                return i["long_name"]
        return ""
    else:
        return ""

def get_height(lat, lng):
    args={"locations": str(lat)+","+str(lng),"key":googlekey}
    url="https://maps.googleapis.com/maps/api/elevation/json?{}".format(urllib.parse.urlencode(args))
    r=requests.get(url)
    if(r.status_code==200):
        re=json.loads(r.text)
        d=re["results"][0]
        return d['elevation']
    return 0
# '%Y-%m-%d'
weather=['snow', 'sunny','cloud','rain']
t_format="%d/%m/%Y"
start_time="11/06/2006"
end_time="11/08/2017"
# random.seed(os.)
if __name__ == '__main__':

    conf=readconfig("configure.json")
    #cities=pd.read_csv(conf["city_file"])
    re=[]
    #shape=cities.shape
    for i in range(10):
        item=[]
        humidity=0
        lat=float(format(random.uniform(-90,90),'.2f'))
        lng=float(format(random.uniform(-180,180),'.2f'))
        ele=float(format(get_height(lat,lng),'.2f'))
        address=get_address(lat,lng)
        item.append(address)
        item.append([lat,lng,ele])
        date=random_date(conf["start_time"], conf["end_time"])
        # temperture on summer every 100 meters above will reduce 0.6 degree，while in winter every 100 meters will reduce 0.36 degree
        # so on average is reduce 0.48 degree on every 100 meteres
        temperture=random_temp(lat,conf)-ele/100*0.48
        day=""
        # temperture below -10 degree will just snow
        # temperture between 5 to 10 degree will have all weather
        # temperture over 5 degree will not snow
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
        location=str(lat)+","+str(lng)+","+str(ele)
        print("|".join(map(str,[address,location,date,day,tstr,pressure,humidity])))
