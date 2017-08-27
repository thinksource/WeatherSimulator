import json

def readconfig(file):
    with open(file) as jsondata:
        d=json.load(jsondata)
        return d

conf=readconfig("configure.json")

weather=['snow', 'sunny','cloud','rain']
mid_pressure=1013.25
sigma_pressure=12
