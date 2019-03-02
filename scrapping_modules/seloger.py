from datetime import datetime

from models import quick_alert_db

import requests
import xml.etree.ElementTree as ET
from peewee import (
    CharField,
    TextField,
    DateTimeField,
    Model
)

AD_REQUIRED_FIELDS = {
    #"dateinsert": DateTimeField(null=True, default=""),
    "idTiers": CharField(null=True, default=""),
    "idAnnonce": CharField(null=True, default=""),
    "idAgence": CharField(null=True, default=""),
    "idPublication": CharField(null=True, default=""),
    "idTypeTransaction": CharField(null=True, default=""),
    "idTypeBien": CharField(null=True, default=""),
    "dtFraicheur": DateTimeField(null=True, default=None),
    "dtCreation": DateTimeField(null=True, default=None),
    "titre": CharField(null=True, default=""),
    "libelle": CharField(null=True, default=""),
    "descriptif": TextField(),
    "prix": CharField(null=True, default=""),
    "prixUnite": CharField(null=True, default=""),
    "prixMention": CharField(null=True, default=""),
    "nbPiece": CharField(null=True, default=""),
    "nbChambre": CharField(null=True, default=""),
    "surface": CharField(null=True, default=""),
    "surfaceUnite": CharField(null=True, default=""),
    "idPays": CharField(null=True, default=""),
    "pays": CharField(null=True, default=""),
    "cp": CharField(null=True, default=""),
    "codeInsee": CharField(null=True, default=""),
    "ville": CharField(null=True, default=""),
    "logoTnyUrl": CharField(null=True, default=""),
    "logoBigUrl": CharField(null=True, default=""),
    "firstThumb": CharField(null=True, default=""),
    "permaLien": CharField(null=True, default=""),
    "latitude": CharField(null=True, default=""),
    "longitude": CharField(null=True, default=""),
    "llPrecision": CharField(null=True, default=""),
    "typeDPE": CharField(null=True, default=""),
    "consoEnergie": CharField(null=True, default=""),
    "bilanConsoEnergie": CharField(null=True, default=""),
    "emissionGES": CharField(null=True, default=""),
    "bilanEmissionGES": CharField(null=True, default=""),
    "siLotNeuf": CharField(null=True, default=""),
    "siMandatExclusif": CharField(null=True, default=""),
    "siMandatStar": CharField(null=True, default=""),
    "contact/siAudiotel": CharField(null=True, default=""),
    "contact/idPublication": CharField(null=True, default=""),
    "contact/nom": CharField(null=True, default=""),
    "contact/rcsSiren": CharField(null=True, default=""),
    "contact/rcsNic": CharField(null=True, default=""),
    "nbsallesdebain": CharField(null=True, default=""),
    "nbsalleseau": CharField(null=True, default=""),
    "nbtoilettes": CharField(null=True, default=""),
    "sisejour": CharField(null=True, default=""),
    "surfsejour": CharField(null=True, default=""),
    "anneeconstruct": CharField(null=True, default=""),
    "nbparkings": CharField(null=True, default=""),
    "nbboxes": CharField(null=True, default=""),
    "siterrasse": CharField(null=True, default=""),
    "nbterrasses": CharField(null=True, default=""),
    "sipiscine": CharField(null=True, default=""),
    "proximite": CharField(null=True, default="")
}


class AdSeLoger(Model):
    class Meta:
        database = quick_alert_db
        db_table = 'sales_sel_buffer_in'

for name, typ in AD_REQUIRED_FIELDS.items():
    AdSeLoger._meta.add_field(
        name.replace('/', '_').lower(),
        typ
    )


AdSeLoger.create_table()

def search(parameters):
    # preparing request params
    payload = {
        'px_loyermin': parameters['price'][0],
        'px_loyermax': parameters['price'][1],
        'surfacemin': parameters['surface'][0],
        'surfacemax': parameters['surface'][1],
        # Si parameters['rooms'] = (2, 4) => "2,3,4"
        'nbpieces': list(range(parameters['rooms'][0], parameters['rooms'][1] + 1)),
        # Si parameters['bedrooms'] = (2, 4) => "2,3,4"
        'nb_chambres': list(range(parameters['bedrooms'][0], parameters['bedrooms'][1] + 1)),
        'ci': [int(cp[2]) for cp in parameters['cities']]
    }

    # adding seloger specific params
    payload.update(parameters['seloger'])

    headers = {'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; D5803 Build/MOB30M.Z1)'}
    request = requests.get("http://ws.seloger.com/search.xml", params=payload, headers=headers)

    xml_root = ET.fromstring(request.text)

    for adNode in xml_root.findall('annonces/annonce'):
        # Seconde requête pour obtenir la description de l'annonce
        #_payload = {'noAudiotel': 1, 'idAnnonce': adNode.findtext('idAnnonce')}
        #_request = requests.get("http://ws.seloger.com/annonceDetail_4.0.xml", params=_payload, headers=headers)
        #photos = list()
        #for photo in adNode.find("photos"):
        #    photos.append(photo.findtext("stdUrl"))

        #annonce, created = Annonce.create_or_get(
        #    id='seloger-' + adNode.find('idAnnonce').text,
        #    site='SeLoger',
        #    # SeLoger peut ne pas fournir de titre pour une annonce T_T
        #    title="Appartement " + adNode.findtext('nbPiece') + " pièces" if adNode.findtext('titre') is None else adNode.findtext('titre'),
        #    description=ET.fromstring(_request.text).findtext("descriptif"),
        #    telephone=ET.fromstring(_request.text).findtext("contact/telephone"),
        #    created=datetime.strptime(adNode.findtext('dtCreation'), '%Y-%m-%dT%H:%M:%S'),
        #    price=adNode.find('prix').text,
        #    charges=adNode.find('charges').text,
        #    surface=adNode.find('surface').text,
        #    rooms=adNode.find('nbPiece').text,
        #    bedrooms=adNode.find('nbChambre').text,
        #    city=adNode.findtext('ville'),
        #    link=adNode.findtext('permaLien'),
        #    picture=photos
        #)

        #if created:
        #    annonce.save()
        ad_fields = {}
        #ad_fields["dateinsert"] = datetime.now().strftime('%Y-%m-%d')

        for field in AD_REQUIRED_FIELDS:
            field_value = adNode.findtext(field)
            ad_fields[field.lower()] = field_value if field_value else ""

        #print("RONY {}".format(ad_fields["descriptif"]))
        ad_fields["descriptif"] = "FUCK"
        
        ad_model = AdSeLoger.create(**ad_fields)
        ad_model.save()
        print("AD: {}\n".format(ad_fields))

        exit(0)

