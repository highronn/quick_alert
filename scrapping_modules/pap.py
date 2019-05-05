import requests
import time
from urllib.parse import unquote, urlencode
from datetime import datetime

from models import quick_alert_db

from peewee import (
    CharField,
    IntegerField,
    TextField,
    DateTimeField,
    BigIntegerField,
    BooleanField,
    FloatField,

    Model,

    IntegrityError
)

AD_REQUIRED_FIELDS = {
    "id": BigIntegerField(null=False),
    "date_classement": DateTimeField(null=True, default=None),
    "typebien": CharField(null=True, default=None),
    "prix": IntegerField(null=True, default=None),
    "surface": IntegerField(null=True, default=None),
    "nb_pieces": IntegerField(null=True, default=None),
    "nb_chambres_max": IntegerField(null=True, default=None),
    "telephone": CharField(null=True, default=None),
    "city": CharField(null=True, default=None),
    "nouvelle_annonce": BooleanField(null=True, default=False),
    "lat": FloatField(null=True, default=False),
    "lng": FloatField(null=True, default=False),
    "classe_energie": CharField(null=True, default=None),
    "visite_virtuelle": CharField(null=True, default=None),
    "nb_photos": IntegerField(null=True, default=None),
    "is_idf": BooleanField(null=True, default=False),
    "place_lat": FloatField(null=True, default=False),
    "place_lng": FloatField(null=True, default=False),
    "place_title": CharField(null=True, default=None),
    "place_slug": CharField(null=True, default=None),
    "place_id": CharField(null=True, default=None),
    "link": CharField(null=True, default=None),
    "texte": TextField(null=True, default=None),
}

class AdPap(Model):
    class Meta:
        database = quick_alert_db
        db_table = 'sales_pap_buffer_in'


#class AdPapConf(Model):
#    class Meta:
#        database = quick_alert_db
#        db_table = 'pap_req_config'
#
#    id = CharField(unique=True, primary_key=True)
#    limit_date = DateTimeField(null=False)

header = {
    'X-Device-Gsf': '36049adaf18ade77',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; D5803 Build/MOB30M.Z1)',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip'
}

def init_models():
    for name, typ in AD_REQUIRED_FIELDS.items():
        AdPap._meta.add_field(name, typ)

    AdPap.create_table(safe=True)
    #AdPapConf.create_table(safe=True)


def search(parameters):
    # Préparation des paramètres de la requête
    payload = {
        #'recherche[prix][min]': parameters['price'][0],  # Loyer min
        #'recherche[prix][max]': parameters['price'][1],  # Loyer max
        #'recherche[surface][min]': parameters['surface'][0],  # Surface min
        #'recherche[surface][max]': parameters['surface'][1],  # Surface max
        #'recherche[nb_pieces][min]': parameters['rooms'][0],  # Pièces min
        #'recherche[nb_chambres][min]': parameters['bedrooms'][0],  # Chambres min
        'size': 200,
        'page': 1
    }

    wait_time = max(parameters.get("wait_time", 0), 0)

    # Insertion des paramètres propres à PAP
    payload.update(parameters['pap'])

    params = urlencode(payload)

    # Ajout des villes
    for city in parameters['cities']:
        params += "&recherche[geo][ids][]=%s" % place_search(city[1])

    request = requests.get("https://ws.pap.fr/immobilier/annonces", params=unquote(params), headers=header)
    #print("URI = {}".format(request.url))
    data = request.json()

    #print(data)

    with open("output.json", "w+") as output:
        output.write(str(data))

    for ad in data['_embedded']['annonce']:
        ad_id = ad.get('id')

        print("Handle ad {}".format(ad_id))

        _request = requests.get("https://ws.pap.fr/immobilier/annonces/{}".format(ad_id), headers=header)
        _data = _request.json()

        photos = list()
        if ad.get("nb_photos") > 0:
            for photo in ad["_embedded"]['photo']:
                photos.append(photo['_links']['self']['href'])

        ad_place = _data["_embedded"]['place'][0]
        ad_marker = _data['marker']

        ad_fields = dict(
            id = ad_id,
            date_classement = datetime.fromtimestamp(_data.get("date_classement")),
            typebien = ad.get("typebien"),
            prix = ad.get('prix'),
            surface = ad.get('surface'),
            nb_pieces = ad.get('nb_pieces'),
            nb_chambres_max = ad.get('nb_chambres_max'),
            telephone = _data.get("telephones")[0].replace('.', '') if len(_data.get("telephones")) > 0 else None,
            city = ad_place['title'],
            nouvelle_annonce = ad.get("nouvelle_annonce"),
            lat = ad_marker.get("lat") if ad_marker else None,
            lng = ad_marker.get("lng") if ad_marker else None,
            classe_energie = _data.get('classe_energie'),
            visite_virtuelle = ad.get('visite_virtuelle'),
            nb_photos = ad["nb_photos"],
            is_idf = ad_place.get('is_idf'),
            place_lat = float(ad_place.get('lat')),
            place_lng = float(ad_place.get('lng')),
            place_title = ad_place.get('title'),
            place_slug = ad_place.get('slug'),
            place_id = ad_place.get('id'),
            link = ad["_links"]['desktop']['href'],
            texte = str(_data.get("texte")),
        )

        #print("[\n{}]\n".format(",\n".join("{}: {}".format(k,v) for k,v in ad_fields.items())))

        try:
            ad_model = AdPap.create(**ad_fields)
            # ad_model.save()
        except IntegrityError as error:
            logging.info("ERROR: " + str(error))

        time.sleep(wait_time/1000.0)


def place_search(zipcode):
    """Retourne l'identifiant PAP pour un code postal donné"""

    payload = {
        "recherche[cible]": "pap-recherche-ac",
        "recherche[q]": zipcode
    }

    request = requests.get("https://ws.pap.fr/gis/places", params=payload, headers=header)
    return request.json()['_embedded']['place'][0]['id']