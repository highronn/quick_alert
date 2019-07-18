import requests
import datetime
from dateutil.relativedelta import relativedelta
import json
import time
import uuid
import os
import logging

from jwt import JWT
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
    OperationalError,

    Model,

    MySQLDatabase
)

from jwt.jwk import OctetJWK

is_dev_db = (os.environ.get("QUICKALERT_DEV", "0") != 0)
db = MySQLDatabase(
    'quickalert',
    user='quickalert',
    password='quickalert',
    host='myquickalertdbinstance.cqlkfxu7awoj.eu-west-3.rds.amazonaws.com',
    port=3306
)

# Some constants used to build the base local JWT token
AUD_CONST = "SeLoger-Mobile-6.0"
APP_CONST = "63ee714d-a62a-4a27-9fbe-40b7a2c318e4"
ISS_CONST = "SeLoger-mobile"
JWT_CONST = "b845ec9ab0834b5fb4f3a876295542887f559c7920224906bf4bc715dd9e56bc"

AD_REQUIRED_FIELDS = {
    "id": BigIntegerField(null=False),
    "dateinsert": DateTimeField(null=False, default=datetime.datetime.now),

    "created"	: DateTimeField(null=True, default=None),
    "lastModified"	: DateTimeField(null=True, default=None),
    "transactionType"	: CharField(null=True, default=None),
    "realtyType"	: CharField(null=True, default=None),
    "title"	: CharField(null=True, default=None),
    "livingArea"	: CharField(null=True, default=None),
    "livingAreaUnit"	: CharField(null=True, default=None),
    "rooms"	: CharField(null=True, default=None),
    "bedrooms"	: CharField(null=True, default=None),
    "price"	: CharField(null=True, default=None),
    "priceUnit"	: CharField(null=True, default=None),
    "priceDescription"	:CharField(null=True, default=None),

    "priceAnnuity"	: CharField(null=True, default=None),
    "condoAnnualCharges"	: CharField(null=True, default=None),
    "city"	: CharField(null=True, default=None),
    "zipCode"	: CharField(null=True, default=None),
    "longitude"	: DecimalField(decimal_places=6, max_digits=9,null=True, default=None),
    "latitude"	: DecimalField(decimal_places=6, max_digits=9,null=True, default=None),
    "accuracy"	: CharField(null=True, default=None),
    "condoProperties"	: CharField(null=True, default=None),
    "energy_grade"	: CharField(null=True, default=None),
    "energy_status"	: CharField(null=True, default=None),
    "energy_value"	: CharField(null=True, default=None),
    "greenhouseGas_grade"	: CharField(null=True, default=None),
    "greenhouseGas_status"	: CharField(null=True, default=None),
    "greenhouseGas_value"	: CharField(null=True, default=None),

    "publicationId"	: CharField(null=True, default=None),
    #"isIndividual"	: CharField(null=True, default=None),
    "isIndividual"	: BooleanField(null=True, default=None),
    "thirdPartyId"	: CharField(null=True, default=None),
    "comments"	: CharField(null=True, default=None),
    "reference"	: CharField(null=True, default=None),

    "professionals_email"	: CharField(null=True, default=None),
    "professionals_id"	: CharField(null=True, default=None),
    "professionals_publicationId"	: CharField(null=True, default=None),
    "professionals_type"	: CharField(null=True, default=None),
    "professionals_name"	: CharField(null=True, default=None),
    "professionals_phoneNumber"	: CharField(null=True, default=None),
    "professionals_longitude"	: DecimalField(decimal_places=6, max_digits=9,null=True, default=None),
    "professionals_latitude"	: DecimalField(decimal_places=6, max_digits=9,null=True, default=None),
    "professionals_level"	: CharField(null=True, default=None),
    "professionals_directoryId"	: CharField(null=True, default=None),
    #"isSelection"	: CharField(null=True, default=None),
    #"isExclusiveness"	: CharField(null=True, default=None),
    "isSelection"	: BooleanField(null=True, default=None),
    "isExclusiveness"	: BooleanField(null=True, default=None),
    "businessUnit"	: CharField(null=True, default=None),

    "alur_feesPercentage"	: CharField(null=True, default=None),
    "alur_price"	: CharField(null=True, default=None),
    "alur_textTemplate"	: CharField(null=True, default=None),
    "alur_priceExcludingFees"	: CharField(null=True, default=None),
    "permalink"	: CharField(null=True, default=None),
    "priceVariations"	: TextField(null=True, default=None),
    "features"	: TextField(null=True, default=None),
    "description"	: TextField(null=True, default=None),

}


