import random

from helpers import *
from resources import DATA_ACTION_PATTERN

# CONSTANTS
# ---------------------
# Name of the parent UI-Flow in Outsystems
UI_FLOW = "MainFlow"
# Name of the screen in Outsystems
SCREEN_NAME = "FallDetail"
# All the script files, that contain references to aggregates or data actions
SCRIPT_SOURCES = [
    f"{UI_FLOW}.{SCREEN_NAME}",
    "CW.AufgabenDetails",
    "CW.AnlagenDetails",
    "CW.GespraechDetails",
    "CW.BegleitungDetails"
]


def get_payload(self, api_version: str):
    """ TODO Define all screen variables, which are relevant for aggregate filters

    :param self:
    :param api_version:
    :return:
    """
    start_index = 0
    return {
        "versionInfo": {
            "moduleVersion": self.client.module_version,
            "apiVersion": api_version
        },
        "viewName": f"{UI_FLOW}.{SCREEN_NAME}",
        "screenData": {
            "variables": {
                "FallId": self.client.fall_id,
                "_fallIdInDataFetchStatus": 1,
                "DestinationIndex": 2,
                "_destinationIndexInDataFetchStatus": 1,
                "StartIndex": start_index,
                "MaxRecords": start_index + 10,
                "StatusFilter": random.choice([0, 6])
            }
        },
        "inputParameters": {}
    }


