from datetime import datetime

from models import quick_alert_db

import requests
import xml.etree.ElementTree as ET
from peewee import (
    CharField,
    TextField,
    BlobField,
    Model
)

AD_REQUIRED_FIELDS = {	
    "idTiers": CharField(),
    "idAnnonce": CharField(),
    "idAgence": CharField(),
    "idPublication": CharField(),
    "idTypeTransaction": CharField(),
    "idTypeBien": CharField(),
    "dtFraicheur": CharField(),
    "dtCreation": CharField(),
    "titre": CharField(),
    "libelle": CharField(),
    "descriptif": TextField(),
    "prix": CharField(),
    "prixUnite": CharField(),
    "prixMention": CharField(),
    "nbPiece": CharField(),
    "nbChambre": CharField(),
    "surface": CharField(),
    "surfaceUnite": CharField(),
    "idPays": CharField(),
    "pays": CharField(),
    "cp": CharField(),
    "codeInsee": CharField(),
    "ville": CharField(),
    "logoTnyUrl": CharField(null=True, default=""),
    "logoBigUrl": CharField(null=True, default=""),
    "firstThumb": CharField(),
    "permaLien": CharField(),
    "latitude": CharField(),
    "longitude": CharField(),
    "llPrecision": CharField(),
    "typeDPE": CharField(),
    "consoEnergie": CharField(),
    "bilanConsoEnergie": CharField(),
    "emissionGES": CharField(),
    "bilanEmissionGES": CharField(),
    "siLotNeuf": CharField(),
    "siMandatExclusif": CharField(),
    "siMandatStar": CharField(),
    "contact/siAudiotel": CharField(null=True, default=""),
    "contact/idPublication": CharField(null=True, default=""),
    "contact/nom": CharField(null=True, default=""),
    "contact/rcsSiren": CharField(null=True, default=""),
    "contact/rcsNic": CharField(null=True, default=""),
    "nbsallesdebain": CharField(),
    "nbsalleseau": CharField(),
    "nbtoilettes": CharField(),
    "sisejour": CharField(),
    "surfsejour": CharField(),
    "anneeconstruct": CharField(),
    "nbparkings": CharField(),
    "nbboxes": CharField(),
    "siterrasse": CharField(),
    "nbterrasses": CharField(),
    "sipiscine": CharField(),
    "proximite": CharField()
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
        
        for field in AD_REQUIRED_FIELDS:
            field_value = adNode.findtext(field)
            ad_fields[field.lower()] = field_value if field_value else ""

        #print("RONY {}".format(ad_fields["descriptif"]))
        ad_fields["descriptif"] = "FUCK"
        
        ad_model = AdSeLoger.create(**ad_fields)
        ad_model.save()
        print("AD: {}\n".format(ad_fields))
        exit(0)

