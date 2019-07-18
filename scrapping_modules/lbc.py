#!/usr/bin/python3
# coding: utf-8

import requests
import json
import time
import os
import logging
from datetime import datetime
from models import dev_db
from dateutil.relativedelta import relativedelta
from urllib.parse import unquote, urlencode
import sys
from fake_useragent import UserAgent
import random
from peewee import (
    CharField,
    TextField,
    DateTimeField,
    BigIntegerField,
    BooleanField,
    IntegerField,
    DecimalField,
    IntegrityError,
    OperationalError,
    Model,
    MySQLDatabase
)

AD_REQUIRED_FIELDS = {
    'list_id': IntegerField(null=False),
    'first_publication_date': DateTimeField(null=False, default=datetime.now),
    'expiration_date': DateTimeField(null=True),
    'index_date': DateTimeField(null=True),
    'status': CharField(null=True, default=None),
    'category_id': IntegerField(null=True, default=None),
    'category_name': CharField(null=True, default=None),
    'subject': CharField(null=True, default=None),
    'ad_type': CharField(null=True, default=None),
    'price': IntegerField(null=True, default=None),
    'price_calendar': CharField(null=True, default=None),
    'nb_images': IntegerField(null=True, default=None),
    'real_estate_type': IntegerField(null=True, default=None),
    'custom_ref': CharField(null=True, default=None),
    'ges': CharField(null=True, default=None),
    'lease_type': CharField(null=True, default=None),
    'rooms': IntegerField(null=True, default=None),
    'immo_sell_type': CharField(null=True, default=None),
    'fai_included': CharField(null=True, default=None),
    'square': IntegerField(null=True, default=None),
    'is_import': BooleanField(null=True, default=None),
    'energy_rate': CharField(null=True, default=None),
    'location_region_id': IntegerField(null=True, default=None),
    'location_region_name': CharField(null=True, default=None),
    'location_department_id': IntegerField(null=True, default=None),
    'location_department_name': CharField(null=True, default=None),
    'location_city_label': CharField(null=True, default=None),
    'location_city': CharField(null=True, default=None),
    'location_zipcode': CharField(null=True, default=None),
    'location_lat': DecimalField(decimal_places=6, max_digits=9,null=True, default=None),
    'location_lng': DecimalField(decimal_places=6, max_digits=9,null=True, default=None),
    'location_source': CharField(null=True, default=None),
    'location_provider': CharField(null=True, default=None),
    'location_is_shape': BooleanField(null=True, default=None),
    'owner_store_id': IntegerField(null=True, default=None),
    'owner_user_id': CharField(null=True, default=None),
    'owner_type': CharField(null=True, default=None),
    'owner_name': CharField(null=True, default=None),
    'owner_no_salesmen': BooleanField(null=True, default=None),
    'owner_siren': CharField(null=True, default=None),
    #'owner_pro_rates_link': CharField(null=True, default=None),
    'opt_has_option': BooleanField(null=True, default=None),
    'opt_booster': BooleanField(null=True, default=None),
    'opt_photosup': BooleanField(null=True, default=None),
    'opt_urgent': BooleanField(null=True, default=None),
    'opt_gallery': BooleanField(null=True, default=None),
    'opt_sub_toplist': BooleanField(null=True, default=None),
    'has_phone': BooleanField(null=True, default=None),
    'pro_rates_link': CharField(null=True, default=None),
    'url': CharField(null=True, default=None),
    'body': TextField(null=True, default=None)
}

""" is_dev_db = (os.environ.get("QUICKALERT_DEV", "0") != 0)
db = dev_db if is_dev_db else MySQLDatabase(
    'quickalert',
    user='quickalert',
    password='quickalert',
    host='myquickalertdbinstance.cqlkfxu7awoj.eu-west-3.rds.amazonaws.com',
    port=3306
) """

db = quick_alert_db = MySQLDatabase(
    'quickalert',
    user='quickalert',
    password='quickalert',
    host='myquickalertdbinstance.cqlkfxu7awoj.eu-west-3.rds.amazonaws.com',
    port=3306
)

API_ENDPOINT = "https://api.leboncoin.fr/finder/search"
API_KEY = 'ba0c2dad52b3ec'

###########################################################################################

class AdLBC(Model):
    class Meta:
        database = db
        db_table = 't_lbc_ads_buffer_in'
        primary_key = False


class AdBatchTable(Model):
    class Meta:
        database = db
        db_table = 't_batch_info'

    id = CharField(unique=True, primary_key=True)
    limit_date = DateTimeField(null=False)
    cp = DateTimeField(null=False)
    ad_type = CharField(null=False)
    thread = IntegerField(null=False)

class AdBatchView(Model):
    class Meta:
        database = db
        db_table = 'v_batch_run_lbc'

    id = CharField(unique=True, primary_key=True)
    cp = DateTimeField(null=False)
    ad_type = CharField(null=False)

def init_models():
    for name, typ in AD_REQUIRED_FIELDS.items():
        AdLBC._meta.add_field(name, typ)
    AdLBC.create_table(safe=True)


