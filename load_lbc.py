#!/usr/bin/env python3
#############################################################
# IMPORT FUNCTIONS
##############################################################
import os
import json
import logging
from scrapping_modules import sel
from scrapping_modules import lbc
from scrapping_modules import pap
import threading

#############################################################
# PARAMETERS
##############################################################
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
script_path = os.path.abspath(__file__)
os.chdir(os.path.dirname(script_path))
script = lbc

#############################################################
# DEFINE FUNCTION FOR THE THREAD
##############################################################
def ThreadScript(threadid):
   for a in range(max_launch_per_tread):
        with open("data/lbc_model.json", encoding='utf-8') as parameters_data:
            parameters = json.load(parameters_data)
            script.init_models()
            if script.search(parameters,threadid) == -1 :
                break

#############################################################
# CLEAN THREAD_ID
##############################################################
script.AdBatchTable.update( thread=0).where(script.AdBatchTable.id == 'lbc%' and script.AdBatchTable.thread != 999 ).execute()

#############################################################
# MULTI THREADING
##############################################################
nb_thread = 30
max_batch = 13000
max_launch_per_tread = round(max_batch/nb_thread)
print("nb_thread : {}      max_batch : {}      max_per_thread : {}".format(nb_thread,max_batch,max_launch_per_tread))
thread_list = []

for i in range(nb_thread):
    #print(i)
    thread = threading.Thread(target=ThreadScript, args=(i,))
    thread_list.append(thread)
    thread.start()
    #print(i)

for thread in thread_list:
    thread.join()
#############################################################
# CLEAN THREAD_ID
##############################################################
script.AdBatchTable.update( thread=0).where(script.AdBatchTable.id == 'lbc%' and script.AdBatchTable.thread != 999 ).execute()

print ("Thread has finished")
##############################################################