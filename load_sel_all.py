#!/usr/bin/env python3

import os
import json
import logging
from scrapping_modules import sel


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

script_path = os.path.abspath(__file__)
os.chdir(os.path.dirname(script_path))

with open("data/sel_075_1_crea.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_075_2_crea.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_077_1_crea.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_077_2_crea.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_078_1_crea.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_078_2_crea.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_091_1_crea.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_091_2_crea.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_092_1_crea.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_092_2_crea.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_093_1_crea.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_093_2_crea.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_094_1_crea.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_094_2_crea.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_095_1_crea.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_095_2_crea.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

######################################################################################
######################################################################################

with open("data/sel_075_1_maj.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_075_2_maj.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_077_1_maj.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_077_2_maj.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_078_1_maj.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_078_2_maj.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_091_1_maj.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_091_2_maj.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_092_1_maj.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_092_2_maj.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_093_1_maj.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_093_2_maj.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_094_1_maj.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_094_2_maj.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_095_1_maj.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)

with open("data/sel_095_2_maj.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    sel.init_models()
    sel.search(parameters)