def search(parameters,ThreadId):
    for i in range(0,10):
        ####################################################################
        ##  RECUPERATION IDENTIFIANT DU BATCH A TRAITER
        ####################################################################
        try :
            BatchView = AdBatchView.get()
            config_id = BatchView.id
            #print("{} - Thread {} Starting...".format(config_id, ThreadId))
            #print(BatchView.id)
            #print(config_id)
        except :
            print("No Batch to run")
            return -1

        ####################################################################
        ##  CHECK SI BATCH UNLOCK
        ####################################################################
        try :
            #print("{} - Thread {} Starting 2...".format(config_id, ThreadId))
            BatchTable = AdBatchTable.get(AdBatchTable.id == config_id)
            if BatchTable.thread == 0 :
                #print("{} - Thread {} batch unlocked 3...".format(config_id, ThreadId))
                pass
            else :
                #print("{} - Thread {} Check 1 : Batch already locked !      {}/{}".format(config_id, ThreadId,BatchTable.thread ,ThreadId ))
                continue
        except :
            print("Error to get batch table info")
            continue

        ####################################################################
        ##  LOCK DU BATCH
        ####################################################################
        try :
            #print("{} - Thread {} trying to get lock...".format(config_id, ThreadId))
            AdBatchTable.update( thread=ThreadId).where(AdBatchTable.id == config_id , AdBatchTable.thread == "0" ).execute()
            BatchTable = AdBatchTable.get(AdBatchTable.id == config_id)
            #time.sleep(1/ThreadId)
            if BatchTable.thread == ThreadId :
                #print("{} - Thread {} batch locked successfully...".format(config_id, ThreadId))
                break
            else :
                #print("{} - Thread {} Check 2 : Batch already locked !      {}/{}".format(config_id, ThreadId,BatchTable.thread ,ThreadId ))
                continue
        except :
            print("{} - Thread {} Database Error - Unable to get lock !".format(config_id, ThreadId))
            continue
    else :
        return

    ####################################################################
    ##  PARAMETRAGE DU JSON & URL
    ####################################################################
    parameters['config_id'] = BatchTable.id
    parameters["lbc_web"]["filters"]['location']["city_zipcodes"][0]["zipcode"] = BatchTable.cp
    parameters["lbc_web"]["filters"]["category"]["id"] = BatchTable.ad_type
    payload = parameters["lbc_web"]
    config_id = parameters['config_id']
    start_date_script = (datetime.now()+ relativedelta(minutes=-0)).strftime('%Y-%m-%d %H:%M:00')

    headers = {'content-type': 'application/json', 'api-key': API_KEY}

    try:
        config = AdBatchTable.get(AdBatchTable.id == config_id)
        limit_date = config.limit_date.strftime('%Y-%m-%d %H:%M:%S')
        print("{} - Thread {} batch locked successfully : {}".format(config_id, ThreadId,limit_date))
        #print("     {} - using limit date : {}".format(config_id,limit_date))
    except Exception:
        print("     {} - no config found for. no limit date will be used".format(config_id))
        limit_date = None
    ####################################################################

    # sending post request and saving response as response object
    response = requests.post(url=API_ENDPOINT, data=json.dumps(payload), headers=headers)
    json_response = response.json()
    url_response = response.url

    #with open("data/test/lbc.json") as json_file:
    #    json_response = json.load(json_file)
    #print(json_response)

    attributes_set = set()

    for ad in json_response.get('ads', []):
        list_id = ad['list_id']

        fields = {
            'list_id': list_id,
            'first_publication_date': ad['first_publication_date'],
            'expiration_date' : ad.get('expiration_date'),
            'index_date' : ad.get('index_date'),
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
        fields['location_department_name'] = location.get('department_name' , None)
        fields['location_city_label'] = location['city_label']
        fields['location_city'] = location.get('city' , None)
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
        fields['owner_name'] = owner.get('name' , None)
        fields['owner_no_salesmen'] = owner['no_salesmen']
        fields['owner_siren'] = owner.get('siren' , None)
        #fields['owner_pro_rates_link'] = owner.get('owner_pro_rates_link' , None)

        options = ad['options']
        fields['opt_has_option'] = options['has_option']
        fields['opt_booster'] = options['booster']
        fields['opt_photosup'] = options['photosup']
        fields['opt_urgent'] = options['urgent']
        fields['opt_gallery'] = options['gallery']
        fields['opt_sub_toplist'] = options['sub_toplist']

        fields['has_phone'] = ad['has_phone']

        """ print("      ad {} price {} surf {} rooms {} city {}-{}".format(
            list_id,
            fields['price'], fields['square'],
            fields.get('rooms', -1),
            fields['location_city'], fields['location_zipcode']
        )) """

        date_classement =ad.get('index_date') #.strftime('%Y-%m-%d %H:%M:%S')
        #print(date_classement)
        if limit_date and date_classement <= limit_date :
            #print("      limit date reached")
            break

        try:
            ad_model = AdLBC.create(**fields)
            # ad_model.save()
        except IntegrityError as error:
            logging.info("ERROR: " + str(error))

        except Exception:
            print("{} - Insert data error into DB".format(config_id))





    AdBatchTable.update( limit_date=start_date_script, thread=0).where(AdBatchTable.id == config_id).execute()

    #print("      {} - new limit date to '{}'".format(config_id, start_date_script))
