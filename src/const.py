"""
CONSTANTS 
"""

import enum

#ms between calling while_waiting on the forms 
KEYPRESS_TIMEOUT =  100

class API_TYPES(enum.Enum):
    LAUNCHES = "LAUNCHES"
    EXPEDITIONS = "EXPEDITIONS"
    ASTRONAUTS = "ASTRONAUTS"
    SPACE_STATIONS = "SPACE STATIONS"

MSG_CONNECTION_ERROR = "Could not connect to the Internet\nTrying again in {} seconds".format(KEYPRESS_TIMEOUT/10)

OFFSET_DELTA = 20
