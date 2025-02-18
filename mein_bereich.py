import logging
import random
import re

from config import *
from resources import DATA_ACTION_PATTERN

# CONSTANTS
# ---------------------
# Name of the parent UI-Flow in Outsystems
UI_FLOW = "MainFlow"
# Name of the screen in Outsystems
SCREEN_NAME = "MeinBereich"
# All the script files, that contain references to aggregates or data actions
SCRIPT_SOURCES = [
    f"{UI_FLOW}.{SCREEN_NAME}",
    "CW.MeinBereichFaelle",
    "CW.MeinBereichAufgaben"
]


def get_payload(self, api_version):
    start_index = random.randint(0, MIN_AUFGABEN_PER_FALL - 10)
    return {
        "versionInfo": {
            "moduleVersion": self.client.module_version,
            "apiVersion": api_version
        },
        "viewName": f"{UI_FLOW}.{SCREEN_NAME}",
        "screenData": {
            "variables": {
                "SearchInput": "",
                "StartIndex": start_index,
                "MaxRecords": start_index + 10,
                "TableSort": ""
            }
        },
        "inputParameters": {}}


def load_data_actions(self):
    for script in SCRIPT_SOURCES:
        with self.client.get(f"/scripts/{MODULE_NAME}.{script}.mvc.js", headers=self.client.headers,
                             catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:
            # Find all matches
            matches = re.findall(DATA_ACTION_PATTERN, response.text)

            # POST all aggregate/data action requests
            for match in matches:
                _, endpoint, endpoint_url, api_version = match
                logging.debug(f"Loading: {endpoint}")
                self.client.post("/" + endpoint_url, json=get_payload(self, api_version),
                                 headers=self.client.headers, name=f"/{SCREEN_NAME}")
