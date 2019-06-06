# coding: utf-8

from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
import math
import time

from models import dev_db

import requests
import xml.etree.ElementTree as ET
from peewee import (
    CharField,
    TextField,
    DateTimeField,
    BigIntegerField,
    BooleanField,
    IntegerField,
    DecimalField,
    IntegrityError,
    Model,
    MySQLDatabase
)

start_date_c = (datetime.now()+ relativedelta(minutes=-5)).strftime('%Y-%m-%d %H:%M:00')
start_date_m = (datetime.now()+ relativedelta(days=-1)).strftime('%Y-%m-%d 00:00:00')

quick_alert_db = MySQLDatabase(
    'quickalert',
    user='quickalert',
    password='quickalert',
    host='myquickalertdbinstance.cqlkfxu7awoj.eu-west-3.rds.amazonaws.com',
    port=3306
)

#db = dev_db
db = quick_alert_db

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
    "permaLien": CharField(null=True, default=None),
    "latitude": CharField(null=True, default=None),
    "longitude": CharField(null=True, default=None),
    "llPrecision": CharField(null=True, default=None),
    "typeDPE": CharField(null=True, default=None),
    "consoEnergie": CharField(null=True, default=None),
    "bilanConsoEnergie": CharField(null=True, default=None),
    "emissionGES": CharField(null=True, default=None),
    "bilanEmissionGES": CharField(null=True, default=None),
    "siLotNeuf": CharField(null=True, default=False),
    "siMandatExclusif": CharField(null=True, default=False),
    "siMandatStar": CharField(null=True, default=False),
    "contact/siAudiotel":  BooleanField(null=True, default=False),
    "contact/idPublication": CharField(null=True, default=None),
    "contact/nom": CharField(null=True, default=None),
    "contact/rcsSiren": CharField(null=True, default=None),
    "contact/rcsNic": CharField(null=True, default=None),
    "nbsallesdebain": CharField(null=True, default=None),
    "nbsalleseau": CharField(null=True, default=None),
    "nbtoilettes": CharField(null=True, default=None),
    "sisejour": CharField(null=True, default=False),
    "surfsejour": CharField(null=True, default=None),
    "anneeconstruct": CharField(null=True, default=None),
    "nbparkings": CharField(null=True, default=None),
    "nbboxes": CharField(null=True, default=None),
    "siterrasse": CharField(null=True, default=False),
    "nbterrasses": CharField(null=True, default=None),
    "sipiscine": CharField(null=True, default=False),
    "proximite": TextField(null=True, default=None)
}


class AdSeLoger(Model):
    class Meta:
        database = db
        db_table = 't_sel_ads_buffer_in'
        primary_key = False


class AdSeLogerConf(Model):
    class Meta:
        database = db
        db_table = 't_sel_script_info'

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
        logging.info("{} - batch {}: process page {}".format(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            batch_id,
            page_id
        ))
        

    def read_sel_ads(req_params, page_id, limit_date, db_insert=True):
        sel_api_host = "http://ws.seloger.com/search.xml"
        headers = {'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; D5803 Build/MOB30M.Z1)'}
        req_params['SEARCHpg'] = page_id
        
        ##############################################################################################""
        #response = requests.get(sel_api_host, params=req_params, headers=headers)
        #xml_root = ET.fromstring(response.text)
        ##############################################################################################""
        v_timer = 0
        v_wait = 5
        xml_root = None
        for i in range(0,10):
            try:
                response = requests.get(sel_api_host, params=req_params, headers=headers, timeout=5)
                xml_root = ET.fromstring(response.text)
            except:
                #logging.info("ERROR: Database error connection")
                time.sleep(v_timer)
                v_timer += v_wait   
                db.close     
                init_models()    
                print ("Request Error - Try again - Waiting : {} sec(s)".format(v_timer))            
                continue
            else:
                break 
        else:
            return




        ##############################################################################################""
        for adNode in xml_root.findall('annonces/annonce'):
            ad_fields = {}
            ad_fields["dateinsert"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            for field in AD_REQUIRED_FIELDS:
                if field == "dateinsert":
                    continue

                field_value = adNode.findtext(field)
                db_col = convert_api_field_to_db_col(field)
                ad_fields[db_col] = field_value if field_value else None

            id_annonce = ad_fields["idannonce"]
            dt_refresh = ad_fields["dtfraicheur"]
            dt_creation = ad_fields["dtcreation"]

            #if dt_refresh < dt_creation:
            #    logging.warning("annonce [{}] has inconsistent dates [{} < {}]".format(
            #        id_annonce,
            #        dt_refresh,
            #        dt_creation
            #    ))

            """ 
            if limit_date and dt_creation <= limit_date and req_params['tri'] == 'd_dt_crea' :
                return -1
            elif limit_date and dt_refresh <= limit_date and req_params['tri'] == 'd_dt_maj' :
                return -1
            """

            #logging.info("id: {} dt: {}".format(id_annonce, dt_creation))

            if db_insert:
                try:
                    ad_model = AdSeLoger.create(**ad_fields)
                    # ad_model.save()
                except IntegrityError as error:
                   logging.info("ERROR: " + str(error))

            #if id_annonce in AD_IDS:
            #    logging.error("annonce [{}] already received".format(id_annonce))
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
    logging.info("Retrieve ad from : {} - {} - {}".format( req_params['cp'],req_params['tri'],req_params['idtt']))
    #print ("Retrieve ad from : {},{},{}".format( req_params['cp'],req_params['tri'],req_params['idtt']))

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
        if 'tri' not in req_params or req_params['tri'] not in ['d_dt_crea','d_dt_maj']:
            logging.warning("force parameter 'tri' = 'd_dt_crea' or 'tri' = 'd_dt_maj' ")
            #req_params['tri'] = 'd_dt_crea'

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
    """ 
    if use_limit_date and req_params['tri'] == 'd_dt_crea':
        new_limit_date = start_date_c
        AdSeLogerConf.replace(id=config_id, limit_date=new_limit_date).execute()
        logging.info("set '{}' config new limit date for d_dt_crea to '{}'".format(config_id, new_limit_date))
    elif use_limit_date and req_params['tri'] == 'd_dt_maj':
        new_limit_date = start_date_m
        AdSeLogerConf.replace(id=config_id, limit_date=new_limit_date).execute()
        logging.info("set '{}' config new limit date for d_dt_maj to '{}'".format(config_id, new_limit_date))
    """
    logging.info("{} ads processed.".format(len(AD_IDS)))
