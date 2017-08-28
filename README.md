# WeatherSimulator


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


```
python main.py
```

## Test:

```
python test.py
```

## Specification

1,This name of adddress only show the "locality","administrative_area_level_2" or "administrative_area_level_1".
It do not show details of address District or Road
