import json

import random
import time
import os
from datetime import datetime
import math
import requests
import urllib
import config
from myexception import *

def try_except(success, failure, *exceptions):
    try:
        return success() if callable(success) else success
    except Exception:
        return failure() if callable(failure) else failure


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
    return datetime.fromtimestamp(ptime)


def random_date(start, end):
    return str_time_prop(start, end, "%d/%m/%Y", random.random())


def random_temp(lat, conf):
    temp_conf = conf["latitude_temp"]
    if(lat >= 80):
        return random.normalvariate(temp_conf["80"][0],
                                    temp_conf["80"][1]*0.68)
    elif(lat <= -80):
        return random.normalvariate(temp_conf["-80"][0],
                                    temp_conf["-80"][1]*0.68)
    else:
        ceil = math.ceil(lat/10)*10
        floor = math.floor(lat/10)*10
        mean = (temp_conf[str(ceil)][0] * (ceil - lat) +
                temp_conf[str(floor)][0] * (lat - floor))/(ceil - floor)
        sigma = (temp_conf[str(ceil)][1] * (ceil - lat) +
                 temp_conf[str(floor)][1] * (lat - floor))/(ceil - floor)*0.68
        return random.normalvariate(mean, sigma)


def random_pressure(elevation):
    mid = config.mid_pressure
    sigma = config.sigma_pressure
    # on average every 9 meters will reduce 100 Pa
    p = random.normalvariate(mid, sigma) - elevation / 9 * 0.1
    return p


def random_humidity(day):
    humidity = 0
    if(day == "rain" or day == "snow"):
        humidity = random.normalvariate(65, 20)
    elif(day == "cloud"):
        humidity = random.normalvariate(50, 20)
    else:
        humidity = random.normalvariate(30, 20)
    if humidity < 0:
        humidity = 0
    return round(humidity)


def get_address(lat, lng):
    args = {"latlng": str(lat)+","+str(lng), "key": config.googlekey}
    url = "https://maps.googleapis.com/maps/api/geocode/json?{}".\
          format(urllib.parse.urlencode(args))
    try:
        r = requests.get(url)
    except OSError as e:
        raise NetException(e.message, 400)
    rr = ""
    if(r.status_code == 200):
        re = json.loads(r.text)
        if(re["status"] == "ZERO_RESULTS"):
            raise DataFormatError("result is empty")
        if(len(re["results"]) == 0):
            raise DataFormatError("result is empty")
        address = re["results"][0]["address_components"]
        for i in address:
            if "locality" in i["types"] and "political" in i["types"]:
                if any(char.isdigit() for char in i["long_name"]):
                    continue
                return i["long_name"]
            if "administrative_area_level_2" in i["types"]:
                if any(char.isdigit() for char in i["long_name"]):
                    continue
                return i["short_name"]
            if "administrative_area_level_1" in i["types"]:
                rr = i["long_name"]
        return rr
    else:
        raise NetException("http return wrong status", r.status_code)


def get_height(lat, lng):
    args = {"locations": str(lat)+","+str(lng), "key": config.googlekey}
    url = "https://maps.googleapis.com/maps/api/elevation/json?{}".\
          format(urllib.parse.urlencode(args))
    try:
        r = requests.get(url)
        if(r.status_code == 200):
            re = json.loads(r.text)
            if(len(re["results"]) == 0):
                raise DataFormatError("result is empty")
            d = re["results"][0]
            if int(d['elevation']) < 0:
                return 0
            return d['elevation']
        else:
            raise NetException("http return wrong status", r.status_code)
    except OSError as e:
        raise NetException(e.message, 400)
