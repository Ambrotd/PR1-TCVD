import requests
from bs4 import BeautifulSoup as bs
import re
import random
import time
import os
from pathlib import Path
from csv import writer
import pandas


def get_headers():
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    ]
    # Pick a random user agent this is only working in case of proxiing
    #user_agent = random.choice(user_agent_list)
    user_agent ='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,es-ES;q=0.8,es;q=0.7",
        "sec-ch-ua": '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": f"{user_agent}"
    }
    return headers


def proxy_pool():
    url = 'https://free-proxy-list.net/'
    r = requests.get(url)
    soup = bs(r.text, 'lxml')
    ip_list = re.findall(r"[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}:[0-9]{2,5}", soup.text)
    return ip_list


def get_proxy():
    proxies = proxy_pool()
    # Just choose from the newest 20
    i = random.randint(0, 20)
    ip_proxy = proxies[i]
    proxies = {"http": f"{ip_proxy}", "https": f"{ip_proxy}"}
    return proxies


def random_time():
    t = random.randint(0, 3)
    time.sleep(t)


def append_csv(fileName, data):
    file = open(f"csv/{fileName}.csv", 'a+', newline='')
    csv_writer = writer(file)
    try:
        csv_writer.writerow(data)
    except:
        print("possible encoding error")


def create_csv(fileName):
    first_row = ['ID', 'Listing', 'Location', 'price','old_price', 'discount', 'meters', 'sq_meter_price', 'rooms', 'floor', 'garage', 'description']
    file_exists = os.path.exists(f"csv/{fileName}.csv")
    if not file_exists:
        myfile = Path(f"csv/{fileName}.csv")
        myfile.touch(exist_ok=True)
        append_csv(fileName, first_row)


def check_csv_list(fileName):
    colNames = ['ID', 'Listing', 'Location', 'price','old_price', 'discount', 'meters', 'sq_meter_price', 'rooms', 'floor', 'garage', 'description']
    data = pandas.read_csv(f"csv/{fileName}.csv", names=colNames, encoding="ISO-8859-1")
    Id_csv = data.ID.tolist()[1:]
    print(Id_csv)
    return Id_csv


def remove_list_duplicates(IdFromIdealista, IdFromCsv):
    return list(set(IdFromIdealista) - set(IdFromCsv))
