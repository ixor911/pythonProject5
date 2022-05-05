from binance_ixor import *
from binance.spot import Spot
from big_snapper_indicator import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import Flask, request, abort
import requests
import socket


#socket.getaddrinfo('https://webhook.site/0fa5de5f-3c6f-4075-9d5a-e9736706a002', port=8080)











app = Flask(__name__, static_host='webhook.site', host_matching=True)

@app.route('/9c7bd5a9-8f2c-42aa-a497-f33fe41c14a3', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print("Data received from Webhook is: ", request.json)
        return "Webhook received!"

app.get(host='webhook.site/9c7bd5a9-8f2c-42aa-a497-f33fe41c14a3')

api_key = "4bRqCMlCkjxLoIfAT6NBwFHG15VtbmJ1WtI1JZgb0E3tfRasJjSPi12icZotddV5"
secret_key = "WYnoEo1mIhAQWqzpXSqAEXVeEXsVSv3iQc08yACFUAuCrh7vRGwgpYzwy50UHeCl"
spot = Spot(api_key, secret_key)

frame = get_init_df("BTC")
