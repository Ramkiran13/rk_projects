from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

import requests
import json

# Create your views here.
def index(request):
    return render(request, 'weatherapp/index.html')

def currentTemp(request):

    latitude, longitude, source = getLatLongSource(request)

    if validateLatLon(latitude, longitude):
        average_current_temperature = calculateAvgTemp(latitude, longitude, source)
    else:
        # messages.info(request, 'Provide float values to Latitude and Longitude' )
        return HttpResponseRedirect('/')

    return render(request, 'weatherapp/currentTemp.html',
    {'latitude':latitude, 'longitude':longitude, 'source':source, 'current_temp':average_current_temperature})

def getLatLongSource(request):

    lat = request.GET['Latitude']
    long = request.GET['Longitude']
    source = request.GET.getlist('source')

    return lat, long, source

def validateLatLon(lat, long):
    try:
        latitude = float(lat)
        longitude = float(long)
        return True
    except ValueError:
        return False

def calculateAvgTemp(lat, long, source):

    temp_celsius, temp_fahrenheit = getSourceTemp(lat, long, source)

    avg_temp_celius = sum(temp_celsius)/len(temp_celsius)
    avg_temp_fahrenheit = sum(temp_fahrenheit)/len(temp_fahrenheit)

    final_output = {"current_temperature_celsius":avg_temp_celius, "current_temperature_fahrenheit":avg_temp_fahrenheit}

    return json.dumps(final_output)

def getSourceTemp(lat, long, source):
    temp_celsius = []
    temp_fahrenheit = []

    for source in source:
        if source == 'accuweather':
            current_temp_celsius, current_temp_fahrenheit = currentTempAccu(lat, long)
        elif source == 'NOAA':
            current_temp_celsius, current_temp_fahrenheit = currentTempNoaa(lat, long)
        elif source == 'weatherdotcom':
            current_temp_celsius, current_temp_fahrenheit = currentTempWeatherdotcom(lat, long)

        temp_celsius.append(current_temp_celsius)
        temp_fahrenheit.append(current_temp_fahrenheit)

    return temp_celsius, temp_fahrenheit

def currentTempAccu(lat, long):

    output = requests.get('http://127.0.0.1:5000/accuweather?latitude={}&longitude={}'.format(lat, long))
    output_json = output.json()

    current_temp_celsius = int(output_json['simpleforecast']['forecastday'][0]['current']['celsius'])
    current_temp_fahrenheit  = int(output_json['simpleforecast']['forecastday'][0]['current']['fahrenheit'])

    return current_temp_celsius, current_temp_fahrenheit

def currentTempNoaa(lat, long):

    output = requests.get('http://127.0.0.1:5000/noaa?latlon={},{}'.format(lat, long))
    output_json = output.json()

    current_temp_celsius = int(output_json['today']['current']['celsius'])
    current_temp_fahrenheit = int(output_json['today']['current']['fahrenheit'])

    return current_temp_celsius, current_temp_fahrenheit

def currentTempWeatherdotcom(lat, long):

    data = {'lat':lat,'lon':long}

    output = requests.post(url="http://127.0.0.1:5000/weatherdotcom", json=data)

    output_json = output.json()

    if output_json['query']['results']['channel']['units']['temperature'] == 'F':
        current_temp_fahrenheit = int(output_json['query']['results']['channel']['condition']['temp'])
        current_temp_celsius = (current_temp_fahrenheit - 32) * 5/9

    else:
        current_temp_celsius = int(output_json['query']['results']['channel']['condition']['temp'])
        current_temp_fahrenheit = (current_temp_celsius + 32) * 9/5

    return current_temp_celsius, current_temp_fahrenheit
