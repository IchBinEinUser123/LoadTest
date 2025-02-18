import random
import re
import logging
from config import *
from resources import PDF_FILE


def debug_log(response):
    print(response.request.url)
    # print(f"Request Headers: {response.request.headers}")
    # print(f"Response Headers: {response.headers}")
    print(response.status_code, response.text)
    print("-" * 42 + "\n")


def get_api_key_from_script(response_text, endpoint_name, endpoint_url):
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
    if random.randint(1, 100) > UPLOAD_PROBABILITY:
        return None
    else:
        return {"DokumentId": "0",
                "FileName": "Alice_in_Wonderland.pdf",
                "FileBinary": PDF_FILE}


def get_random_sachbearbeiter_id(self):
    return random.choice(self.client.sb_ids)


def get_random_user_id():
    return str(random.randint(2, 29))


# random texts
lorem = ("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. "
         "At vero eos et accusam et justo duo dolores et ea rebum. "
         "Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. "
         "At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. "
         "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea re")

def get_random_text(max_length: int = 800):
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

PLZ vom Ortsteil Charlottenburg-Nord
10589
13353
13627
13629
-
-
PLZ vom Ortsteil Grunewald
10711
14055
14193
14195
14199
-
PLZ vom Ortsteil Halensee
10709
10711
10713
-
-
-
PLZ vom Ortsteil Schmargendorf
14193
14195
14197
14199
-
-
PLZ vom Ortsteil Westend
14050
14052
14053
14055
14057
14059
PLZ vom Ortsteil Wilmersdorf
10707
10709
10711
10713
10715
10717
10719
10777
10779
10789
10825
14195
14197
14199
-
-
-
-
Die Postleitzahlen von Friedrichshain-Kreuzberg
PLZ vom Ortsteil Friedrichshain
10243
10179
10245
10317
10247
10249
10178
10179
-
-
-
-
PLZ vom Ortsteil Kreuzberg
10961
10969
10963
10785
10965
10967
10997
10999
-
-
-
-
Die Postleitzahlen von Lichtenberg Hohenschönhausen
PLZ vom Ortsteil Alt-Hohenschönhausen
12681
13051
13053
13055
-
-
Postleitzahl Berlin Falkenberg
13057
-
-
-
-
-
PLZ vom Ortsteil Fennpfuhl
10367
10369
-
-
-
-
PLZ vom Ortsteil Friedrichsfelde
10315
10317
10319
-
-
-
PLZ vom Ortsteil Lichtenberg
10315
10365
10367
10317
10369
-
PLZ vom Ortsteil Karlshorst
10317
10318
-
-
-
-
PLZ vom Ortsteil Malchow
13051
-
-
-
-
-
Postleitzahl vom Ortsteil Neu-Hohenschönhausen
13051
13053
13057
13059
-
-
PLZ vom Ortsteil Rummelsburg
10315
10317
10318
10365
-
-
PLZ vom Ortsteil Wartenberg
13051
13059
-
-
-
-

Die Postleitzahlen von Marzahn-Hellersdorf
PLZ vom Ortsteil Biesdorf
12683
12685
-
-
-
-
PLZ vom Ortsteil Kaulsdorf
12555
12619
12621
12623
-
-
PLZ vom Ortsteil Hellersdorf
12619
12621
12627
12629
-
-
PLZ vom Ortsteil Marzahn
12679
12681
12683
12685
12687
12689
PLZ vom Ortsteil Mahlsdorf
12621
12623
-
-
-
-
Die Postleitzahlen von Berlin Mitte
PLZ vom Ortsteil Gesundbrunnen
13347
13353
13355
13357
13359
13409
PLZ vom Ortsteil Hansaviertel
10555
10557
-
-
-
-
PLZ vom Ortsteil Mitte
10115
10117
10119
10178
10179
10435
PLZ vom Ortsteil Moabit
10551
10553
10555
10557
10559
13353
PLZ vom Ortsteil Tiergarten
10117
10557
10623
10785
10787
10963
PLZ vom Ortsteil Wedding
13347
13349
13351
13353
13357
13359
13405
13407
13409
-
-
-
Die Postleitzahlen Berlin Neukölln
PLZ vom Ortsteil Britz
12051
12057
12099
12347
12349
12351
12359
-
-
-
-
-
PLZ vom Ortsteil Buckow
12107
12305
12349
12351
12353
12357
12359
-
-
-
-
-
PLZ vom Ortsteil Gropiusstadt
12351
12353
12357
-
-
-
PLZ vom Ortsteil Neukölln
10965
10967
12043
12045
12047
12049
12051
12053
12055
12057
12059
12099
PLZ vom Ortsteil Rudow
12351
12353
12355
12357
12359
-
Die Postleitzahlen von Pankow
PLZ vom Ortsteil Blankenburg
13051
13125
13129
-
-
-
PLZ vom Ortsteil Blankenfelde
13127
13158
13159
-
-
-
PLZ vom Ortsteil Buch
13125
13127
-
-
-
-
PLZ vom Ortsteil Französisch Buchholz
13127
13129
13156
-
-
-
PLZ vom Ortsteil Heinersdorf
13086
13088
13089
13129
-
-
PLZ vom Ortsteil Karow
13125
-
-
-
-
-
PLZ vom Ortsteil Niederschönhausen
13127
13156
13158
13187
-
-
PLZ vom Ortsteil Pankow
10439
13129
13187
13189
-
-
PLZ vom Ortsteil Prenzlauer Berg
10119
10247
10249
10369
10405
10407
10409
10435
10437
10439
13187
13189
PLZ vom Ortsteil Rosenthal
13156
13158
-
-
-
-
PLZ vom Ortsteil Stadtrandsiedlung Malchow
13051
13088
13089
13129
-
-
PLZ vom Ortsteil Weißensee
13051
13086
13088
-
-
-
PLZ vom Ortsteil Wilhelmsruh
13156
13158
-
-
-
-

