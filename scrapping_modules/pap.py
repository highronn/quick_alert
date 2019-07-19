# -*- coding: utf-8 -*-

import sys
import os
import logging
import requests
import time
import random

from datetime import datetime
from urllib.parse import unquote, urlencode
from dateutil.relativedelta import relativedelta

from models import dev_db

from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPProxyAuth

from fake_useragent import UserAgent

from peewee import (
    CharField,
    IntegerField,
    TextField,
    DateTimeField,
    IntegerField,
    BigIntegerField,
    BooleanField,
    FloatField,
    DecimalField,
    IntegrityError,
    Model,
    MySQLDatabase
)

is_dev_db = (os.environ.get("QUICKALERT_DEV", "0") != 0)
db = dev_db if is_dev_db else MySQLDatabase(
    'rec_quickalert',
    user='rec_quickalert',
    password='quickalert',
    host='myquickalertdbinstance.cqlkfxu7awoj.eu-west-3.rds.amazonaws.com',
    port=3306
)

start_date_script = (datetime.now() + relativedelta(minutes=0)).strftime('%Y-%m-%d %H:%M:00')

AD_REQUIRED_FIELDS = {
    "id": IntegerField(null=False),
    "dateinsert": DateTimeField(null=False, default=datetime.now),
    "produit": CharField(null=True, default=None),
    "typebien": CharField(null=True, default=None),
    "prix": IntegerField(null=True, default=None),
    "surface": IntegerField(null=True, default=None),
    "nb_pieces": IntegerField(null=True, default=None),
    "nb_chambres_max": IntegerField(null=True, default=None),
    "nb_photos": IntegerField(null=True, default=None),
    "date_classement": DateTimeField(null=True, default=None),
    "telephone": CharField(null=True, default=None),
    "city": CharField(null=True, default=None),
    #"departement": CharField(null=True, default=None),
    "nouvelle_annonce": CharField(null=True, default=False),
    "lat": FloatField(null=True, default=False),
    "lng": FloatField(null=True, default=False),
    "classe_energie": CharField(null=True, default=None),
    "visite_virtuelle": CharField(null=True, default=None),
    "place_slug": CharField(null=True, default=None),
    "place_id": CharField(null=True, default=None),
    "place_title": CharField(null=True, default=None),
    "place_lat": FloatField(null=True, default=False),
    "place_lng": FloatField(null=True, default=False),
    "place_is_idf": CharField(null=True, default=None),
    "link": TextField(null=True, default=None),
    "texte": TextField(null=True, default=None),
}



"""
class AdSeLoger(Model):
    class Meta:
        database = db
        db_table = 't_sel_ads_buffer_in'
        primary_key = False
"""


###################################################################3
class AdPap(Model):
    class Meta:
        database = db
        db_table = 't_pap_ads_buffer_in'
"""
class AdBatchTable(Model):
    class Meta:
        database = db
        db_table = 't_batch_info_2'

    id = CharField(unique=True, primary_key=True)
    is_actif = IntegerField(null=False)
    limit_date = DateTimeField(null=False)
    thread = IntegerField(null=True)

class AdBatchView(Model):
    class Meta:
        database = db
        db_table = 'v_batch_run_pap'


    id = CharField(unique=True, primary_key=True)
    cp = DateTimeField(null=False)
    ad_type = CharField(null=False)   """

class AdBatchTable(Model):
    class Meta:
        database = db
        db_table = 't_batch_info'

    id = CharField(unique=True, primary_key=True)
    is_actif = IntegerField(null=False)
    limit_date = DateTimeField(null=False)
    ad_type = CharField(null=False)
    ad_code = CharField(null=False)
    cp = CharField(null=False)
    thread = IntegerField(null=False)

class AdBatchView(Model):
    class Meta:
        database = db
        db_table = 'v_batch_run_pap'

    id = CharField(unique=True, primary_key=True)
    cp = CharField(null=False)
    ad_type = CharField(null=False)

class v_check_validity(Model):
    class Meta:
        database = db
        db_table = 'v_check_validity'

    id_ad = IntegerField(unique=True, primary_key=True)
    id_origin = IntegerField(null=False)
    check_expiration = IntegerField(null=False)
    url = TextField(null=False)

