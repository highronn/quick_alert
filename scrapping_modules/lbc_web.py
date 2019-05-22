#!/usr/bin/python3
# coding: utf-8

import requests
import json
import time
from datetime import datetime

from models import dev_db

from peewee import (
    CharField,
    TextField,
    DateTimeField,
    BigIntegerField,
    BooleanField,
    IntegerField,
    DecimalField,
    IntegrityError,
    Model,
    MySQLDatabase
)

quick_alert_db = MySQLDatabase(
    'quickalert',
    user='quickalert',
    password='quickalert',
    host='myquickalertdbinstance.cqlkfxu7awoj.eu-west-3.rds.amazonaws.com',
    port=3306
)

db = dev_db
#db = quick_alert_db

API_ENDPOINT = "https://api.leboncoin.fr/finder/search"
API_KEY = 'ba0c2dad52b3ec'

AD_REQUIRED_FIELDS = {
    'id': BigIntegerField(null=False),
    'pub_date': DateTimeField(null=False, default=datetime.now),
    'exp_date': DateTimeField(null=True),
    'status': CharField(null=True, default=None),
    'category_id': CharField(null=True, default=None),
    'category_name': CharField(null=True, default=None),
    'subject': CharField(null=True, default=None),
    'body': TextField(null=True, default=None),
    'ad_type': CharField(null=True, default=None),
    'url': CharField(null=True, default=None),
    'price': IntegerField(null=True, default=None),
    'price_calendar': CharField(null=True, default=None),
    'nb_images': CharField(null=True, default=None),
    'real_estate_type': CharField(null=True, default=None),
    'custom_ref': CharField(null=True, default=None),
    'ges': CharField(null=True, default=None),
    'lease_type': CharField(null=True, default=None),
    'rooms': IntegerField(null=True, default=None),
    'immo_sell_type': CharField(null=True, default=None),
    'fai_included': CharField(null=True, default=None),
    'square': IntegerField(null=True, default=None),
    'is_import': CharField(null=True, default=None),
    'pro_rates_link': CharField(null=True, default=None),
    'energy_rate': CharField(null=True, default=None),
    'location_region_id': CharField(null=True, default=None),
    'location_region_name': CharField(null=True, default=None),
    'location_department_id': CharField(null=True, default=None),
    'location_department_name': CharField(null=True, default=None),
    'location_city': CharField(null=True, default=None),
    'location_zipcode': CharField(null=True, default=None),
    'location_lat': DecimalField(null=True, default=None),
    'location_lng': DecimalField(null=True, default=None),
    'location_source': CharField(null=True, default=None),
    'location_provider': CharField(null=True, default=None),
    'location_is_shape': CharField(null=True, default=None),
    'owner_store_id': CharField(null=True, default=None),
    'owner_user_id': CharField(null=True, default=None),
    'owner_type': CharField(null=True, default=None),
    'owner_name': CharField(null=True, default=None),
    'owner_no_salesmen': CharField(null=True, default=None),
    'opt_has_option': CharField(null=True, default=None),
    'opt_booster': CharField(null=True, default=None),
    'opt_photosup': CharField(null=True, default=None),
    'opt_urgent': CharField(null=True, default=None),
    'opt_gallery': CharField(null=True, default=None),
    'opt_sub_toplist': CharField(null=True, default=None),
    'has_phone': CharField(null=True, default=None),
}

class AdLBC(Model):
    class Meta:
        database = db
        db_table = 't_lbc_buffer_in'
        primary_key = False


def init_models():
    for name, typ in AD_REQUIRED_FIELDS.items():
        AdLBC._meta.add_field(name, typ)

    AdLBC.create_table(safe=True)


def search(parameters):
    wait_time = max(parameters.get("wait_time", 0), 0) / 1000.0

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
    #response = requests.post(url=API_ENDPOINT, data=json.dumps(payload), headers=headers)
    #json_response = response.json()

    with open("data/test/lbc.json") as json_file:
        json_response = json.load(json_file)

    attributes_set = set()

    for ad in json_response.get('ads', []):
        id = ad['list_id']
        print("ad {}".format(id))
        fields = {
            'id': id,
            'pub_date': ad['first_publication_date'],
            'exp_date' : ad.get('expiration_date'),
            'status' : ad['status'],
            'category_id' : ad['category_id'],
            'category_name' : ad['category_name'],
            'subject' : ad['subject'],
            'body' : ad['body'],
            'ad_type' : ad['ad_type'],
            'url' : ad['url'],
            'price' : ad['price'][0],
            'price_calendar' : ad['price_calendar'],
            'nb_images' : ad['images']['nb_images']
        }

        for atts in ad.get('attributes', []):
            key = atts['key']
            value = atts['value']
            attributes_set.add(key)
            fields[key] = value

        location = ad['location']
        fields['location_region_id'] = location['region_id']
        fields['location_region_name'] = location['region_name']
        fields['location_department_id'] = location['department_id']
        fields['location_department_name'] = location['department_name']
        fields['location_city'] = location['city']
        fields['location_zipcode'] = location['zipcode']
        fields['location_lat'] = location['lat']
        fields['location_lng'] = location['lng']
        fields['location_source'] = location['source']
        fields['location_provider'] = location['provider']
        fields['location_is_shape'] = location['is_shape']

        owner = ad['owner']
        fields['owner_store_id'] = owner['store_id']
        fields['owner_user_id'] = owner['user_id']
        fields['owner_type'] = owner['type']
        fields['owner_name'] = owner['name']
        fields['owner_no_salesmen'] = owner['no_salesmen']

        options = ad['options']
        fields['opt_has_option'] = options['has_option']
        fields['opt_booster'] = options['booster']
        fields['opt_photosup'] = options['photosup']
        fields['opt_urgent'] = options['urgent']
        fields['opt_gallery'] = options['gallery']
        fields['opt_sub_toplist'] = options['sub_toplist']

        fields['has_phone'] = ad['has_phone']

        try:
            ad_model = AdLBC.create(**fields)
            # ad_model.save()
        except IntegrityError as error:
            logging.info("ERROR: " + str(error))

        time.sleep(wait_time)
