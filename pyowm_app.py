import pyowm
import requests
import websockets
import asyncio
import os


def weatherapp(message):
    owm = pyowm.OWM('abe1d37c41b622deda8d7c70b6203664')
    cities = ["beijing", "manila", "tokyo", "new york"]
    # while(True):
    #     try:
    #         async for message in websocket:
    for city in cities:
        if(city in message):
            find_city = city
            observation = owm.weather_at_place(find_city)
            w = observation.get_weather()

            if(("temperature" in message)):
                temp = w.get_temperature(unit='celsius')['temp']
                weather = w.get_detailed_status()
                to_send = "The weather forecast for {} today is {}. The current temperature is {} degrees celsius.".format(
                    city,
                    weather,
                    temp
                )
                return(to_send)
            else:
                weather = w.get_detailed_status()
                to_send = "The weather forecast for {} today is {}".format(city, weather)
                return(to_send)

            break

        else:
            pass
        # except websockets.ConnectionClosed:
        #     pass
        # finally:
        #     print("connection removed")
        #     break

# weatherapp("I want to live in manila weather temperature")
