#!/usr/bin/env python3

import os
import logging
import threading
import json

from scrapping_modules import pap as scrapping_module


def scrap(tasker_id, runs_count):
    for _ in range(runs_count):
        with open("data/pap_model.json", encoding='utf-8') as json_config:
            parameters = json.load(json_config)
            if scrapping_module.search(parameters, tasker_id) == -1:
                break


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    script_path = os.path.abspath(__file__)
    os.chdir(os.path.dirname(script_path))

    scrapping_module.AdBatchTable.update(thread=0).where(id == 'pap%').execute()

    tasker_count = 1
    total_runs = 13000
    runs_per_tasker = round(total_runs/tasker_count)

    print("tasker_count [{}] runs_per_tasker [{}]".format(
        tasker_count,
        runs_per_tasker
    ))

    scrapping_module.init_models()

    thread_list = [threading.Thread(target=scrap, args=(id, runs_per_tasker)) for id in range(tasker_count)]

    # start all threads
    for thread in thread_list:
        thread.start()

    # wait all threads to finish
    for thread in thread_list:
        thread.join()

    # Lock task infos
    scrapping_module.AdBatchTable.update(thread=0).where(id == 'pap%').execute()

    print("All tasks done.")