class BaseAds():
    def __init__(self):
        self.website = 'None'

    def get_ad_details(self, add_id, raw=True):
        ret = {
            'source': self.website,
            'id': None,
            'alur_feesPercentage': None,
            'alur_price': None,
            'alur_textTemplate': None,

            'priceDescription'	: None,
            'created'	: None,
            'lastModified'	: None,
            'title'	: None,
            'condoProperties'	: None,
            'energy_grade'	: None,
            'energy_status'	: None,
            'energy_value'	: None,
            'livingArea'	: None,
            'livingAreaUnit'	: None,
            'publicationId'	: None,
            'city'	: None,
            'zipCode'	: None,
            'longitude'	: None,
            'latitude'	: None,
            'accuracy'	: None,
            'isIndividual'	: None,
            'thirdPartyId'	: None,
            'comments'	: None,
            'reference'	: None,
            'price'	: None,
            'priceUnit'	: None,
            'priceAnnuity'	: None,
            'priceVariations'	: None,
            'alur_feesPercentage'	: None,
            'alur_price'	: None,
            'alur_textTemplate'	: None,
            'alur_priceExcludingFees'	: None,
            'professionals_email'	: None,
            'professionals_id'	: None,
            'professionals_publicationId'	: None,
            'professionals_type'	: None,
            'professionals_name'	: None,
            'professionals_phoneNumber'	: None,
            'professionals_longitude'	: None,
            'professionals_latitude'	: None,
            'professionals_level'	: None,
            'professionals_directoryId'	: None,
            'transactionType'	: None,
            'realtyType'	: None,
            'greenhouseGas_grade'	: None,
            'greenhouseGas_status'	: None,
            'greenhouseGas_value'	: None,
            'isSelection'	: None,
            'rooms'	: None,
            'bedrooms'	: None,
            'isExclusiveness'	: None,
            'businessUnit'	: None,
            'condoAnnualCharges'	: None,
            'description'	: None,
            'permalink'	: None,
            'features'	: None
        }
        return ret

    def get_location(self, cp):
        return None

    def search(self, cp, min_surf, max_price, ad_type, nb_room_min, raw=True):
        """Recover the ads matching a given search
        arg 1: the postal code
        arg 2: the minimal surface
        arg 3: the maximum rent/price
        arg 4: type of the add ('rent' -> location, 'sell' -> sell)
        arg 5: the owner_id of the search (the user making the search)
        arg 6: nb_room_min, minimum number of rooms
        arg 7: include the raw data in the return
        """
        ret = {
            'source': self.website,
            'id': [],
            'raw': None,
        }
        return ret


