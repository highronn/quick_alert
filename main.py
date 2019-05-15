#!/usr/bin/env python3

import os
# import sys
import json
# import models
# import trello_module
import logging
# from scrapping_modules import li
from scrapping_modules import sel
from scrapping_modules import lbc
from scrapping_modules import lbc_web
from scrapping_modules import pap


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

script_path = os.path.abspath(__file__)
os.chdir(os.path.dirname(script_path))

#with open("data/sel.json", encoding='utf-8') as parameters_data:
#    parameters = json.load(parameters_data)
#    sel.init_models()
#    sel.search(parameters)

#with open("data/pap.json", encoding='utf-8') as parameters_data:
#    parameters = json.load(parameters_data)
#    pap.init_models()
#    pap.search(parameters)

with open("data/lbc_web.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    #lbc_web.init_models()
    lbc_web.search(parameters)
