#!/usr/bin/env python3

import os
import json
import logging
from scrapping_modules import sel
from scrapping_modules import pap


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

script_path = os.path.abspath(__file__)
os.chdir(os.path.dirname(script_path))


pap.get_expiration()
