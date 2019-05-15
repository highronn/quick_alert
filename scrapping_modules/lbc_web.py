#!/usr/bin/python3
# coding: utf-8

import requests
import json

API_ENDPOINT = "https://api.leboncoin.fr/finder/search"
API_KEY = 'ba0c2dad52b3ec'


def search(params):
    payload = {
        "filters": {
            "category": {"id": "9"},
            "enums": {
                "ad_type": ["offer"],
                "real_estate_type": ["1", "5"]
            },
            "keywords": {},
            "location": {
                "city_zipcodes": [
                    {
                        "locationType": "city",
                        "city": "Roubaix",
                        "zipcode": "59100",
                        "label": "Roubaix (59100)"}
                ],
                "regions": ["17"]
            },
            "ranges": {
                "price": {"max": 200000},
                "square": {"min": 80}
            }
        },
        "limit": 35,
        "limit_alu": 3
    }
    headers = {'content-type': 'application/json', 'api-key': API_KEY}

    # sending post request and saving response as response object
    response = requests.post(url=API_ENDPOINT, data=json.dumps(payload), headers=headers)
    ads = response.json()