def load_data_actions(self):
    for script in SCRIPT_SOURCES:
        with self.client.get(f"/scripts/{MODULE_NAME}.{script}.mvc.js", headers=self.client.headers,
                             catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:

            # Find all matches
            matches = re.findall(DATA_ACTION_PATTERN, response.text)

            # Print extracted values
            for match in matches:
                _, endpoint, endpoint_url, api_version = match
                with self.client.post("/" + endpoint_url, json=get_payload(self, api_version),
                                 headers=self.client.headers, name=f"/{SCREEN_NAME}") as inner_response:
                    if "SetGetAufgabesByFallId" in endpoint:
                        # select new Fall
                        inner_matches = re.findall(r'"Aufgabe":\{"Id":"(\d+)"', inner_response.text)
                        if inner_matches:
                            self.client.aufgabe_id = random.choice(inner_matches)


def aufgabe_erfassen(self, aufgabe_id, titel, beschreibung, datum):
    # set action specific values
    action_name = "AufgabeErfassenOrBearbeiten"
    action_path = f"/screenservices/SHPPOC/Popups/Aufgabe_Popup/Action{action_name}"

    with self.client.get(f"/scripts/{MODULE_NAME}.Popups.Aufgabe_Popup.mvc.js", headers=self.client.headers,
                         catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:
        api_version = get_api_key_from_script(response.text, action_name,
                                              action_path[1:])
        payload = {
            "versionInfo": {"moduleVersion": self.client.module_version, "apiVersion": api_version},
            "viewName": f"{UI_FLOW}.{SCREEN_NAME}",
            "inputParameters":
                {"AufgabeId": aufgabe_id,
                 "FallId": self.client.fall_id,
                 "TypId": random.randint(1, 3),
                 "Titel": titel,
                 "Beschreibung": beschreibung,
                 "SachbearbeiterId": get_random_sachbearbeiter_id(self),
                 "Faelligkeitsdatum": datum
                 }
        }

        self.client.post(action_path, json=payload, headers=self.client.headers, name=f"/{SCREEN_NAME}/Aufgaben")


def gespraech_dokumentieren(self, gespraech_id, titel, beschreibung, datum):
    # set action specific values
    action_name = "Beratungsgespraech_ErfassenOrBearbeiten"
    action_path = f"/screenservices/SHPPOC/Popups/GespraechDokumentieren_Popup/Action{action_name}"

    # decide if user uploads a file
    upload = random_choice_document()
    if upload is None:
        upload = {"List": [], "EmptyListItem": {"DokumentId": "0", "FileName": "", "FileBinary": None}}
    else:
        upload = {"List": [upload]}

    with self.client.get(f"/scripts/{MODULE_NAME}.Popups.GespraechDokumentieren_Popup.mvc.js",
                         headers=self.client.headers,
                         catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:
        payload = {
            "versionInfo":
                {"moduleVersion": self.client.module_version,
                 "apiVersion": get_api_key_from_script(response.text, action_name, action_path[1:])
                 },
            "viewName": f"{UI_FLOW}.{SCREEN_NAME}",
            "inputParameters": {
                "BeratungsgespraechId": gespraech_id,
                "Datum": datum,
                "FallId": self.client.fall_id,
                "List_sDokument": upload,
                "Titel": titel,
                "Zusammenfassung": beschreibung
            }
        }

        self.client.post(action_path, json=payload, headers=self.client.headers, name=f"/{SCREEN_NAME}/Gespräche")


def aufgabe_status_aendern(self):
    # set action specific values
    action_name = "AufgabeSetNextStep"
    action_path = f"/screenservices/SHPPOC/CW/AufgabenDetails/Action{action_name}"

    with self.client.get(f"/scripts/{MODULE_NAME}.CW.AufgabenDetails.mvc.js", headers=self.client.headers,
                         catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:
        payload = {
            "versionInfo":
                {"moduleVersion": self.client.module_version,
                 "apiVersion": get_api_key_from_script(response.text, action_name, action_path[1:])
                 },
            "viewName": f"{UI_FLOW}.{SCREEN_NAME}",
            "inputParameters": {
                "AufgabeId": self.client.aufgabe_id,
                "CurrentStatusId": random.randint(7, 8)
            }
        }

        self.client.post(action_path, json=payload, headers=self.client.headers, name=f"/{SCREEN_NAME}/Aufgaben")


def aufgabe_sachbearbeiter_aendern(self):
    # set action specific values
    action_name = "ChangeAufgabeSB"
    action_path = f"/screenservices/SHPPOC/CW/AufgabenDetails/Action{action_name}"

    with self.client.get(f"/scripts/{MODULE_NAME}.CW.AufgabenDetails.mvc.js", headers=self.client.headers,
                         catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:
        payload = {
            "versionInfo":
                {"moduleVersion": self.client.module_version,
                 "apiVersion": get_api_key_from_script(response.text, action_name, action_path[1:])
                 },
            "viewName": f"{UI_FLOW}.{SCREEN_NAME}",
            "inputParameters": {
                "AufgabeId": self.client.aufgabe_id,
                "UserId": random.choice(self.client.sb_ids)
            }
        }

        self.client.post(action_path, json=payload, headers=self.client.headers, name=f"/{SCREEN_NAME}/Aufgaben")


def begleitung_dokumentieren(self, begleitung_id, beschreibung, datum):
    # set action specific values
    action_name = "Begleitung_ErfassenOrBearbeiten"
    action_path = f"/screenservices/SHPPOC/Popups/Begleitung_Popup/Action{action_name}"

    # decide if user uploads a file
    upload = random_choice_document()
    if upload is None:
        upload = {"List": [], "EmptyListItem": {"DokumentId": "0", "FileName": "", "FileBinary": None}}
    else:
        upload = {"List": [upload]}

    with self.client.get(f"/scripts/{MODULE_NAME}.Popups.Begleitung_Popup.mvc.js", headers=self.client.headers,
                         catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:
        payload = {
            "versionInfo":
                {"moduleVersion": self.client.module_version,
                 "apiVersion": get_api_key_from_script(response.text, action_name, action_path[1:])
                 },
            "viewName": f"{UI_FLOW}.{SCREEN_NAME}",
            "inputParameters": {
                "BegleitungId": begleitung_id,
                "FallId": self.client.fall_id,
                "Bezeichnung": beschreibung,
                "Beschreibung": beschreibung,
                "Eingangsdatum": datum,
                "List_sDokument": upload
            }
        }

        self.client.post(action_path, json=payload, headers=self.client.headers, name=f"/{SCREEN_NAME}/Aufgaben")


def fall_beenden(self):
    # set action specific values
    action_name = "FallChangeStatus"
    action_path = f"/screenservices/SHPPOC/Popups/FallBeenden_Popup/Action{action_name}"

    with self.client.get(f"/scripts/{MODULE_NAME}.Popups.FallBeenden_Popup.mvc.js", headers=self.client.headers,
                         catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:
        payload = {
            "versionInfo":
                {"moduleVersion": self.client.module_version,
                 "apiVersion": get_api_key_from_script(response.text, action_name, action_path[1:])
                 },
            "viewName": f"{UI_FLOW}.{SCREEN_NAME}",
            "inputParameters": {
                "FallId": self.client.fall_id,
                "StatusId": 5
            }
        }

        self.client.post(action_path, json=payload, headers=self.client.headers, name=f"/{SCREEN_NAME}")

    # we reload all screen data afterwards
    load_data_actions(self)


def fall_sachbearbeiter_aendern(self):
    # set action specific values
    action_name = "ChangeFallSB"
    action_path = f"/screenservices/SHPPOC/MainFlow/FallDetail/Action{action_name}"

    with self.client.get(f"/scripts/{MODULE_NAME}.{UI_FLOW}.{SCREEN_NAME}.mvc.js", headers=self.client.headers,
                         catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:
        payload = {
            "versionInfo": {
                "moduleVersion": self.client.module_version,
                "apiVersion": get_api_key_from_script(response.text, action_name, action_path[1:])
            },
            "viewName": f"{UI_FLOW}.{SCREEN_NAME}",
            "inputParameters": {
                "FallId": self.client.fall_id,
                "UserId": random.choice(self.client.sb_ids)
            }
        }

        self.client.post(action_path, json=payload, headers=self.client.headers, name=f"/{SCREEN_NAME}")


def fall_bearbeitung_starten(self):
    # set action specific values
    action_name = "FallChangeStatus"
    action_path = f"/screenservices/SHPPOC/CW/FallDetailsTabs/Action{action_name}"

    with self.client.get(f"/scripts/{MODULE_NAME}.CW.FallDetailsTabs.mvc.js", headers=self.client.headers,
                         catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:
        payload = {
            "versionInfo": {
                "moduleVersion": self.client.module_version,
                "apiVersion": get_api_key_from_script(response.text, action_name, action_path[1:])
            },
            "viewName": f"{UI_FLOW}.{SCREEN_NAME}",
            "inputParameters": {
                "FallId": self.client.fall_id,
                "StatusId": 4
            }
        }

        self.client.post(action_path, json=payload, headers=self.client.headers, name=f"/{SCREEN_NAME}")

    # we reload all screen data afterwards
    load_data_actions(self)


def fall_abrechnen(self):
    # set action specific values
    action_name = "FallAbrechnen"
    action_path = f"/screenservices/SHPPOC/Popups/FallAbrechnen_Popup/Action{action_name}"

    with self.client.get(f"/scripts/{MODULE_NAME}.Popups.FallAbrechnen_Popup.mvc.js", headers=self.client.headers,
                         catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:
        payload = {
            "versionInfo":
                {"moduleVersion": self.client.module_version,
                 "apiVersion": get_api_key_from_script(response.text, action_name, action_path[1:])
                 },
            "viewName": f"{UI_FLOW}.{SCREEN_NAME}",
            "inputParameters": {
                "Betrag": "42",
                "Date": "2025-02-18",
                "FallId": self.client.fall_id
            }
        }

        self.client.post(action_path, json=payload, headers=self.client.headers, name=f"/{SCREEN_NAME}")

    # we reload all screen data afterwards
    load_data_actions(self)


def fall_begleiten(self):
    # set action specific values
    action_name = "FallChangeStatus"
    action_path = f"/screenservices/SHPPOC/MainFlow/FallDetail/Action{action_name}"

    with self.client.get(f"/scripts/{MODULE_NAME}.{UI_FLOW}.{SCREEN_NAME}.mvc.js", headers=self.client.headers,
                         catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:
        payload = {
            "versionInfo":
                {"moduleVersion": self.client.module_version,
                 "apiVersion": get_api_key_from_script(response.text, action_name, action_path[1:])
                 },
            "viewName": f"{UI_FLOW}.{SCREEN_NAME}",
            "inputParameters": {
                "FallId": self.client.fall_id,
                "StatusId": 10
            }
        }

        self.client.post(action_path, json=payload, headers=self.client.headers, name=f"/{SCREEN_NAME}")

    # we reload all screen data afterwards
    load_data_actions(self)


def fall_als_pdf_exportieren(self):
    # set action specific values
    action_name = "GenerateAndSaveFallPDF"
    action_path = f"/screenservices/SHPPOC/MainFlow/FallDetail/Action{action_name}"

    with self.client.get(f"/scripts/{MODULE_NAME}.{UI_FLOW}.{SCREEN_NAME}.mvc.js", headers=self.client.headers,
                         catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:
        payload = {
            "versionInfo":
                {"moduleVersion": self.client.module_version,
                 "apiVersion": get_api_key_from_script(response.text, action_name, action_path[1:])
                 },
            "viewName": f"{UI_FLOW}.{SCREEN_NAME}",
            "inputParameters": {
                "FallId": self.client.fall_id,
                "IstAntrag": False
            }
        }

        self.client.post(action_path, json=payload, headers=self.client.headers, name=f"/{SCREEN_NAME}")

    # we reload all screen data afterwards
    load_data_actions(self)


def fall_anlagen_exportieren(self):
    # set action specific values
    action_name = "ZipDocsByFallId"
    action_path = f"/screenservices/SHPPOC/MainFlow/FallDetail/Action{action_name}"

    with self.client.get(f"/scripts/{MODULE_NAME}.{UI_FLOW}.{SCREEN_NAME}.mvc.js", headers=self.client.headers,
                         catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:
        payload = {
            "versionInfo":
                {"moduleVersion": self.client.module_version,
                 "apiVersion": get_api_key_from_script(response.text, action_name, action_path[1:])
                 },
            "viewName": f"{UI_FLOW}.{SCREEN_NAME}",
            "inputParameters": {
                "FallId": self.client.fall_id
            }
        }

        self.client.post(action_path, json=payload, headers=self.client.headers, name=f"/{SCREEN_NAME}")


def fall_weiterleiten(self, hinweis):
    # set action specific values
    action_name = "FallWeiterleiten"
    action_path = f"/screenservices/SHPPOC/Popups/EDIS_Popup/Action{action_name}"

    with self.client.get(f"/scripts/{MODULE_NAME}.Popups.EDIS_Popup.mvc.js", headers=self.client.headers,
                         catch_response=True, name=f"/{SCREEN_NAME}_resources") as response:
        payload = {
            "versionInfo":
                {"moduleVersion": self.client.module_version,
                 "apiVersion": get_api_key_from_script(response.text, action_name, action_path[1:])
                 },
            "viewName": f"{UI_FLOW}.{SCREEN_NAME}",
            "inputParameters": {
                "FallId": self.client.fall_id,
                "EDISId": random.randint(1, 14),
                "Hinweis": hinweis
            }
        }

        self.client.post(action_path, json=payload, headers=self.client.headers, name=f"/{SCREEN_NAME}")






