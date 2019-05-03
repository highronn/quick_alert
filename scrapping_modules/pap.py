import requests
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

    Model,

    IntegrityError
)

AD_REQUIRED_FIELDS = {
    "id": BigIntegerField(null=False),
    "date_classement": DateTimeField(null=True, default=None),
    # produit
    "typebien": CharField(null=True, default=None),
    "prix": IntegerField(null=True, default=None),
    "surface": IntegerField(null=True, default=None),
    "nb_pieces": IntegerField(null=True, default=None),
    "nb_chambres_max": IntegerField(null=True, default=None),
    # nb_photos
    # marker
    "telephone": CharField(null=True, default=None),
    "link": CharField(null=True, default=None),
    # slug
    # title
    # lat
    # lng
    # is_idf
    "city": CharField(null=True, default=None),
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

        ad_fields = dict(
            id = ad_id,
            date_classement = datetime.fromtimestamp(_data.get("date_classement")),
            typebien = ad.get("typebien"),
            prix = ad.get('prix'),
            surface = ad.get('surface'),
            nb_pieces = ad.get('nb_pieces'),
            nb_chambres_max = ad.get('nb_chambres_max'),
            telephone = _data.get("telephones")[0].replace('.', '') if len(_data.get("telephones")) > 0 else None,
            city = ad["_embedded"]['place'][0]['title'],
            link = ad["_links"]['desktop']['href'],
            texte = str(_data.get("texte")),
        )

        #print("[\n{}]\n".format(",\n".join("{}: {}".format(k,v) for k,v in ad_fields.items())))

        try:
            ad_model = AdPap.create(**ad_fields)
            # ad_model.save()
        except IntegrityError as error:
            logging.info("ERROR: " + str(error))


def place_search(zipcode):
    """Retourne l'identifiant PAP pour un code postal donné"""

    payload = {
        "recherche[cible]": "pap-recherche-ac",
        "recherche[q]": zipcode
    }

    request = requests.get("https://ws.pap.fr/gis/places", params=payload, headers=header)
    return request.json()['_embedded']['place'][0]['id']