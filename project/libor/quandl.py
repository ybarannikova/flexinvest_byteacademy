import requests
import json
from getenv import env
import datetime

class Quandl:
    def __init__(self):
        self.libor_url = 'https://www.quandl.com/api/v1/datasets/FED/RILSPDEPM01_N_B.json?auth_token='
        self.api_key = env('QUANDL_API_KEY')


    def get_all_libor_rates_and_dates(self):
        response = requests.get(self.libor_url + self.api_key)
        dates_and_rates = response.json()['data']
        libor_list = []
        for date_and_rate in dates_and_rates:
            rate = float(date_and_rate[1]) * .01
            strfdate = date_and_rate[0]
            date = datetime.date(
                year=int(strfdate[0:4]),
                month=int(strfdate[5:7]),
                day=int(strfdate[8:10])
            )
            libor_list.append({'date':date,'rate':rate})
        return libor_list             


