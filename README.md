# WeatherSimulator

This script just random select 8-16 random places by latitude and longitude, and provided some mock data for weather. The details of the requirement is on WeatherData.pdf.
It simply random data with common knowledge to make sure the value is at normal weather condition. Add test on https://travis-ci.org/thinksource/WeatherSimulator

## how to run:

This is base on python 3.6

install dependence:
```
pip install -r requirements.txt.
```
Use the google api key.

In config.py file, input your key for Google Maps Geocoding API and Google Maps Elevation API in variable:

```
googlekey="YOUR KEY HERE"
```

And then just run:

```
python main.py
```

## Test:

```
python test.py
```

## Specification & Assumption

1,This name of address only show the "locality","administrative_area_level_2" or "administrative_area_level_1".
It do not show details of address District or Road

2, The output format is

```
|-40.82,130.09,-5541.03|2013-03-17T16:17:12Z|sunny|-5.7|1070.1|41
```

if none place is finding out it will not give the None.

3, about the iso8601 format.

In python the iso 8601 format time should be

YYYY-MM-DDTHH:MM:SS.mmmmmm

```
>>> import datetime
>>> datetime.datetime.utcnow().isoformat()
'2017-08-29T11:46:26.349654'
```

It is obviously different from your document, so I fellow your document time example format instead of iso 8601 format.

```
YYYY-MM-DDTHH:MM:SSZ
```
