import logging
import random
import re

from config import *
from resources import DATA_ACTION_PATTERN
from helpers import debug_log

# CONSTANTS
# ---------------------
# Name of the parent UI-Flow in Outsystems
UI_FLOW = "MainFlow"
# Name of the screen in Outsystems
SCREEN_NAME = "AlleFaelle"
# All the script files, that contain references to aggregates or data actions
SCRIPT_SOURCES = [
    f"{UI_FLOW}.{SCREEN_NAME}"
]


def get_payload(self, api_version, search_input=""):
    """
    Generates the payload for API requests.

    :param self: The HttpUser object
    :param api_version: API version being used
    :param search_input: Optional search input parameter
    :return: Dictionary containing the request payload
    """
    start_index = random.randint(0, MIN_FALL_COUNT_PER_EDIS - 10)
    return {
        "versionInfo": {
            "moduleVersion": self.client.module_version,
            "apiVersion": api_version
        },
        "viewName": f"{UI_FLOW}.{SCREEN_NAME}",
        "screenData": {
            "variables": {
                "SearchInput": search_input,
                "StartIndex": start_index,
                "MaxRecords": start_index + 10,
                "TableSort": "Fall.DatumFallanlage"
            }
        },
        "inputParameters": {}
    }


def load_data_actions_and_set_new_fall_id(self, search_input=""):
    """
    Loads data actions and updates the fall ID by extracting it from the response.

    :param self: The HttpUser object
    :param search_input: Optional search input parameter
    :return:
    """
    for script in SCRIPT_SOURCES:
        with self.client.get(f"/scripts/{MODULE_NAME}.{script}.mvc.js", headers=self.client.headers,
                             catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:

            matches = re.findall(DATA_ACTION_PATTERN, response.text)

            for match in matches:
                _, endpoint, endpoint_url, api_version = match
                logging.debug(f"Loading: {endpoint}")
                with self.client.post("/" + endpoint_url, json=get_payload(self, api_version, search_input),
                                      headers=self.client.headers, name=f"/{SCREEN_NAME}") as inner_response:
                    if "SetGetFallsByEDISId" in endpoint:
                        inner_matches = re.findall(r'"Fall":\{"Id":"(\d+)"', inner_response.text)
                        if inner_matches:
                            self.client.fall_id = random.choice(inner_matches)
                            logging.debug(f"New Fall ID: {self.client.fall_id}")
                        else:
                            self.client.fall_id = 0
                            logging.debug(f"No new Fall ID found")

                    if "GetSachbearbeiterByEDIS" in endpoint:
                        sb_matches = re.findall(r'"UserId":\s*(\d+)', inner_response.text)
                        if sb_matches:
                            logging.debug(sb_matches)
                            self.client.sb_ids = sb_matches


def load_data_actions(self, search_input=""):
    """
    Loads data actions without modifying the fall ID.

    :param self: The HttpUser object
    :param search_input: Optional search input parameter
    :return:
    """
    for script in SCRIPT_SOURCES:
        with self.client.get(f"/scripts/{MODULE_NAME}.{script}.mvc.js", headers=self.client.headers,
                             catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:

            matches = re.findall(DATA_ACTION_PATTERN, response.text)

            for match in matches:
                _, endpoint, endpoint_url, api_version = match
                logging.debug(f"Loading: {endpoint}")
                self.client.post("/" + endpoint_url, json=get_payload(self, api_version, search_input),
                                 headers=self.client.headers, name=f"/{SCREEN_NAME}")
