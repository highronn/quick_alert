from datetime import datetime
import logging
import math

from models import quick_alert_db

import requests
import xml.etree.ElementTree as ET
from peewee import (
    CharField,
    TextField,
    DateTimeField,
    BigIntegerField,
    BooleanField,

    Model,

    IntegrityError
)

AD_REQUIRED_FIELDS = {
    #"idAnnonce": BigIntegerField(primary_key=True, unique=True),
    "idAnnonce": BigIntegerField(null=False),
    "dateinsert": DateTimeField(null=False, default=datetime.now),
    "idTiers": CharField(null=True, default=None),
    "idAgence": CharField(null=True, default=None),
    "idPublication": CharField(null=True, default=None),
    "idTypeTransaction": CharField(null=True, default=None),
    "idTypeBien": CharField(null=True, default=None),
    "dtFraicheur": DateTimeField(null=True, default=None),
    "dtCreation": DateTimeField(null=True, default=None),
    "titre": CharField(null=True, default=None),
    "libelle": CharField(null=True, default=None),
    "descriptif": TextField(null=True, default=None),
    "prix": CharField(null=True, default=None),
    "prixUnite": CharField(null=True, default=None),
    "prixMention": CharField(null=True, default=None),
    "nbPiece": CharField(null=True, default=None),
    "nbChambre": CharField(null=True, default=None),
    "surface": CharField(null=True, default=None),
    "surfaceUnite": CharField(null=True, default=None),
    "idPays": CharField(null=True, default=None),
    "pays": CharField(null=True, default=None),
    "cp": CharField(null=True, default=None),
    "codeInsee": CharField(null=True, default=None),
    "ville": CharField(null=True, default=None),
    "logoTnyUrl": CharField(null=True, default=None),
    "logoBigUrl": CharField(null=True, default=None),
    "firstThumb": CharField(null=True, default=None),
    "permaLien": CharField(null=True, default=None),
    "latitude": CharField(null=True, default=None),
    "longitude": CharField(null=True, default=None),
    "llPrecision": CharField(null=True, default=None),
    "typeDPE": CharField(null=True, default=None),
    "consoEnergie": CharField(null=True, default=None),
    "bilanConsoEnergie": CharField(null=True, default=None),
    "emissionGES": CharField(null=True, default=None),
    "bilanEmissionGES": CharField(null=True, default=None),
    "siLotNeuf": BooleanField(null=True, default=False),
    "siMandatExclusif": BooleanField(null=True, default=False),
    "siMandatStar": BooleanField(null=True, default=False),
    "contact/siAudiotel":  BooleanField(null=True, default=False),
    "contact/idPublication": CharField(null=True, default=None),
    "contact/nom": CharField(null=True, default=None),
    "contact/rcsSiren": CharField(null=True, default=None),
    "contact/rcsNic": CharField(null=True, default=None),
    "nbsallesdebain": CharField(null=True, default=None),
    "nbsalleseau": CharField(null=True, default=None),
    "nbtoilettes": CharField(null=True, default=None),
    "sisejour": BooleanField(null=True, default=False),
    "surfsejour": CharField(null=True, default=None),
    "anneeconstruct": CharField(null=True, default=None),
    "nbparkings": CharField(null=True, default=None),
    "nbboxes": CharField(null=True, default=None),
    "siterrasse": BooleanField(null=True, default=False),
    "nbterrasses": CharField(null=True, default=None),
    "sipiscine": BooleanField(null=True, default=False),
    "proximite": TextField(null=True, default=None)
}


class AdSeLoger(Model):
    class Meta:
        database = quick_alert_db
        db_table = 'sales_sel_buffer_in'
        primary_key = False


class AdSeLogerConf(Model):
    class Meta:
        database = quick_alert_db
        db_table = 'sel_req_config'

    id = CharField(unique=True, primary_key=True)
    limit_date = DateTimeField(null=False)


def convert_api_field_to_db_col(field_name):
    return field_name.replace('/', '_').lower()


