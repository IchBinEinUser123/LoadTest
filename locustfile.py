import logging
import random
import time

from config import *
import fall_details
import alle_fälle
import mein_bereich
import eingangsprüfung
import neuen_fall_anlegen

from locust import task, between
from locust_plugins.users.resource import HttpUserWithResources
from helpers import *
from login import login_user


class Sachbearbeiter(HttpUserWithResources):
    """
    Simulates a Sachbearbeiter (caseworker) performing various tasks on the application.
    """
    host = FQDN_WITH_PROTO + f"/{MODULE_NAME}"
    wait_time = between(MIN_WAIT_TIME, MAX_WAIT_TIME)
    fall_id = 0
    aufgabe_id = 0

    @task(10)
    def visit_fall_details(self):
        """
        Visits the fall details page and loads necessary data actions.
        :param self: The HttpUser object
        :return:
        """
        self.client.get(f"/FallDetail?DestinationIndex=2&FallId={self.client.fall_id}", headers=self.client.headers,
                        name="/FallDetail")
        fall_details.load_data_actions(self)

    @task(5)
    def visit_mein_bereich(self):
        """
        Visits the 'Mein Bereich' page and loads necessary data actions.
        :param self: The HttpUser object
        :return:
        """
        self.client.get("/MeinBereich", headers=self.client.headers)
        mein_bereich.load_data_actions(self)

    @task(5)
    def visit_eingangspruefung(self):
        """
        Visits the 'Eingangsprüfung' page, loads resources, and optionally performs a search.
        :param self: The HttpUser object
        :return:
        """
        self.client.get("/Eingangspruefung", headers=self.client.headers)
        eingangsprüfung.load_data_actions(self)

        if random.randint(1, 100) < SEARCH_PROBABILITY:
            eingangsprüfung.load_data_actions(self, search_input=str(random.randint(10, 99)))

    @task(5)
    def visit_alle_faelle(self):
        """
        Visits the 'Alle Fälle' page, loads data actions, and optionally performs a search.
        :param self: The HttpUser object
        :return:
        """
        self.client.get("/AlleFaelle", headers=self.client.headers)
        alle_fälle.load_data_actions_and_set_new_fall_id(self)

        if random.randint(1, 100) < SEARCH_PROBABILITY:
            alle_fälle.load_data_actions(self, search_input=str(random.randint(10, 99)))

    @task
    def visit_neuen_fall_anlegen(self):
        """
        Visits the 'Neuen Fall Anlegen' page and initiates the creation of a new case.
        :param self: The HttpUser object
        :return:
        """
        self.client.get("/NeuenFallAnlegen", headers=self.client.headers)
        neuen_fall_anlegen.load_data_actions(self)
        neuen_fall_anlegen.fall_erstellen(self)

    @task(10)
    def gespraech_dokumentieren(self):
        """
        Documents a conversation in a case.
        :param self: The HttpUser object
        :return:
        """
        text = get_random_text()
        fall_details.gespraech_dokumentieren(self, 0, text, text, "2025-06-14")

    @task(10)
    def aufgabe_dokumentieren(self):
        """
        Documents a task in a case.
        :param self: The HttpUser object
        :return:
        """
        text = get_random_text()
        fall_details.aufgabe_erfassen(self, 0, text, text, "2025-06-14")

    @task(20)
    def aufgabe_status_aendern(self):
        """
        Changes the status of a task.
        :param self: The HttpUser object
        :return:
        """
        fall_details.aufgabe_status_aendern(self)

    @task(5)
    def aufgabe_sachbearbeiter_aendern(self):
        """
        Changes the assigned caseworker for a task.
        :param self: The HttpUser object
        :return:
        """
        fall_details.aufgabe_sachbearbeiter_aendern(self)

    @task(10)
    def begleitung_dokumentieren(self):
        """
        Documents case support.
        :param self: The HttpUser object
        :return:
        """
        text = get_random_text()
        fall_details.begleitung_dokumentieren(self, 0, text, "2025-06-14")

    @task(3)
    def fall_bearbeitung_starten(self):
        """
        Starts processing a case.
        :param self: The HttpUser object
        :return:
        """
        fall_details.fall_bearbeitung_starten(self)

    @task(2)
    def fall_sachbearbeiter_aendern(self):
        """
        Changes the assigned caseworker for a case.
        :param self: The HttpUser object
        :return:
        """
        fall_details.fall_sachbearbeiter_aendern(self)

    @task(3)
    def fall_beenden(self):
        """
        Ends a case.
        :param self: The HttpUser object
        :return:
        """
        fall_details.fall_beenden(self)

    @task(3)
    def fall_bescheiden(self):
        """
        Decides a case.
        :param self: The HttpUser object
        :return:
        """
        fall_details.fall_bescheiden(self)

    @task(3)
    def fall_abrechnen(self):
        """
        Processes payment for a case.
        :param self: The HttpUser object
        :return:
        """
        fall_details.fall_abrechnen(self)

    @task(3)
    def fall_begleiten(self):
        """
        Starts attendance of a case.
        :param self: The HttpUser object
        :return:
        """
        fall_details.fall_begleiten(self)

    @task
    def fall_als_pdf_exportieren(self):
        """
        Downloads case as a PDF.
        :param self: The HttpUser object
        :return:
        """
        fall_details.fall_als_pdf_exportieren(self)

    @task
    def fall_anlagen_exportieren(self):
        """
        Downloads case attachments as zip.
        :param self: The HttpUser object
        :return:
        """
        fall_details.fall_anlagen_exportieren(self)

    @task
    def fall_weiterleiten(self):
        """
        Redirects a case to a different EDIS.
        :param self: The HttpUser object
        :return:
        """
        fall_details.fall_weiterleiten(self, hinweis=get_random_text())
        time.sleep(MIN_WAIT_TIME)
        # get new id values, because Fall no longer belongs to current EDIS
        self.visit_alle_faelle()
        time.sleep(MIN_WAIT_TIME)
        self.visit_fall_details()
        time.sleep(MIN_WAIT_TIME)


    def on_start(self):
        """
        Performs login and initializes relevant values.
        :param self: The HttpUser object
        :return:
        """
        # login and set headers
        login_user(self)

        # initialize relevant values, i.e. Sachbearbeiter list, FallId, AufgabeId
        self.visit_alle_faelle()
        time.sleep(MIN_WAIT_TIME)
        self.visit_fall_details()
        time.sleep(MIN_WAIT_TIME)
