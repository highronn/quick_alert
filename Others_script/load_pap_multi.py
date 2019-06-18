#!/usr/bin/env python3

import os
import json
import logging
from scrapping_modules import sel
from scrapping_modules import pap


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
script_path = os.path.abspath(__file__)
os.chdir(os.path.dirname(script_path))

import _thread
import time

# Define a function for the thread
def print_time( threadName):
    with open("data/pap_92_3_rent.json", encoding='utf-8') as parameters_data:
        parameters = json.load(parameters_data)
        pap.init_models()
        pap.search(parameters)
        print ("{}" .format(threadName))


def print_time2( threadName):
    with open("data/pap_92_2_rent.json", encoding='utf-8') as parameters_data:
        parameters = json.load(parameters_data)
        pap.init_models()
        pap.search(parameters)
        print ("{}" .format(threadName))

# Create two threads as follows
try:
   _thread.start_new_thread( print_time, ("Thread-1",  ) )
   _thread.start_new_thread( print_time2, ("Thread-2",  ) )
except:
   print ("Error: unable to start thread")

while 1:
   pass