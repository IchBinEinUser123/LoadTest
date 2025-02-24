import random
import re
import logging
from config import *
from resources import PDF_FILE, PDF_BESCHEID, PDF_ABRECHNUNG, PDF_FALLDATEN


def debug_log(response):
    """
    Logs the details of the HTTP response for debugging purposes.

    This function prints the URL, status code, and response text to the console
    for debugging HTTP requests made during the execution of the script.

    :param response: The HTTP response object to be logged
    :return: None
    """
    print(response.request.url)
    # print(f"Request Headers: {response.request.headers}")
    # print(f"Response Headers: {response.headers}")
    print(response.status_code, response.text)
    print("-" * 42 + "\n")


def get_api_key_from_script(response_text, endpoint_name, endpoint_url):
    """
    Extracts the API key from a given script response.

    This function searches for a pattern in the script's response text to
    find and return the API key associated with the provided endpoint name and URL.

    :param response_text: The response text containing the script
    :param endpoint_name: The name of the API endpoint
    :param endpoint_url: The URL of the API endpoint
    :return: The extracted API key, or None if not found
    """
    if endpoint_url.startswith("/"):
        endpoint_url = endpoint_url[1:]
    endpoint_name = re.escape(endpoint_name)
    endpoint_url = re.escape(endpoint_url)
    logging.debug("Endpoints: ", endpoint_name, endpoint_url)

    for keyword in ["callServerAction", "callAggregateWithStartIndexAndClientVars"]:
        pattern = fr'{keyword}\(\s*"{endpoint_name}"\s*,\s*"{endpoint_url}"\s*,\s*"([^"]+)"'
        match = re.search(pattern, response_text)
        if match:
            return match.group(1)

    # None if no match
    return None


def random_choice_document():
    """
    Returns a random document to be uploaded based on the configured probability.

    This function returns a document with a file and name if the random number
    is below the configured upload probability; otherwise, it returns None.

    :return: A dictionary representing the document, or None if not selected
    """
    if random.randint(1, 100) > UPLOAD_PROBABILITY:
        return None
    else:
        return {
            "DokumentId": "0",
            "FileName": "Alice_in_Wonderland.pdf",
            "FileBinary": PDF_FILE
        }


def get_bescheid_document():
    """
    Returns a predefined Bescheid document.

    This function returns a dictionary representing the Bescheid document
    with a specific file name and binary content.

    :return: A dictionary representing the Bescheid document
    """
    return {
        "DokumentId": "0",
        "FileName": "Bescheid.pdf",
        "FileBinary": PDF_BESCHEID
    }


def get_abrechnung_document():
    """
    Returns a predefined Abrechnung document.

    This function returns a dictionary representing the Abrechnung document
    with a specific file name and binary content.

    :return: A dictionary representing the Abrechnung document
    """
    return {
        "DokumentId": "0",
        "FileName": "Abrechnung.pdf",
        "FileBinary": PDF_ABRECHNUNG
    }


def get_falldaten_document():
    """
    Returns a predefined Falldaten document.

    This function returns a dictionary representing the Falldaten document
    with a specific file name and binary content.

    :return: A dictionary representing the Falldaten document
    """
    return {
        "DokumentId": "0",
        "FileName": "Falldaten.pdf",
        "FileBinary": PDF_FALLDATEN
    }


def get_random_sachbearbeiter_id(self):
    """
    Returns a random Sachbearbeiter (case worker) ID.

    This function selects a random case worker ID from the available list.

    :param self: The HttpUser object (usually representing a user in an HTTP request)
    :return: A random case worker ID from the available IDs
    """
    return random.choice(self.client.sb_ids)


def get_random_user_id():
    """
    Returns a random user ID based on the environment.

    The user ID is selected randomly from a range, with a different range
    depending on whether the environment is a development environment or not.

    :return: A random user ID as a string
    """
    if "dev" in FQDN_WITH_PROTO:
        return str(random.randint(2, 29))
    else:
        return str(random.randint(29, 588))


# Random texts
lorem = ("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. "
         "At vero eos et accusam et justo duo dolores et ea rebum. "
         "Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. "
         "At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. "
         "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea re")


def get_random_text(max_length: int = 800):
    """
    Returns a random text snippet with a maximum length.

    This function generates a random substring from the predefined 'lorem'
    text up to the specified maximum length.

    :param max_length: The maximum length of the returned text
    :return: A random substring from the predefined 'lorem' text
    """
    return lorem[:random.randint(1, max_length)]


# Random PLZ generation
plz_string = """PLZ vom Ortsteil Charlottenburg
10585
10587
10589
10623
10625
10627
10629
10707
10709
10711
10719
10787
10789
14050
14055
14057
14059
-
..."""  # (truncated for brevity)

five_digit_substrings = re.findall(r'\b\d{5}\b', plz_string)

def get_random_plz():
    """
    Returns a random 5-digit postal code (PLZ) from a predefined list.

    This function selects a random postal code from the predefined string
    containing various postal codes from different districts.

    :return: A random 5-digit postal code as a string
    """
    return random.choice(five_digit_substrings)
