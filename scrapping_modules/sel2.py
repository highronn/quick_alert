import requests
import datetime
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
db = dev_db if is_dev_db else MySQLDatabase(
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


class BaseAds():
    def __init__(self):
        self.website = 'None'

    def get_ad_details(self, add_id, raw=True):
        ret = {
            'source': self.website,
            'id': None,
            'price': None,
            'price_unit': None,
            'room': None,
            'surface': None,
            'surface_unit': None,
            'city': None,
            'postal_code': None,
            'date': datetime.datetime.fromtimestamp(0),
            'longitude': None,
            'latitude':  None,
            'proximity': [],
            'pictures': [],
            'description': None,
            'link': None,
            'raw': None,
        }
        return ret

    def get_location(self, cp):
        return None

    # Return the number of ads matching a search
    def count(self, cp, min_surf, max_price, ad_type, nb_room_min):
        """Return the number of ads matching a search
        arg 1: the postal code
        arg 2: the minimal surface
        arg 3: the maximum rent/price
        arg 4: type of the add ('rent' -> location, 'sell' -> sell)
        arg 5: the owner_id of the search (the user making the search)
        arg 6: nb_room_min, minimum number of rooms
        """
        return 0

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
        r = requests.get(auth_url, headers=self._base_headers)
        authed_token = r.text[1:-1]
        self._base_headers['AppToken'] = authed_token

    def get_ad_details(self, add_id, raw=True):
        """Recover the details of an ad"""
        ret = None
        r = requests.get("https://api-seloger.svc.groupe-seloger.com/api/v1/listings/%s" % (add_id), headers=self.headers)
        try:
            data = r.json()
        except:
            print(r.status_code)
            print(r.text)

        ret = {
            'source': self.website,
            'id': add_id,
            'price': data['price'],
            'price_unit': data['priceUnit'],
            'room': data['rooms'],
            'surface': data['livingArea'],
            'surface_unit': data['livingAreaUnit'],
            'city': data['city'],
            'postal_code': data['zipCode'],
            'date': datetime.datetime.strptime(data['lastModified'], '%Y-%m-%dT%H:%M:%S'),
            'longitude': data['coordinates']['longitude'],
            'latitude': data['coordinates']['latitude'],
            'proximity': [],
            'picture': [],
            'description': data['description'],
            'link': data['permalink'],
        }
        if raw:
            ret['raw'] = data
        for t in data['transportations'].get('available', []):
            ret['proximity'].append(t['name'])
        for p in data['photos']:
            ret['picture'].append(p)
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

        r = requests.post(LOCATION_URL, data=json.dumps(LOCATION_PAYLOAD), headers=self.headers)
        return r.json()[0]['id']

    # Return the number of ads matching a search
    def count(self, cp, min_surf, max_price, ad_type, nb_room_min):
        """Return the number of ads matching a search
        arg 1: the postal code
        arg 2: the minimal surface
        arg 3: the maximum rent/price
        arg 4: type of the add ('rent' -> location, 'sell' -> sell)
        arg 5: the owner_id of the search (the user making the search)
        arg 6: nb_room_min, minimum number of rooms
        """
        _cp = []
        if type(cp) is list:
            for c in cp:
                _cp.append(self.get_location(c))
        else:
            _cp.append(get_location(cp))

        SEARCH_PAYLOAD = [
            {
                "includeNewConstructions": True,
                "inseeCodes": _cp,
                "maximumPrice": max_price,
                "minimumLivingArea": min_surf,
                "realtyTypes": 3,
                "rooms": range(nb_room_min, 5),
                "transactionType": self._map_type(ad_type)
            },
        ]

        COUNT_URL = "https://api-seloger.svc.groupe-seloger.com/api/v1/listings/count"

        r = requests.post(COUNT_URL, data=json.dumps(SEARCH_PAYLOAD), headers=self.headers)
        return r.json()[0]

    def search(self, cp, min_surf, max_price, ad_type, nb_room_min, raw=True):
        """Recover the ads matching a given search
        arg 1: the postal code
        arg 2: the minimal surface
        arg 3: the maximum rent/price
        arg 4: type of the add (1 -> location, 2 -> sell)
        arg 5: the owner_id of the search (the user making the search)
        arg 6: nb_room_min, minimum number of rooms
        """
        _cp = []
        if type(cp) is list:
            for c in cp:
                _cp.append(self.get_location(c))
        else:
            _cp.append(self.get_location(cp))

        SEARCH_PAYLOAD = {
            "pageIndex": 1,
            "pageSize": 50000,
            "query": {
                "bedrooms": [],
                "includeNewConstructions": True,
                "inseeCodes": _cp,
                "maximumPrice": max_price,
                "minimumLivingArea": min_surf,
                "realtyTypes": 3,
                "rooms": list(range(nb_room_min, 5)),
                "sortBy": 0,
                "transactionType": self._map_type(ad_type)
            }
        }

        SEARCH_URL = "https://api-seloger.svc.groupe-seloger.com/api/v1/listings/search"

        r = requests.post(SEARCH_URL, data=json.dumps(SEARCH_PAYLOAD), headers=self.headers)
        data = r.json()
        ret = {
            'id': [],
            'source': self.website
        }
        if raw:
            ret['raw'] = data
        for i in data['items']:
            ret['id'].append(i['id'])
        return ret


def search(params):
    write_result_in_file = False
    process_ad_from_file = True

    if process_ad_from_file:
        with open('data/sel2/request.json', 'r') as req_file:
            r = json.loads(req_file.read())
    else:
        seloger = SeLogerAds()
        r = seloger.search(
            cp=['75014', '75010', '75013', '75018'],
            min_surf=25,
            max_price=320000,
            ad_type='sell',
            nb_room_min=2
        )

        if write_result_in_file:
            with open("data/sel2/request.json", "w") as req_file:
                req_file.write(json.dumps(r))

    ids = r.get("id", [])
    items = r.get("raw", {}).get("items")
    id_count = len(ids)
    item_count = len(items)
    assert(id_count == item_count)

    logging.info("{} ads received.".format(id_count))

    for id in ids:
        logging.info("process ad {}".format(id))
        ad_filename = "data/sel2/{}.json".format(id)
        if process_ad_from_file:
            with open(ad_filename, 'r') as ad_file:
                ad = json.loads(ad_file.read())
        else:
            ad = seloger.get_ad_details(id, raw=True)['raw']

            if write_result_in_file:
                with open(ad_filename, 'w') as ad_file:
                    ad_file.write(json.dumps(ad))

#from pprint import pprint
#
#seloger = SeLogerAds()
#
#r = seloger.get_location('75014')
#pprint(r)
#
#r = seloger.count(
#    cp=['75014', '75010', '75013', '75018'],
#    min_surf=25,
#    max_price=320000,
#    ad_type='sell',
#    nb_room_min=2
#)
#pprint(r)
#
#r = seloger.search(
#    cp=['75014', '75010', '75013', '75018'],
#    min_surf=25,
#    max_price=320000,
#    ad_type='sell',
#    nb_room_min=2
#)
#pprint(r)
#
#for id in r['id']:
#    pprint(seloger.get_ad_details(id))