class t_peewee(Model):
    class Meta:
        database = db
        db_table = 't_all_ads_flag'

    id_ad = IntegerField(unique=True, primary_key=True)
    id_origin = IntegerField(null=False)
    check_expiration = IntegerField(null=False)
    url = TextField(null=False)

ua = UserAgent()

header = {
    'X-Device-Gsf': '36049adaf18ade77',
    'User-Agent': ua.random,
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip'
}


def init_models():
    for name, typ in AD_REQUIRED_FIELDS.items():
        AdPap._meta.add_field(name, typ)

    AdPap.create_table(safe=True)

    #AdPapConf.create_table(safe=True)


def search(parameters, thread):

    v_timer = 5
    v_wait = 0
    wait_time = 1.5
    start_date_script = (datetime.now()+ relativedelta(minutes=0)).strftime('%Y-%m-%d %H:%M:00')

    """ parameters['config_id'] = AdBatchView.get().id
    parameters["cities"][0][1] = AdBatchView.get().cp
    parameters["pap"]["recherche[produit]"] = AdBatchView.get().ad_type
    config_id = parameters['config_id'] """

    try :
        parameters['config_id'] = AdBatchView.get().id
        parameters["cities"][0][1] = AdBatchView.get().cp
        parameters["pap"]["recherche[produit]"] = AdBatchView.get().ad_type
        config_id = parameters['config_id']

    except Exception:
        print("No Batch to run")
        return -1

    try:
        config = AdBatchTable.get(AdBatchTable.id == parameters['config_id'])
        limit_date = config.limit_date.strftime('%Y-%m-%d %H:%M:%S')
        print("{} - using limit date : {}".format(config_id,limit_date))

    except Exception:
        print("{} - no config found for. no limit date will be used".format(config_id))
        limit_date = None



    # Préparation des paramètres de la requête
    payload = {}
    """ payload = {
        'recherche[prix][min]': parameters['price'][0],  # Loyer min
        'recherche[prix][max]': parameters['price'][1],  # Loyer max
        'recherche[surface][min]': parameters['surface'][0],  # Surface min
        'recherche[surface][max]': parameters['surface'][1],  # Surface max
        'recherche[nb_pieces][min]': parameters['rooms'][0],  # Pièces min
        'recherche[nb_chambres][min]': parameters['bedrooms'][0],  # Chambres min
        #'size': 200,
        #'page': 1
    } """
    # Insertion des paramètres propres à PAP
    payload.update(parameters['pap'])
    params = urlencode(payload)

    # Ajout des villes
    for city in parameters['cities']:

        code = place_search(city[1])
        #print("&recherche[geo][ids][]=%s" % code)
        #print(code)
        if code == 0:
            AdBatchTable.update(is_actif = -1).where(AdBatchTable.id == config_id).execute()
            print("     Batch deactivated")
            return

        else :
            params += "&recherche[geo][ids][]=%s" % code

    #print (parameters)

    #print("Retrieve Ads")
    for i in range(0,10):
        #proxies = { 'https' : "https://139.28.219.246:8080" }
        #request = requests.get("https://ws.pap.fr/immobilier/annonces", params=unquote(params), headers=header, timeout=60,proxies=proxies,auth=HTTPBasicAuth('loic.montagnac@gmail.com', 'FRbY3wZPobCmAbIEaBzW'))

        #proxies = { 'https' : "https://loic.montagnac@gmail.com:FRbY3wZPobCmAbIEaBzW@139.28.219.246:8080" }
        #request = requests.get("https://ws.pap.fr/immobilier/annonces", params=unquote(params), headers=header, timeout=60,proxies=proxies)

        """
        s = requests.Session()
        proxies = {
        "http": "http://fr373.nordvpn.com:8080",
        "https": "https://fr373.nordvpn.com:8080"
        }
        auth = HTTPProxyAuth("loic.montagnac@gmail.com", "FRbY3wZPobCmAbIEaBzW")
        s.proxies = proxies
        s.auth = auth        # Set authorization parameters globally

        ext_ip = s.get("https://ws.pap.fr/immobilier/annonces", params=unquote(params), headers=header, timeout=120)
        """
        try:
            request = requests.get("https://ws.pap.fr/immobilier/annonces", params=unquote(params), headers=header, timeout=10)
            #print("{} - URI = {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), request.url))
            print(request.url)
            data = request.json()
            time.sleep(wait_time)
            #print(data)
        except requests.exceptions.ConnectionError as r:
            r.status_code = "      {} - Connection refused"
            print ("      requests.get - {} - Waiting : {} sec(s)".format(r.status_code,v_timer))
            time.sleep(v_timer)
            v_timer += v_wait
            continue
        except requests.exceptions.ReadTimeout as r:
            r.status_code = "Connection Timeout"
            print ("      requests.get - {} - Waiting : {} sec(s)".format(r.status_code,v_timer))
            time.sleep(v_timer)
            v_timer += v_wait
            continue
        else:
            break
    else:
        return

    with open("output.json", "w+") as output:
        output.write(str(data))

    #print("Retrieve Ad details")
    for it, ad in enumerate(data['_embedded'].get('annonce', [])):
        ad_id = ad.get('id')

        for i in range(0,10):
            try:
                _request = requests.get("https://ws.pap.fr/immobilier/annonces/{}".format(ad_id), headers=header, timeout=3)
                #print("{} - URI = {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), request.url))
                _data = _request.json()
                time.sleep(wait_time)
            except requests.exceptions.ConnectionError as r:
                r.status_code = "Connection refused"
                print ("      ad.get - {} - Waiting : {} sec(s)".format(r.status_code,v_timer))
                time.sleep(v_timer)
                v_timer += v_wait
                continue

            except requests.exceptions.ReadTimeout as r:
                r.status_code = "Connection Timeout"
                print ("      ad.get - {} - Waiting : {} sec(s)".format(r.status_code,v_timer))
                time.sleep(v_timer)
                v_timer += v_wait
                continue
            else:
                break

        else:
            return

        #photos = list()
        #if ad.get("nb_photos") > 0:
        #    for photo in ad["_embedded"]['photo']:
        #        photos.append(photo['_links']['self']['href'])

        ad_place = _data["_embedded"]['place'][0]
        ad_marker = _data['marker']

        ad_fields = dict(
            id = ad_id,
            date_classement = datetime.fromtimestamp(_data.get("date_classement")),
            produit = ad.get("produit"),
            typebien = ad.get("typebien"),
            prix = ad.get('prix'),
            surface = ad.get('surface'),
            nb_pieces = ad.get('nb_pieces'),
            nb_chambres_max = ad.get('nb_chambres_max'),
            telephone = _data.get("telephones")[0].replace('.', '') if len(_data.get("telephones")) > 0 else None,
            city = ad_place['title'],
            #departement = ad.get('adtech'),
            nouvelle_annonce = ad.get("nouvelle_annonce"),
            lat = ad_marker.get("lat") if ad_marker else None,
            lng = ad_marker.get("lng") if ad_marker else None,
            classe_energie = _data.get('classe_energie'),
            visite_virtuelle = ad.get('visite_virtuelle'),
            nb_photos = ad["nb_photos"],
            place_is_idf = ad_place.get('is_idf'),
            place_lat = float(ad_place.get('lat')),
            place_lng = float(ad_place.get('lng')),
            place_title = ad_place.get('title'),
            place_slug = ad_place.get('slug'),
            place_id = ad_place.get('id'),
            link = ad["_links"]['desktop']['href'],
            texte = str(_data.get("texte")),
        )

        date_classement = ad_fields["date_classement"].strftime('%Y-%m-%d %H:%M:%S')

        #print(date_classement)
        #print(limit_date)
        if limit_date and date_classement <= limit_date :
            print("      limit date reached")
            break

        print("      {} Import ADS : {} - {} - {} sec ...".format(it, ad_id, date_classement, wait_time))
        for i in range(0,2):
            try:
                #db.connect
                ad_model = AdPap.create(**ad_fields)
                # ad_model.save()
                #db.close
            except IntegrityError as error:
                logging.info("      Error: " + str(error))
                break
            except:
                #logging.info("ERROR: Database error connection")
                time.sleep(v_timer)
                v_timer += v_wait
                db.close
                init_models()
                print ("      Database error - waiting : {} sec(s)".format(v_timer))
                return
            else:
                break

    AdBatchTable.update( limit_date=start_date_script).where(AdBatchTable.id == config_id).execute()
    print("      {} - new limit date to '{}'".format(config_id, start_date_script))
    #print("Change PROXY")
    #time.sleep(20)

