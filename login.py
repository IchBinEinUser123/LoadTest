import json
import logging
import re
import urllib.parse

from config import FQDN_WITH_PROTO, MODULE_NAME
from helpers import get_api_key_from_script, get_random_user_id

# CONSTANTS
# ---------------------
# Name of the parent UI-Flow in Outsystems
UI_FLOW = "Common"
# Name of the screen in Outsystems
SCREEN_NAME = "Login"
# path of the login action
LOGIN_ACTION_NAME = "SBLogin"
LOGIN_PATH = f"/screenservices/SHPPOC/Common/Login/Action{LOGIN_ACTION_NAME}"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"


def login_user(self):
    """
    Handles User Login, extracts CSRF-Token etc. and updates relevant HTTP headers in client.headers
    :param self: The HttpUser object
    :return:
    """
    # set default headers
    self.client.headers = {
        "User-Agent": USER_AGENT,
        "Accept-Language": "de-DE,de;q=0.9",
        "Origin": FQDN_WITH_PROTO
    }

    # get module version
    response = self.client.get("/Login")
    print(response.text)
    with self.client.get("/moduleservices/moduleversioninfo") as response:
        self.client.module_version = json.loads(response.text).get("versionToken")
        logging.debug("Module Version", self.client.module_version)

    response = self.client.get("/scripts/OutSystems.js")
    match = re.search(r'e\.AnonymousCSRFToken\s*=\s*"([^"]+)"', response.text)
    if match:
        csrf_token = match.group(1)
        self.client.headers.update({"X-Csrftoken": csrf_token})
        logging.debug(f"Extracted CSRF Token: {csrf_token}")
    else:
        logging.debug("CSRF Token not found!")

    # Get Login API Version Info
    with self.client.get(f"/scripts/{MODULE_NAME}.{UI_FLOW}.{SCREEN_NAME}.mvc.js", headers=self.client.headers,
                         catch_response=True) as response:
        api_version = get_api_key_from_script(response.text, LOGIN_ACTION_NAME, LOGIN_PATH[1:])
        logging.debug(api_version)

    payload = {
        "versionInfo": {
            "moduleVersion": self.client.module_version,
            "apiVersion": api_version
        },
        "viewName": "Common.Login",
        "inputParameters": {
            "ExtendedUserId": get_random_user_id()
        }
    }

    # Login and extract new CSRF token
    self.client.post(LOGIN_PATH, json=payload, headers=self.client.headers)
    match = re.search(r"crf%3d(.*?)%3d", self.client.cookies.get("nr2Users"))
    if match:
        csrf_token = urllib.parse.unquote(match.group(1)) + "="
        self.client.headers.update({"X-Csrftoken": csrf_token})
        logging.debug("New CSRF-Token: ", csrf_token)