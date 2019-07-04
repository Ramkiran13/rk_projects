from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

import requests
import json

# Create your views here.
def index(request):
    # return HttpResponse("Hello, world. You're at the weather app")
    return render(request, 'weatherapp/index.html')

def currentTemp(request):

    latitude = request.GET['Latitude']
    longitude = request.GET['Longitude']

    source = request.GET.getlist('source')

    average_current_temperature = calculate_avg_temp(latitude, longitude, source)


    return render(request, 'weatherapp/currentTemp.html',
    {'latitude':latitude, 'longitude':longitude, 'source':source, 'current_temp':average_current_temperature})

def calculate_avg_temp(lat, long, source):

    temp_celsius = []
    temp_fahrenheit = []

    for source in source:
        if source == 'accuweather':
            output = requests.get('http://127.0.0.1:5000/accuweather?latitude={}&longitude={}'.format(lat, long))
            output_json = output.json()

            current_temp_celsius = int(output_json['simpleforecast']['forecastday'][0]['current']['celsius'])
            current_temp_fahrenheit  = int(output_json['simpleforecast']['forecastday'][0]['current']['fahrenheit'])

            temp_celsius.append(current_temp_celsius)
            temp_fahrenheit.append(current_temp_fahrenheit)

        elif source == 'NOAA':

            output2 = requests.get('http://127.0.0.1:5000/noaa?latlon={},{}'.format(lat, long))
            output_json2 = output2.json()

            current_temp_celsius = int(output_json2['today']['current']['celsius'])
            current_temp_fahrenheit = int(output_json2['today']['current']['fahrenheit'])

            temp_celsius.append(current_temp_celsius)
            temp_fahrenheit.append(current_temp_fahrenheit)

        elif source == 'weatherdotcom':

            # json_data = serializers.deserialize("json", {"lat":lat,"long":long}, ignorenonexistent=True)
            data = {'lat':lat,'lon':long}

            output3 = requests.post(url="http://127.0.0.1:5000/weatherdotcom", json=data)
            print(output3.text)
            output_json3 = output3.json()
            print(output_json3)
            if output_json3['query']['results']['channel']['units']['temperature'] == 'F':
                current_temp_fahrenheit = int(output_json3['query']['results']['channel']['condition']['temp'])
                current_temp_celsius = (current_temp_fahrenheit - 32) * 5/9

                temp_celsius.append(current_temp_celsius)
                temp_fahrenheit.append(current_temp_fahrenheit)
            else:
                current_temp_celsius = int(output_json3['query']['results']['channel']['condition']['temp'])
                current_temp_fahrenheit = (current_temp_celsius + 32) * 9/5

                temp_celsius.append(current_temp_celsius)
                temp_fahrenheit.append(current_temp_fahrenheit)

    print(temp_celsius)
    print(temp_fahrenheit)

    avg_temp_celius = sum(temp_celsius)/len(temp_celsius)
    avg_temp_fahrenheit = sum(temp_fahrenheit)/len(temp_fahrenheit)

    final_output = {"current_temperature_celsius":avg_temp_celius, "current_temperature_fahrenheit":avg_temp_fahrenheit}

    return json.dumps(final_output)
