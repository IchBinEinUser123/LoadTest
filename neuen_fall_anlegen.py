import random
import re

from config import *
from helpers import get_api_key_from_script
from resources import DATA_ACTION_PATTERN

# CONSTANTS
# ---------------------
# Name of the parent UI-Flow in Outsystems
UI_FLOW = "MainFlow"
# Name of the screen in Outsystems
SCREEN_NAME = "NeuenFallAnlegen"
# All the script files, that contain references to aggregates or data actions
SCRIPT_SOURCES = [
    "CW.FallDisplay"
]


def get_payload(self, api_version):
    """
    Generates the payload for the FallFormSubmit request with API versioning.
    :param self: The instance calling the function (likely related to the client making the request)
    :param api_version: The API version for which the payload is being generated
    :return: Dictionary containing the payload with version info and screen data
    """
    return {
        "versionInfo": {
            "moduleVersion": self.client.module_version,
            "apiVersion": api_version
        },
        "viewName": f"{UI_FLOW}.{SCREEN_NAME}",
        "screenData": {
            "variables": {}
        },
        "inputParameters": {}
    }


def load_data_actions(self):
    """
    Loads the data actions from the defined script sources, and sends POST requests with the generated payload.
    This function checks all scripts for references to data actions, and sends them to the API.
    :param self: The instance calling the function (likely related to the client making the request)
    :return None
    """
    for script in SCRIPT_SOURCES:
        with self.client.get(f"/scripts/{MODULE_NAME}.{script}.mvc.js", headers=self.client.headers,
                             catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:
            # Find all matches
            matches = re.findall(DATA_ACTION_PATTERN, response.text)

            # POST all aggregate/data action requests
            for match in matches:
                _, endpoint, endpoint_url, api_version = match
                self.client.post("/" + endpoint_url, json=get_payload(self, api_version),
                                 headers=self.client.headers, name=f"/{SCREEN_NAME}")


def fall_erstellen(self):
    """
    Creates a new case (Fall) by sending a POST request with the appropriate payload.
    This function performs the action of creating a new case with predefined values.
    :param self: The instance calling the function (likely related to the client making the request)
    :return None
    """
    with self.client.get(f"/scripts/{MODULE_NAME}.CW.FallDisplay.mvc.js", headers=self.client.headers,
                         catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:
        api_version = get_api_key_from_script(response.text, "FallFormSubmit",
                                              "screenservices/SHPPOC/CW/FallDisplay/ActionFallFormSubmit")
        payload = {
            "versionInfo": {"moduleVersion": self.client.module_version, "apiVersion": api_version},
            "viewName": f"{UI_FLOW}.{SCREEN_NAME}",
            "inputParameters": {
                "Fall": {
                    "Id": "0",
                    "IstAntrag": False,
                    "StatusId": 0,
                    "FallbezeichnungId": random.randint(1, 2),
                    "AnredeId": 0,
                    "TitelId": 5,
                    "Nachname": "Test",
                    "Geburtsname": "",
                    "Vorname": "Load",
                    "Geburtsdatum": "2025-02-17",
                    "Geburtsort": "",
                    "GeschlechtId": 2,
                    "StaatsangehoerigkeitLandId": "38",
                    "Telefonnummer": "", "Email": "example@example.invalid",
                    "Strasse": "Teststraße",
                    "HausNr": "42",
                    "PLZ": "12527",
                    "Ort": "Berlin",
                    "LandId": "38",
                    "WohnhaftInBerlinSeit": "2025-02-17",
                    "Kontoinhaber": "Load Test",
                    "IBAN": "DE02120300000000202051",
                    "Bank": "DEUTSCHE KREDITBANK BERLIN",
                    "Antragsdatum": "1900-01-01",
                    "EDISId": 0,
                    "SachbearbeiterId": 0,
                    "WohnverhaeltnisId": 0,
                    "IstWeiterePersonImHaushalt": False,
                    "LebenssituationAngaben": "",
                    "AbrechnungBetrag": "0",
                    "KostenuebernahmeDatum": "1900-01-01",
                    "DatumFallanlage": "1900-01-01",
                    "AngelegtVon": 0,
                    "IstWeiterleitung": False,
                    "WeiterleitungHinweis": "",
                    "WeiterleitungOldStatusId": 0,
                    "WeiterleitungDatum": "1900-01-01",
                    "WeiterleitungOldEDISId": 0},
                "List_Dokumente": {
                    "List": [],
                    "EmptyListItem": {
                        "DokumentId": "0",
                        "FileName": "",
                        "FileBinary": None
                    }
                }
            }
        }

        self.client.post("/screenservices/SHPPOC/CW/FallDisplay/ActionFallFormSubmit",
                         json=payload, headers=self.client.headers, name=f"/{SCREEN_NAME}")
