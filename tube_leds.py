#!/usr/bin/env python3

import board
import neopixel
import requests
import json
from time import sleep

URL = 'https://api.tfl.gov.uk/line/mode/tube/status'

pixels = neopixel.NeoPixel(board.D18, 50)

stations = [
        ('circle', (255,255,0)),
        ('district', (128,0,0)),
        ('piccadilly', (0,0,128)),
        ('victoria', (128,0,255)),
        ('metropolitan', (0,128,70)),
        ('jubilee', (255,255,255)),
        ('northern', (70,70,70)),
        ('hammersmith-city', (0,255,255)),
        ('bakerloo', (70,255,0)),
        ('waterloo-city', (255,0,128)),
        ('central', (0,255,0))
        ]

status = []

def all_on():
    for i in range(len(stations)):
        pixels[i] = stations[i][1]

def good_on():
    for i in range(len(stations)):
        if is_good(status_for(stations[i][0])):
            pixels[i] = stations[i][1]
        else:
            pixels[i] = (0,0,0)


# Start up
all_on()

def status_for(line):
    try:
        severity = list(filter(lambda i: i['id'] == line, status))[0]['lineStatuses'][0]['statusSeverity']
        return severity
    except:
        return 0


def is_good(severity):
    return severity == 10


def update_status():
    global status
    print('Updating status...')
    response = requests.get(URL)
    if response.status_code == 200:
        status = json.loads(response.text)
        print('Loaded status successfully')
        for i in range(len(stations)):
            print('%s: %s' % (stations[i][0], status_for(stations[i][0])))
    else:
        print('something went wrong loading the status')


while True:
    update_status()
    for n in range(100):
        good_on()
        sleep(0.5)
        all_on()
        sleep(0.5)