class SeLogerAds(BaseAds):
    def __init__(self):
        self._base_headers = {
            'User-Agent': 'okhttp/3.11.0',
            'AppGuid': APP_CONST,
            'AppToken': None,
            'Accept': 'Accept',
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip'
        }
        self._token_ts = 0
        self.website = 'SeLoger'

    @staticmethod
    def _map_type(ad_type):
        if ad_type == 'sell':
            return 2
        elif ad_type == 'rent':
            return 1

    # Generate the headers for the REST calls
    @property
    def headers(self):
        now = int(time.time() - 1)
        # if token is too old, renew it
        if now - self._token_ts > 1800:
            # update the auth token
            self._update_authed_token()
            # update the timestamp of the last authentication
            self._token_ts = now
            return self._base_headers
        else:
            return self._base_headers

    # Generate the local token
    def _gen_local_token(self):
        jwt_ = JWT()
        params = {
            'iss': ISS_CONST,
            'app': APP_CONST,
            'iat': int(time.time() - 1),
            'jit': str(uuid.uuid1()),
            'aud': AUD_CONST,
            'kty': 'RSA',
        }
        encoded_jwt = jwt_.encode(
            payload=params,
            key = OctetJWK(bytes(JWT_CONST, 'utf-8')),
            alg = 'HS256',
            optional_headers = {"typ":"JWT","alg":"HS256"})
        return encoded_jwt

    # Get the authenticated token.
    # For that, you generate the local token, do a call on "/security/authenticate" which give you back
    # the JWT token used for the rest of the REST calls.
    def _update_authed_token(self):
        local_token = self._gen_local_token()
        self._base_headers['AppToken'] = local_token
        auth_url = "https://api-seloger.svc.groupe-seloger.com/api/v1/security/authenticate"
        r = requests.get(auth_url, headers=self._base_headers,timeout=30)
        authed_token = r.text[1:-1]
        self._base_headers['AppToken'] = authed_token

    def get_ad_details(self, add_id, raw=True):
        """Recover the details of an ad"""
        ret = None
        v_timer = 5
        v_wait = 5
        wait_time = 1.5

        """
        r = requests.get("https://api-seloger.svc.groupe-seloger.com/api/v1/listings/%s" % (add_id), headers=self.headers)
        try:
            data = r.json()
        except:
            print(r.status_code)
            print(r.text) """




        #####################################################################################"


        for i in range(0,10):
            try:
                r = requests.get("https://api-seloger.svc.groupe-seloger.com/api/v1/listings/%s" % (add_id), headers=self.headers, timeout=30)
                data = r.json()
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
            except:
                print("     {}".format(r.status_code))
                print("     {}".format(r.text))
                print ("      ad.get - {} - Waiting : {} sec(s)".format(r.status_code,v_timer))
                time.sleep(v_timer)
                v_timer += v_wait
                continue

            else:
                break

        else:
            return

        #####################################################################################""


        #print(r.json())
        #time.sleep(10)
        #return
        ret = {
            'source': self.website,
            'id': add_id,

            'priceDescription': data['priceDescription'],
            'created': datetime.datetime.strptime(data['created'], '%Y-%m-%dT%H:%M:%S'),
            'lastModified': datetime.datetime.strptime(data['lastModified'], '%Y-%m-%dT%H:%M:%S'),
            'title': data['title'],
            'condoProperties': data['condoProperties'],
            'energy_grade': data['energy']['grade'],
            'energy_status': data['energy']['status'],
            'energy_value': data['energy']['value'],
            'livingArea': data['livingArea'],
            'livingAreaUnit': data['livingAreaUnit'],
            'publicationId': data['publicationId'],
            'city': data['city'],
            'zipCode': data['zipCode'],
            'longitude': data['coordinates']['longitude'],
            'latitude': data['coordinates']['latitude'],
            'accuracy': data['coordinates']['accuracy'],
            'isIndividual': data['isIndividual'],
            'thirdPartyId': data['thirdPartyId'],
            'comments': data['comments'],
            'reference': data['reference'],
            'price': data['price'],
            'priceUnit': data['priceUnit'],
            'priceAnnuity': data['priceAnnuity'],
            'priceVariations': data.get('priceVariations',None),

            'alur_feesPercentage': data['alur'].get('feesPercentage',None),
            'alur_price': data['alur'].get('price',None),
            'alur_textTemplate': data['alur'].get('textTemplate',None),
            'alur_priceExcludingFees': data['alur'].get('priceExcludingFees',None),

            'professionals_email': data['professionals'][0]['email'],
            'professionals_id': data['professionals'][0]['id'],
            'professionals_publicationId': data['professionals'][0]['publicationId'],
            'professionals_type': data['professionals'][0]['type'],
            'professionals_name': data['professionals'][0]['name'],
            'professionals_phoneNumber': data['professionals'][0]['phoneNumber'],
            'professionals_longitude': data['professionals'][0]['longitude'],
            'professionals_latitude': data['professionals'][0]['latitude'],
            'professionals_level': data['professionals'][0]['level'],
            'professionals_directoryId': data['professionals'][0]['directoryId'],

            'transactionType': data['transactionType'],
            'realtyType': data['realtyType'],
            'greenhouseGas_grade': data['greenhouseGas']['grade'],
            'greenhouseGas_status': data['greenhouseGas']['status'],
            'greenhouseGas_value': data['greenhouseGas']['value'],
            'isSelection': data['isSelection'],
            'rooms': data['rooms'],
            'bedrooms': data['bedrooms'],
            'isExclusiveness': data['isExclusiveness'],
            'businessUnit': data['businessUnit'],
            'condoAnnualCharges': data['condoAnnualCharges'],
            'description': data['description'],
            'permalink': data['permalink'],
            'features': data['features'],
        }
        if raw:
            ret['raw'] = data
        """ for t in data['transportations'].get('available', []):
            ret['proximity'].append(t['name'])
        for p in data['photos']:
            ret['picture'].append(p) """
        return ret

    def get_location(self, cp):
        """get the seloger location code from the postal code"""
        LOCATION_URL = "https://api-seloger.svc.groupe-seloger.com/api/v1/locations/search"

        LOCATION_PAYLOAD = {
            "latitude": 0.0,
            "limit": 50,
            "locationTypes": 30,
            "longitude": 0.0,
            "radius": 0,
            "searchTerm": cp,
            "type": 0
        }

        r = requests.post(LOCATION_URL, data=json.dumps(LOCATION_PAYLOAD), headers=self.headers,timeout=30)
        return r.json()[0]['id']

    def search(self, cp, min_surf, max_price, ad_type, nb_room_min,config_id, raw=True):
        """Recover the ads matching a given search
        arg 1: the postal code
        arg 2: the minimal surface
        arg 3: the maximum rent/price
        arg 4: type of the add (1 -> location, 2 -> sell)
        arg 5: the owner_id of the search (the user making the search)
        arg 6: nb_room_min, minimum number of rooms"""

        #######################################################""
        try :
            _cp = []
            if type(cp) is list:
                for c in cp:
                    _cp.append(self.get_location(c))
            else:
                _cp.append(self.get_location(cp))

            db_cp = cp
            db_insee_code = AdBatchTable.get(AdBatchTable.id == config_id).ad_code
            __cp=_cp[0]

            if __cp != db_insee_code :
                print("     Check CP Update     {}/{} for {}".format(db_insee_code,__cp,db_cp))
                AdBatchTable.update( ad_code=__cp, is_actif=3).where(AdBatchTable.id == config_id).execute()
        except :
            return -2
        #######################################################""


        v_timer = 5
        v_wait = 5
        wait_time = 1.5
        _pageCount = 10
        ret = {
                'id': [],
                'source': self.website
            }
        #for y in range(1,_pageCount) :
        y = 1
        _pageCount = 1
        while y <= _pageCount :
            #print(y)
            #print(_pageCount)
            SEARCH_PAYLOAD = {
                "pageIndex": y,
                "pageSize": 100 ,
                "query": {
                    #"bedrooms": [],
                    "includeNewConstructions": True,
                    "inseeCodes": [__cp],
                    #"maximumPrice": max_price,
                    #"minimumLivingArea": min_surf,
                    #"realtyTypes": 3,
                    #"rooms": list(range(nb_room_min, 5)),
                    "sortBy":10,
                    #"transactionType": self._map_type(ad_type)
                    "transactionType": ad_type
                }
            }
            #"sortBy":0
            #"sortBy":1 prix/m2 croissant
            #"sortBy":2 prix/m2 DEcroissant
            #"sortBy":3 Prix croissant
            #"sortBy":4 Prix decroissant
            #"sortBy":5 Surface croissante
            #"sortBy":6 Surface decroissante
            #"sortBy":7 None
            #"sortBy":8 None
            #"sortBy":9  ????
            #"sortBy":10  date created récente
            #"sortBy":11  date
            SEARCH_URL = "https://api-seloger.svc.groupe-seloger.com/api/v1/listings/search"
            #################################################################

            #print('hello')
            for i in range(0,10):
                try:
                    #r = requests.post(SEARCH_URL, data=json.dumps(SEARCH_PAYLOAD), headers=self.headers,timeout=10)
                    r = requests.post(SEARCH_URL, data=json.dumps(SEARCH_PAYLOAD), headers=self.headers,timeout=120)
                    #print("     {}".format(r))
                    if r.status_code == 404:
                        AdBatchTable.update(is_actif = -1).where(AdBatchTable.id == config_id).execute()
                        print("     Batch deactivated")
                        return -2
                    if r.status_code != 200 :
                        print(r.status_code)
                        continue
                    else :

                        data = r.json()
                        #print(data)
                        time.sleep(10)
                        if y == 1 :
                            print ("pageCount : {}".format(data['pageCount']))
                            print ("totalCount : {}".format(data['totalCount']))
                        _pageCount = data['pageCount']
                        print ("Retrieve Page : {}".format(y))
                        break
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
                config_id = AdBatchView.get().id
                AdBatchTable.update(is_actif = -2).where(AdBatchTable.id == config_id).execute()
                print("    {} - Batch deactivated".format(config_id))
                return
            #################################################################
            #print('hello2')
            ret1 = {
                'id': [],
                'source': self.website
            }

            for i in data['items']:
                ret1['id'].append(i['id'])

            #print(ret1)



            ret['id'].extend( ret1['id'])
            #print ( ret['id'])
            #print(_pageCount)
            y += 1


        else :
            return ret


