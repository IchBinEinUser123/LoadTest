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
    host = FQDN_WITH_PROTO + f"/{MODULE_NAME}"
    wait_time = between(MIN_WAIT_TIME, MAX_WAIT_TIME)
    fall_id = 0

    @task(6)
    def visit_fall_details(self):
        self.client.get(f"/FallDetail?DestinationIndex=2&FallId={self.client.fall_id}", headers=self.client.headers,
                        name="/FallDetail")
        fall_details.load_data_actions(self)

    @task
    def visit_mein_bereich(self):
        self.client.get("/MeinBereich", headers=self.client.headers)
        mein_bereich.load_data_actions(self)

    @task
    def visit_eingangspruefung(self):
        # request document, resources and all ajax data requests
        self.client.get("/Eingangspruefung", headers=self.client.headers)
        eingangsprüfung.load_data_actions(self)

        # Random choice to input search and reload Data
        if random.randint(1, 100) < SEARCH_PROBABILITY:
            # Search for integer of length two -> ensures sufficient search results
            eingangsprüfung.load_data_actions(self, search_input=str(random.randint(10, 99)))

    @task
    def visit_alle_faelle(self):
        # get document and its resources
        self.client.get("/AlleFaelle", headers=self.client.headers)
        alle_fälle.load_data_actions_and_set_new_fall_id(self)

        # Random choice to input search and reload Data
        if random.randint(1, 100) < SEARCH_PROBABILITY:
            # Search for integer of length two -> ensures sufficient search results
            alle_fälle.load_data_actions(self, search_input=str(random.randint(10, 99)))

    @task
    def visit_neuen_fall_anlegen(self):
        self.client.get("/NeuenFallAnlegen", headers=self.client.headers)
        neuen_fall_anlegen.load_data_actions(self)
        neuen_fall_anlegen.fall_erstellen(self)

    @task(5)
    def gespraech_dokumentieren(self):
        text = get_random_text()
        fall_details.gespraech_dokumentieren(self, 0, text, text, "2025-06-14")

    @task(5)
    def aufgabe_dokumentieren(self):
        text = get_random_text()
        fall_details.aufgabe_erfassen(self, 0, text, text, "2025-06-14")

    @task(5)
    def aufgabe_status_aendern(self):
        fall_details.aufgabe_status_aendern(self)

    @task(5)
    def aufgabe_sachbearbeiter_aendern(self):
        fall_details.aufgabe_sachbearbeiter_aendern(self)

    @task(5)
    def begleitung_dokumentieren(self):
        text = get_random_text()
        fall_details.begleitung_dokumentieren(self, 0, text, "2025-06-14")

    @task
    def fall_bearbeitung_starten(self):
        fall_details.fall_bearbeitung_starten(self)

    @task
    def fall_sachbearbeiter_aendern(self):
        fall_details.fall_sachbearbeiter_aendern(self)

    @task
    def fall_beenden(self):
        fall_details.fall_beenden(self)

    @task
    def fall_bescheiden(self):
        fall_details.fall_bescheiden(self)

    @task
    def fall_abrechnen(self):
        fall_details.fall_abrechnen(self)

    @task
    def fall_begleiten(self):
        fall_details.fall_begleiten(self)

    @task
    def fall_als_pdf_exportieren(self):
        fall_details.fall_als_pdf_exportieren(self)

    @task
    def fall_anlagen_exportieren(self):
        fall_details.fall_anlagen_exportieren(self)

    @task
    def fall_weiterleiten(self):
        fall_details.fall_weiterleiten(self, hinweis=get_random_text())
        time.sleep(MIN_WAIT_TIME)
        # get new id values, because Fall no longer belongs to current EDIS
        self.visit_alle_faelle()
        time.sleep(MIN_WAIT_TIME)
        self.visit_fall_details()
        time.sleep(MIN_WAIT_TIME)


    def on_start(self):
        # login and set headers
        login_user(self)

        # initialize relevant values, i.e. Sachbearbeiter list, FallId, AufgabeId
        self.visit_alle_faelle()
        time.sleep(MIN_WAIT_TIME)
        self.visit_fall_details()
        time.sleep(MIN_WAIT_TIME)
