#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import logging
from scrapping_modules import pap 


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

script_path = os.path.abspath(__file__)
os.chdir(os.path.dirname(script_path))


for a in range(1,600):
    with open("data/pap_model.json", encoding='utf-8') as parameters_data:
        parameters = json.load(parameters_data)
        pap.init_models()
        if pap.search(parameters) == -1 :
            break

    