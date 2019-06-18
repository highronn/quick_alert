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
    pap.get_expiration()
    print ("{}" .format(threadName))

# Create two threads as follows
try:
   _thread.start_new_thread( print_time, ("Thread-1",  ) )
   time.sleep(1.5)
   _thread.start_new_thread( print_time, ("Thread-2",  ) )
except:
   print ("Error: unable to start thread")

while 1:
   pass