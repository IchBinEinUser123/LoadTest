# FQDN with protocol
FQDN_WITH_PROTO = "REPLACE_ME"

# module name
MODULE_NAME = "SHPPOC"

# DB Metadata (Just for integrity reasons)
MIN_FALL_COUNT_PER_EDIS = 1000
MIN_AUFGABEN_PER_FALL = 10

# Probabilities (0 - 100)
UPLOAD_PROBABILITY = 10 # probability that SB attaches a file to Fall/Gespraech/Begleitung
SEARCH_PROBABILITY = 33 # probability that SB uses the search input (i.e. triggers additional server requests)

# Thresholds
MIN_WAIT_TIME = 10  # seconds
MAX_WAIT_TIME = 60  # seconds