"""
CONSTANTS 
"""
import enum
from pathlib import Path

VERSION = "1.1.0"
#ms between calling while_waiting on the forms 
KEYPRESS_TIMEOUT =  100
#Default Offset Delta
DEFAULT_OFFSET_DELTA = 20


ROOT_DIR = Path(__file__).parent
DATA_DIR = (ROOT_DIR/"data").resolve()
MAP_IMAGE_FILEPATH = (  DATA_DIR / "mapimg.png").resolve()
MAP_IMAGE_THRESHOLD = 225

class API_TYPES(enum.Enum):
    LAUNCHES = "UPCOMING LAUNCHES"
    EVENTS = "UPCOMING EVENTS"
    ASTRONAUTS = "ACTIVE ASTRONAUTS"
    SPACE_STATIONS = "ACTIVE SPACE STATIONS"
    SOLAR_SYSTEM_BODIES = "SOLAR SYSTEM BODIES"

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
