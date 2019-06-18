#!/usr/bin/env python3

import os
import json
import logging
from scrapping_modules import sel_v2



logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

script_path = os.path.abspath(__file__)
os.chdir(os.path.dirname(script_path))



sel_v2.SeLogerAds.get_location(0,75018)

sel_v2.SeLogerAds.search(75018,0,0,10000,"rent",0)