def init_models():
    for name, typ in AD_REQUIRED_FIELDS.items():
        AdSeLoger._meta.add_field(
            convert_api_field_to_db_col(name),
            typ
        )

    AdSeLoger.create_table(safe=True)
    AdSeLogerConf.create_table(safe=True)


def search(params):
    AD_IDS = set()

    # ---------------------------
    def log_batch_info(batch_id, page_id):
        logging.info("batch {}: process page {}".format(
            batch_id,
            page_id
        ))

    def read_sel_ads(req_params, page_id, limit_date, db_insert=True):
        sel_api_host = "http://ws.seloger.com/search.xml"
        headers = {'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; D5803 Build/MOB30M.Z1)'}
        req_params['SEARCHpg'] = page_id
        response = requests.get(sel_api_host, params=req_params, headers=headers)
        xml_root = ET.fromstring(response.text)

        for adNode in xml_root.findall('annonces/annonce'):
            ad_fields = {}
            ad_fields["dateinsert"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            for field in AD_REQUIRED_FIELDS:
                if field == "dateinsert":
                    continue

                field_value = adNode.findtext(field)
                db_col = convert_api_field_to_db_col(field)
                ad_fields[db_col] = field_value if field_value else None

            if limit_date and ad_fields["dtcreation"] <= limit_date:
                return -1

            #logging.info("id: {} dt: {}".format(ad_fields["idannonce"], ad_fields["dtcreation"]))

            if db_insert:
                try:
                    ad_model = AdSeLoger.create(**ad_fields)
                    # ad_model.save()
                except IntegrityError as error:
                   logging.info("ERROR: " + str(error))

            id_annonce = ad_fields["idannonce"]
            if id_annonce in AD_IDS:
                logging.error("annonce id [{}] already received".format(id_annonce))
            AD_IDS.add(id_annonce)

        next_page_url = xml_root.findtext("pageSuivante")
        has_next_page = (next_page_url is not None)
        return (page_id+1) if has_next_page else -1

    # ---------------------------
    ## config process
    use_db_insertion = True

    # custom request params
    req_params = params['request']

    # start_page
    page_id = int(params.get("start_page", 1))
    page_id = page_id if page_id > 0 else 1

    if "SEARCHpg" in req_params:
        logging.warning("'SEARCHpg' param will be ignored. Use 'start_page' instead")

    logging.info("start page: {}".format(page_id))

    # max pages
    max_pages = params.get("max_pages", math.inf)
    max_pages = math.inf if max_pages <= 0 else max_pages
    batch_id = 1

    config_id = params["config_id"]
    assert config_id, "no 'config_id' parameter set"

    only_new_ads = params.get("only_new_ads", False)
    limit_date = None

    # max_pages param has priority over only_new_ads
    use_limit_date = only_new_ads and max_pages == math.inf
    if use_limit_date:
        if 'tri' not in req_params or req_params['tri'] != 'd_dt_crea':
            logging.warning("force parameter 'tri' = 'd_dt_crea'")
            req_params['tri'] = 'd_dt_crea'

        try:
            config = AdSeLogerConf.get(AdSeLogerConf.id == config_id)
            limit_date = config.limit_date.strftime('%Y-%m-%dT%H:%M:%S')
            logging.info("using limit date '{}'".format(limit_date))
        except Exception:
            logging.error("no config found for '{}'. no limit date will be used".format(config_id))
    else:
        limit_date = None

    # request process
    log_batch_info(batch_id, page_id)
    page_id = read_sel_ads(req_params, page_id, limit_date, db_insert=use_db_insertion)

    while (page_id > 0) and (batch_id < max_pages):
        batch_id += 1
        log_batch_info(batch_id, page_id)
        page_id = read_sel_ads(req_params, page_id, limit_date, db_insert=use_db_insertion)

    if use_limit_date:
        new_limit_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        AdSeLogerConf.replace(id=config_id, limit_date=new_limit_date).execute()
        logging.info("set '{}' config new limit date to '{}'".format(config_id, new_limit_date))

    logging.info("{} ads processed.".format(len(AD_IDS)))
