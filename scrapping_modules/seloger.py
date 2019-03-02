import requests
import xml.etree.ElementTree as ET
from models import Annonce
from datetime import datetime
'''module to retrieve seloger.com ads'''

AD_REQUIRED_FIELDS = [
    "idTiers",
    "idAnnonce",
    "idAgence",
    "idPublication",
    "idTypeTransaction",
    "idTypeBien",
    "dtFraicheur",
    "dtCreation",
    "titre",
    "libelle",
    "descriptif",
    "prix",
    "prixUnite",
    "prixMention",
    "nbPiece",
    "nbChambre",
    "surface",
    "surfaceUnite",
    "idPays",
    "pays",
    "cp",
    "codeInsee",
    "ville",
    "logoTnyUrl",
    "logoBigUrl",
    "firstThumb",
    "permaLien",
    "latitude",
    "longitude",
    "llPrecision",
    "typeDPE",
    "consoEnergie",
    "bilanConsoEnergie",
    "emissionGES",
    "bilanEmissionGES",
    "siLotNeuf",
    "siMandatExclusif",
    "siMandatStar",
    "contact/siAudiotel",
    "contact/idPublication",
    "contact/nom",
    "contact/rcsSiren",
    "contact/rcsNic",
    "nbsallesdebain",
    "nbsalleseau",
    "nbtoilettes",
    "sisejour",
    "surfsejour",
    "anneeconstruct",
    "nbparkings",
    "nbboxes",
    "siterrasse",
    "nbterrasses",
    "sipiscine",
    "proximite",
]

def search(parameters):
    # Preparing request params
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

    # Adding seloger specific params
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
            ad_fields[field] = adNode.findtext(field)

        print("AD: {}\n".format(ad_fields))

