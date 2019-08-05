# PROJECT HUSTON - Terminal Based Space Display 

## Goal
Aggregate information from several Space-related APIs into a single, cohesive and (hopefully) cool-looking terminal based interface

## Features
Display in separate screens/tabs the following:

### In-Orbit Assets
List all Active Stations & Expeditions(End >= Today) & Active Astronauts (Display more info on them)
    |- Stations (Space launch) [MVP]
    |- Expeditions (Space launch) [MVP]
    |- Satelites (n2yo) [Future]

### Launches
    |- Upcoming Launches and rocket information (Space Launch) [MVP]
    
### Solar System
    |- (Stuff on le-systeme) [Future]

### Maps & Tracking
Display maps and rough position of A TRACKABLE OBJECT
* World Map [MVP]
* Orbital Map [Future]
* Solar System Map [Future]


## UI Flow

### Tab 1: Launches
https://spacelaunchnow.me/api/3.3.0/launch/upcoming/ 

Left side: 
* BoxTitle all upcoming Launches by name / "No Upcoming Launches" warning / "No connection" warning
Right Side:
* mission Details
* pad: Name and Coordinates

Other Considerations: 
* Only 20 responses at a time

### Tab 2: Maps
Left Side:
* BoxTitle: World,Orbit,System
* Text: Can be used to dump stuff
Right Side:
* (For Now): Dump all info in a text box

Pager, TitlePager
    This widget displays lines of text, allowing the user to scroll through them, but not edit them. The text to display is held in the .values attribute.

### Tab 3, 4 & 5: Stations In-Orbit, Current Expeditions & Astronauts In-Orbit
Left Side:
* BoxTitle all active space stations / Expeditions / Astronauts
Right Side:
* (For Now): Dump all info in a text box



## Candidate APIs
https://spacelaunchnow.me/api/3.3.0/

https://open-notify.org/

https://www.n2yo.com/api/

https://api.le-systeme-solaire.net/swagger/#/bodies/get_bodies

https://celestrak.com/