def place_search(zipcode):
    """Retourne l'identifiant PAP pour un code postal donné"""
    payload = {
        "recherche[cible]": "pap-recherche-ac",
        "recherche[q]": zipcode
    }

    v_timer = 5
    v_wait = 0

    #print("Retrieve Ids of postal code : {}".format(zipcode))

    for i in range(0,5):
        try:
            request = requests.get("https://ws.pap.fr/gis/places", params=payload, headers=header, timeout=3)
            #print("{} - URI = {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),request.url))
            json = request.json()['_embedded']['place'][0]['id']
            time.sleep(1.5)
            return json
        except requests.exceptions.ConnectionError as r:
            r.status_code = "Connection refused"
            print ("      place_search - {} - Waiting : {} sec(s)".format(r.status_code,v_timer))
            time.sleep(v_timer)
            v_timer += v_wait
            continue
        except requests.exceptions.ReadTimeout as r:
            r.status_code = "Connection Timeout"
            print ("      place_search - {} - Waiting : {} sec(s)".format(r.status_code,v_timer))
            time.sleep(v_timer)
            v_timer += v_wait
            continue
        except :
            print ("      place_search - zipcode doesn't exist - Waiting : {} sec(s)".format(v_timer))
            #time.sleep(v_timer)
            #v_timer += v_wait
            return 0


        else:
            break

