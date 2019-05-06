#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import logging
from scrapping_modules import pap


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

script_path = os.path.abspath(__file__)
os.chdir(os.path.dirname(script_path))


with open("data/pap_75001_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75002_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75003_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75004_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75005_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75006_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75007_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75008_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75009_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75010_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75011_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75012_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75013_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75014_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75015_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75016_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75017_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75018_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75019_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75020_rent.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75001_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75002_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75003_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75004_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75005_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75006_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75007_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75008_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75009_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75010_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75011_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75012_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75013_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75014_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75015_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75016_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75017_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75018_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75019_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)

with open("data/pap_75020_sale.json", encoding='utf-8') as parameters_data:
    parameters = json.load(parameters_data)
    pap.init_models()
    pap.search(parameters)