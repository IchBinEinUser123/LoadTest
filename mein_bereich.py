import logging
import random
import re

from config import *
from resources import DATA_ACTION_PATTERN

# CONSTANTS
# ---------------------
# Define constants for Outsystems UI flow and screen names, as well as the list of script sources
UI_FLOW = "MainFlow"  # Name of the parent UI-Flow in Outsystems
SCREEN_NAME = "MeinBereich"  # Name of the screen in Outsystems


# List of script sources containing references to aggregates or data actions
SCRIPT_SOURCES = [
    f"{UI_FLOW}.{SCREEN_NAME}",
    "CW.MeinBereichFaelle",
    "CW.MeinBereichAufgaben"
]


def get_payload(self, api_version):
    """
    Generates the payload for making a request, with dynamic values for start index and max records.
    :param self: The instance calling the function (likely related to the client making the request)
    :param api_version: The version of the API for which the payload is being generated
    :return: Dictionary containing the payload with version info and screen data
    """
    # Randomly calculate the starting index for the query
    start_index = random.randint(0, MIN_AUFGABEN_PER_FALL - 10)

    # Construct the payload dictionary with dynamic values
    return {
        "versionInfo": {
            "moduleVersion": self.client.module_version,  # Module version from the client instance
            "apiVersion": api_version  # The provided API version
        },
        "viewName": f"{UI_FLOW}.{SCREEN_NAME}",  # The view name (Outsystems flow and screen)
        "screenData": {
            "variables": {
                "SearchInput": "",  # Placeholder for search input
                "StartIndex": start_index,  # The dynamically calculated start index
                "MaxRecords": start_index + 10,  # Max records to fetch (start index + 10)
                "TableSort": ""  # Placeholder for table sorting, if any
            }
        },
        "inputParameters": {}  # Placeholder for any additional input parameters
    }


def load_data_actions(self):
    """
    Loads the data actions from the defined script sources, and sends POST requests with the generated payload.
    This function checks all scripts for references to data actions, and sends them to the API.
    :param self: The instance calling the function (likely related to the client making the request)
    """
    # Iterate through all defined script sources
    for script in SCRIPT_SOURCES:
        # Perform an HTTP GET request to fetch the script content
        with self.client.get(f"/scripts/{MODULE_NAME}.{script}.mvc.js", headers=self.client.headers,
                             catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:
            # Use regex to find all matches for data action patterns in the script
            matches = re.findall(DATA_ACTION_PATTERN, response.text)

            # Iterate through all found matches
            for match in matches:
                # Unpack the match (match includes endpoint, URL, and API version)
                _, endpoint, endpoint_url, api_version = match
                logging.debug(f"Loading: {endpoint}")  # Log which endpoint is being loaded

                # Perform a POST request to the endpoint with the generated payload
                self.client.post("/" + endpoint_url, json=get_payload(self, api_version),
                                 headers=self.client.headers, name=f"/{SCREEN_NAME}")
