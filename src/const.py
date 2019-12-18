"""
CONSTANTS 
"""

import enum

class API_TYPES(enum.Enum):
    LAUNCHES = "launches"
    EXPEDITIONS = "expeditions"
    ASTRONAUTS = "ASTRONAUTS"
    SPACE_STATIONS = "SPACE STATIONS"



OFFSET_DELTA = 20

#ms between calling while_waiting on the forms 
KEYPRESS_TIMEOUT =  30