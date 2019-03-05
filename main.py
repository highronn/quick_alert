#!/usr/bin/env python3

import os
# import sys
import json
# import models
# import trello_module
import logging
# from scrapping_modules import logic_immo
from scrapping_modules import seloger
# from scrapping_modules import leboncoin
# from scrapping_modules import pap


logging.basicConfig(level=logging.INFO)

script_path = os.path.abspath(__file__)
os.chdir(os.path.dirname(script_path))

# models.create_tables()

SELOGER_CONF_LIST = [
    "data/paris01.json",
    "data/paris02.json",
    "data/paris03.json",
    "data/paris04.json",
    "data/paris05.json",
    "data/paris06.json",
    "data/paris07.json",
    "data/paris08.json",
    "data/paris09.json",
    "data/paris10.json",
    "data/paris11.json",
    "data/paris12.json",
    "data/paris13.json",
    "data/paris14.json",
    "data/paris15.json",
    "data/paris16.json",
    "data/paris17.json",
    "data/paris18.json",
    "data/paris19.json",
    "data/paris20.json",
]

logging.info("Retrieving from seloger")
seloger.init_models()

for conf in SELOGER_CONF_LIST:
    with open(conf, encoding='utf-8') as parameters:
        logging.info("read conf file: {}".format(conf))
        parameters = json.load(parameters)
        seloger.search(parameters)
