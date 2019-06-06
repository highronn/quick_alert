#!/usr/bin/env python3

import os
# import sys
import json
# import models
# import trello_module
import logging
# from scrapping_modules import li
#from scrapping_modules import sel
#from scrapping_modules import sel2
#from scrapping_modules import lbc
from scrapping_modules import lbc_web
from scrapping_modules import pap
from pprint import pprint


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

script_path = os.path.abspath(__file__)
os.chdir(os.path.dirname(script_path))


for a in range(1,600):
    with open("data/lbc_model.json", encoding='utf-8') as parameters_data:
        parameters = json.load(parameters_data)
        lbc_web.init_models()
        if lbc_web.search(parameters) == -1 :
            break
        
    