Die Postleitzahlen von Reinickendorf
PLZ vom Ortsteil Borsigwalde
13403
13509
-
-
-
-
PLZ vom Ortsteil Frohnau
13465
-
-
-
-
-
PLZ vom Ortsteil Heiligensee
13503
13505
-
-
-
-
PLZ vom Ortsteil Hermsdorf
13465
13467
-
-
-
-
PLZ vom Ortsteil Konradshöhe
13505
-
-
-
-
-
PLZ vom Ortsteil Lübars
13435
13469
-
-
-
-
PLZ vom Ortsteil Märkisches Viertel
13435
13439
-
-
-
-
PLZ vom Ortsteil Reinickendorf
13403
13405
13407
13409
13437
13509
PLZ vom Ortsteil Tegel
13403
13405
13503
13505
13507
13509
13599
13629
-
-
-
-
PLZ vom Ortsteil Waidmannslust
13469
-
-
-
-
-
PLZ vom Ortsteil Wittenau
13403
13407
13435
13437
13439
13469
13509
-
-
-
-
-
Die Postleitzahlen von Spandau
PLZ vom Ortsteil Falkenhagener Feld
13583
13585
13589
13591
-
-
PLZ vom Ortsteil Gatow
14089
-
-
-
-
-
PLZ vom Ortsteil Hakenfelde
13585
13587
13589
-
-
-
PLZ vom Ortsteil Haselhorst
13597
13599
-
-
-
-
PLZ vom Ortsteil Kladow
14089
-
-
-
-
-
PLZ vom Ortsteil Siemensstadt
13599
13627
13629
-
-
-
PLZ vom Ortsteil Spandau
13581
13583
13585
13587
13597
14052
PLZ vom Ortsteil Staaken
13581
13589
13591
13593
-
-
PLZ vom Ortsteil Wilhelmstadt
13581
13593
13595
13597
-
-
Die Postleitzahlen von Steglitz-Zehlendorf
PLZ vom Ortsteil Dahlem
12203
14169
14193
14195
14199
-
PLZ vom Ortsteil Lankwitz
12167
12209
12247
12249
12277
-
PLZ vom Ortsteil Lichterfelde
12165
12203
12205
12207
12209
12247
12249
12279
14167
14169
14195
-
PLZ vom Ortsteil Nikolassee
14109
14129
14163
14193
-
-
PLZ vom Ortsteil Schlachtensee
14129
-
-
-
-
-
-
-
-
-
-
-
PLZ vom Ortsteil Steglitz
12157
12161
12163
12165
12167
12169
12203
12247
14195
14197
-
-
PLZ vom Ortsteil Wannsee
14109
-
-
-
-
-
PLZ vom Ortsteil Zehlendorf
14163
14165
14167
14169
14129
-
Die Postleitzahlen von Tempelhof-Schöneberg
PLZ vom Ortsteil Friedenau
10827
12159
12161
12163
14197
-
PLZ vom Ortsteil Lichtenrade
12107
12277
12305
12307
12309
-
PLZ vom Ortsteil Mariendorf
12099
12105
12107
12109
12277
12103
PLZ vom Ortsteil Marienfelde
12107
12249
12277
12279
12307
-
PLZ vom Ortsteil Schöneberg
10777
10779
10781
10783
10785
10787
10789
10823
10825
10827
10829
10965
12101
12103
12105
12157
12159
-
PLZ vom Ortsteil Tempelhof
10965
12099
12101
12103
12105
12109
12279
-
-
-
-
-
Die Postleitzahlen von Treptow-Köpenick
PLZ vom Ortsteil Adlershof
12439
12487
12489
-
-
-
PLZ vom Ortsteil Alt-Treptow
12435
-
-
-
-
-
PLZ vom Ortsteil Altglienicke
12524
12526
-
-
-
-
PLZ vom Ortsteil Baumschulenweg
12437
12487
-
-
-
-
PLZ Berlin Bohnsdorf
12524
12526
-
-
-
-
PLZ vom Ortsteil Friedrichshagen
12587
-
-
-
-
-
PLZ vom Ortsteil Grünau
12526
12527
-
-
-
-
PLZ vom Ortsteil Johannisthal
12437
12439
12487
12489
-
-
PLZ Berlin Köpenick
12555
12557
12559
12587
12623
12459
PLZ vom Ortsteil Müggelheim
12559
-
-
-
-
-
PLZ vom Ortsteil Niederschöneweide
12437
12439
-
-
-
-

PLZ vom Ortsteil Oberschöneweide
10318
12459
-
-
-
-
PLZ vom Ortsteil Plänterwald
12435
12437
-
-
-
-
PLZ vom Ortsteil Rahnsdorf
12587
12589
-
-
-
-
Postleitzahl Berlin Schmöckwitz
12527
-
-
-
-
-"""

five_digit_substrings = re.findall(r'\b\d{5}\b', plz_string)

def get_random_plz():
    return random.choice(five_digit_substrings)
