import json
import requests
import time
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY='<insert_api_key_here>'

@app.route('/')
def index():
    background, style, message = setParams()
    return render_template('index.html', background=background, style=style, message=message)

#funstion to set parameters
def setParams():
    weather = getWeather()
    background, style = getBackground(weather)
    condition = weather['weather'][0]['description']
    message = "Looks like it's " + condition + " outside"
    return background, style, message

#get users city from IP address and return weather
def getWeather():
    try:
        ip_address = request.headers['x-appengine-user-ip']
        url = f'http://ip-api.com/json/{ip_address}'
        location = requests.get(url, verify=False).json()
        city = location['city']
    except Exception as e:
        print(e)
        city='london'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    weather = requests.get(url, verify=False).json()
    return weather

#get current time in seconds
def getCurrentTime():
    now = round(time.time())
    return now

#return background image based on time of day
def getBackground(weather):
    sunrise = weather['sys']['sunrise']
    sunset = weather['sys']['sunset']
    startSunset = sunset - 3600
    endSunset = sunset + 3600
    now = getCurrentTime()
    condition = weather['weather'][0]['main']
    if (now < sunrise):
        background = 'https://storage.googleapis.com/apportunity.appspot.com/night_spain.jpeg'
        day = False
    elif (now > sunrise and now < startSunset):
        background = weatherPic(condition)
        day = True
    elif (now > startSunset and now < endSunset):
        background = sunsetPic(condition)
        day = True
    elif (now > endSunset):
        background = 'https://storage.googleapis.com/apportunity.appspot.com/night_spain.jpeg'
        day = False
    style = setStyle(day)
    return background, style

#retrin sunset image based on weather
def sunsetPic(condition):
    if (condition == 'Clear'):
        background = 'https://storage.googleapis.com/apportunity.appspot.com/sunset_burma.jpg'
    elif (condition == 'Clouds'):
        background = 'https://storage.googleapis.com/apportunity.appspot.com/sunset_england.jpg'
    else:
        background = 'https://storage.googleapis.com/apportunity.appspot.com/sunset_burma.jpg'
    return background

#return daytime image based on weather
def weatherPic(condition):
    if (condition == 'Clear'):
        background = 'https://storage.googleapis.com/apportunity.appspot.com/sun_spain.JPG'
    elif (condition == 'Clouds'):
        background = 'https://storage.googleapis.com/apportunity.appspot.com/clouds_london.jpg'
    elif (condition == 'Rain'):
        background = 'https://storage.googleapis.com/apportunity.appspot.com/sun_spain.JPG'
    elif (condition == 'Drizzle'):
        background = 'https://storage.googleapis.com/apportunity.appspot.com/sun_spain.JPG'
    elif (condition == 'Snow'):
        background = 'https://storage.googleapis.com/apportunity.appspot.com/sun_spain.JPG'
    elif (condition == 'Thunderstorm'):
        background = 'https://storage.googleapis.com/apportunity.appspot.com/sun_spain.JPG'
    else:
        background = 'https://storage.googleapis.com/apportunity.appspot.com/sun_spain.JPG'
    return background

#fucntion to get style
def setStyle(day):
    if (day == True):
        style = ['grey lighten-5','grey lighten-3']
    else:
        style = ['grey darken-4','black']
    return style

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
