"""
CONSTANTS 
"""
import enum
VERSION = "1.0"
#ms between calling while_waiting on the forms 
KEYPRESS_TIMEOUT =  100
#Default Offset Delta
DEFAULT_OFFSET_DELTA = 20

class API_TYPES(enum.Enum):
    LAUNCHES = "LAUNCHES"
    EXPEDITIONS = "EXPEDITIONS"
    ASTRONAUTS = "ASTRONAUTS"
    SPACE_STATIONS = "SPACE STATIONS"

MSG_CONNECTION_ERROR = "Could not connect to the Internet\nTrying again in {} seconds".format(KEYPRESS_TIMEOUT/10)

CONTROLS = {
    "update" : "^R",
    "track" : "^T",
    "increment_offset":">",
    "decrement_offset":"<",
}

MSG_CONTROLS_HELP = """
Controls: 
    Access the Main Menu with 'CONTROL+X'
    Use the ARROW KEYS to navigate the lists, press ENTER to select an option
    Flip through the pages with '<' ( SHIFT and , ) and '>' ( SHIFT and . )
    Track a selected object with 'CONTROL+T'
"""
