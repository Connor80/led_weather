# -*- encoding: utf-8 -*-
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import argparse
import json
import requests
import os
import time
from PIL import Image
from utils_weather import get_font, get_file

apikey = config.apikey
city = config.city

class WeatherRenderer:

    def __init__(self, matrix, canvas):
        self.matrix = matrix
        self.canvas = canvas
        self.font = get_font()
    
    def render(self):
        try:
            data = requests.get('https://api.darksky.net/forecast/' + apikey + '/' + city).json()
        except Exception:
            time.sleep(1)
            data = requests.get('https://api.darksky.net/forecast/' + apikey + '/' + city).json()

        alerts = []
        try: 
            alert_title = data['alerts']
            for i in range(len(alert_title)):
                alerts.append(data['alerts'][i]['title'])
            alerts_formatted = "".join(alerts)
        except KeyError:
            alerts_formatted = ""
        try:
            currently_summary = data['currently']['summary']
            currently_temperature = data['currently']['temperature']
            currently_icon = data['currently']['icon']
        except:
            currently_summary = ""
            currently_temperature = ""
            currently_icon = ""
        try:
            minutely_summary = data['minutely']['summary']
        except:
            minutely_summary = ""
        try:
            hourly_summary = data['hourly']['summary']
        except:
            hourly_summary = ""
        weather_str = str("Currently it is " + currently_summary + ". " + minutely_summary + "  " + hourly_summary + alerts_formatted)#alert_description)
        current_temp = str(int(round(currently_temperature)))
      
        text_color = graphics.Color(255, 235, 59)
        image_file = get_file('Assets/' + currently_icon + '.png')
        image = Image.open(image_file)

        image.thumbnail((15, 15), Image.ANTIALIAS)
        pos = self.canvas.width
        pos_1 = self.canvas.width
        start = time.time()
      
        while True:
            self.canvas.Fill(7, 14, 25)
            graphics.DrawText(self.canvas, self.font, 1, 8, text_color, current_temp + "°".decode("utf8"))
            self.matrix.SetImage(image.convert('RGB'), 17, 0)
        
            l = graphics.DrawText(self.canvas, self.font, pos, 25, text_color, weather_str)
            pos -= 1
            if (pos + l < 0):
                pos = self.canvas.width
            time.sleep(0.05)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
        return