def get_expiration():
    """Vérifie la validité des annonces pap"""

    v_delay = 5
    v_wait_e = 0
    v_wait_r = 1.5

    for a in range(1,40):
        config = v_check_validity.get()
        id_origin = config.id_origin
        id_ad  = config.id_ad

        init_url = config.url

        print(init_url)

        for i in range(0,10):
            try:
                request = requests.get(init_url,  headers=header, timeout=3)
                print (request.url)
                print (request.text)

                if id_origin == 1 and request.url == init_url:
                    t_peewee.update(check_expiration = t_peewee.check_expiration + 3).where(t_peewee.id_ad == id_ad, t_peewee.id_origin == config.id_origin).execute()
                    print("get expiration {} :  {}  Valide".format(a,id_ad))
                    data = request.json()
                    print(data)
                    time.sleep(v_wait_r)

                elif id_origin == 1 and  "expiree" in  request.url :
                    t_peewee.update(check_expiration = -4).where(t_peewee.id_ad == id_ad, t_peewee.id_origin == config.id_origin).execute()
                    print("get expiration {} :  {}  Expirée".format(a,id_ad))
                    time.sleep(v_wait_r)

                elif  id_origin == 1 and "erreur-temporaire" in  request.url :
                    t_peewee.update(check_expiration = -1).where(t_peewee.id_ad == id_ad, t_peewee.id_origin == config.id_origin).execute()
                    print("get expiration {} :  {}  Erreur-temporaire".format(a,id_ad))
                    print("{} - URL = {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),request.url))
                    time.sleep(v_wait_r)
                    sys.exit()

                elif  id_origin == 2 and  "produit" in request.text :
                    t_peewee.update(check_expiration = t_peewee.check_expiration + 3).where(t_peewee.id_ad == id_ad, t_peewee.id_origin == config.id_origin).execute()
                    print("     get expiration {} :  {}  Valide".format(a,id_ad))
                    time.sleep(v_wait_r)

                elif  id_origin == 2 and  "Page introuvable" in request.text :
                    t_peewee.update(check_expiration = -4).where(t_peewee.id_ad == id_ad, t_peewee.id_origin == config.id_origin).execute()
                    print("     get expiration {} :  {}  Page introuvable".format(a,id_ad))
                    time.sleep(v_wait_r)

                """ else:
                    t_peewee.update(check_expiration=-3).where(t_peewee.id_ad == id_ad, t_peewee.id_origin == config.id_origin).execute()
                    print("get expiration {} :  {}  Invalide".format(a,id_ad))
                    print("{} - URL = {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),request.url))
                    time.sleep(v_wait_r) """
                break

            except requests.exceptions.ConnectionError as r:
                r.status_code = "Connection refused"
                time.sleep(v_wait_e)
                v_wait_e += v_delay
                print ("      {} - Try again - Waiting : {} sec(s)".format(r.status_code,v_wait_e))
                continue

            except requests.exceptions.ReadTimeout as r:
                r.status_code = "Connection Timeout"
                time.sleep(v_wait_e)
                v_wait_e += v_delay
                print ("      {} - Try again - Waiting : {} sec(s)".format(r.status_code,v_wait_e))
                continue