class AdSeLoger(Model):
    class Meta:
        database = db
        db_table = 't_sel_ads_buffer_in'
        primary_key = False

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
        db_table = 'v_batch_run_sel'

    id = CharField(unique=True, primary_key=True)
    #cp = DateTimeField(null=False)
    ad_type = CharField(null=False)
    ad_code = CharField(null=False)
    cp = CharField(null=False)

def init_models():
    for name, typ in AD_REQUIRED_FIELDS.items():
        AdSeLoger._meta.add_field(name, typ)
    AdSeLoger.create_table(safe=True)


def search(params,ThreadId):
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
            #BatchTable = AdBatchTable.get(AdBatchTable.id == config_id)
            #print(BatchTable.thread)
            if AdBatchTable.get(AdBatchTable.id == config_id).thread == 0 :
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
            #BatchTable = AdBatchTable.get(AdBatchTable.id == config_id)
            #time.sleep(1/ThreadId)
            if AdBatchTable.get(AdBatchTable.id == config_id).thread == ThreadId :
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
    BatchTable = AdBatchTable.get(AdBatchTable.id == config_id)

    params['config_id'] = config_id
    params["sel"]["cp"] = AdBatchTable.get(AdBatchTable.id == config_id).cp
    params["sel"]["ad_type"] = AdBatchTable.get(AdBatchTable.id == config_id).ad_type
    cp = params["sel"]["cp"]

    #print(params)





    start_date_script = (datetime.datetime.now()+ relativedelta(minutes=-0)).strftime('%Y-%m-%d %H:%M:00')


    try:
        config = AdBatchTable.get(AdBatchTable.id == config_id)
        limit_date = config.limit_date.strftime('%Y-%m-%d %H:%M:%S')
        print("{} - Thread {} batch locked successfully : {}".format(config_id, ThreadId,limit_date))
        #print("     {} - using limit date : {}".format(config_id,limit_date))
    except Exception:
        print("     {} - no config found for. no limit date will be used".format(config_id))
        limit_date = None
    ####################################################################



    #################################################""
    """ try :
        params['config_id'] = AdBatchName.get().id
    except Exception:
        print("No Batch to run")
        return -1

    params["sel"]["cp"] = AdBatchName.get().cp
    params["sel"]["ad_type"] = AdBatchName.get().ad_type
    config_id = params['config_id']


    #print(params)
    #print(config_id)

    start_date_script = (datetime.datetime.now()+ relativedelta(minutes=-0)).strftime('%Y-%m-%d %H:%M:00')

    try:
        config = AdBatchInfo.get(AdBatchInfo.id == config_id)
        limit_date = config.limit_date.strftime('%Y-%m-%d %H:%M:%S')
        print("     {} - using limit date : {}".format(config_id,limit_date))
    except Exception:
        print("     {} - no config found for. no limit date will be used".format(config_id))
        limit_date = None
    #################################################

    #print(sel_params) """


    #################################################
    #################################################
    #################################################
    #################################################






    sel_params = params['sel']


    seloger = SeLogerAds()


    config_idd=config_id
    #print(config_idd)

    r = seloger.search(**sel_params,config_id=config_idd)
    if r == -2 :
        return -2
        #print("     {}".format(r))

      # check that data sent are coherent
    # should have the same count of element in r['id'] and r['raw']['items']
    ids = r.get("id", [])
    #items = r.get("raw", {}).get("items")
    id_count = len(ids)
    #item_count = len(items)
    print(ids)
    #print(items)
    print(id_count)
    #print(item_count)
    #assert(id_count == item_count)

    logging.info("      {} ads received.".format(id_count))
    batch_id = 0
    #print(ids)
    for id in ids:


        ##################################################""
        # NEW
        ##################################################""
        batch_id += 1
        data = seloger.get_ad_details(id, raw=True)['raw']
        ##################################################""
        # DESCRIPTION CHAMPS
        ##################################################""
        fields = {
            'id': id,
            'priceDescription': data['priceDescription'],
            'created': datetime.datetime.strptime(data['created'], '%Y-%m-%dT%H:%M:%S'),
            'lastModified': datetime.datetime.strptime(data['lastModified'], '%Y-%m-%dT%H:%M:%S'),
            'title': data['title'],
            'condoProperties': data['condoProperties'],
            'energy_grade': data['energy']['grade'],
            'energy_status': data['energy']['status'],
            'energy_value': data['energy']['value'],
            'livingArea': data['livingArea'],
            'livingAreaUnit': data['livingAreaUnit'],
            'publicationId': data['publicationId'],
            'city': data['city'],
            'zipCode': data['zipCode'],
            'longitude': data['coordinates']['longitude'],
            'latitude': data['coordinates']['latitude'],
            'accuracy': data['coordinates']['accuracy'],
            'isIndividual': data['isIndividual'],
            'thirdPartyId': data['thirdPartyId'],
            'comments': data['comments'],
            'reference': data['reference'],
            'price': data['price'],
            'priceUnit': data['priceUnit'],
            'priceAnnuity': data['priceAnnuity'],
            'priceVariations': data.get('priceVariations',None),
            'alur_feesPercentage': data['alur'].get('feesPercentage',None),
            'alur_price': data['alur'].get('price',None),
            'alur_textTemplate': data['alur'].get('textTemplate',None),
            'alur_priceExcludingFees': data['alur'].get('priceExcludingFees',None),
            'professionals_email': data['professionals'][0]['email'],
            'professionals_id': data['professionals'][0]['id'],
            'professionals_publicationId': data['professionals'][0]['publicationId'],
            'professionals_type': data['professionals'][0]['type'],
            'professionals_name': data['professionals'][0]['name'],
            'professionals_phoneNumber': data['professionals'][0]['phoneNumber'],
            'professionals_longitude': data['professionals'][0]['longitude'],
            'professionals_latitude': data['professionals'][0]['latitude'],
            'professionals_level': data['professionals'][0]['level'],
            'professionals_directoryId': data['professionals'][0]['directoryId'],
            'transactionType': data['transactionType'],
            'realtyType': data['realtyType'],
            'greenhouseGas_grade': data['greenhouseGas']['grade'],
            'greenhouseGas_status': data['greenhouseGas']['status'],
            'greenhouseGas_value': data['greenhouseGas']['value'],
            'isSelection': data['isSelection'],
            'rooms': data['rooms'],
            'bedrooms': data['bedrooms'],
            'isExclusiveness': data['isExclusiveness'],
            'businessUnit': data['businessUnit'],
            'condoAnnualCharges': data['condoAnnualCharges'],
            'description': data['description'],
            'permalink': data['permalink'],
            'features': data['features'],
        }
        print("     {}   {}      {}-ad {} price {} surf {} rooms {} city {}-{}".format(
        data['created'],data['lastModified'],batch_id,id,data['price'],data['livingArea'],data['rooms'],data['city'],data['zipCode']))

        ##################################################""
        # CONTROLE DATE LIMITE
        ##################################################""
        date_classement = data['created']
        if limit_date and date_classement <= limit_date :
            print("      limit date reached")
            break

        ##################################################""
        # INSERT BDD
        ##################################################""
        try:
            ad_model = AdSeLoger.create(**fields)
            # ad_model.save()
        except IntegrityError as error:
            logging.info("ERROR: " + str(error))
    ##################################################""
    # UPDATE LIMIT_DATE & THREAD = 0
    ##################################################""
    AdBatchTable.update( limit_date=start_date_script, thread=0, is_actif=5).where(AdBatchTable.id == config_id).execute()
    print("      {} - new limit date to '{}'".format(config_id, start_date_script))
