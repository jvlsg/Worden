# PROJECT HUSTON - Terminal Based Space Display 

## Goal
Aggregate information from several Space-related APIs into a single, cohesive and (hopefully) cool-looking terminal based interface

## Features
Display in separate screens/tabs the following:

### Assets
List all Active Stations & Expeditions(End >= Today) & Active Astronauts (Display more info on them)
    |- Stations (Space launch) [MVP]
    |- Expeditions (Space launch) [MVP]
    |- Satelites (n2yo) [Future]

### Launches
    |- Upcoming Launches and rocket information (Space Launch) [MVP]
    
### Solar System
    |- (Stuff on le-systeme) [Future]

### Maps
Display maps and rough position of A TRACKABLE OBJECT using Drawille
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


## Candidate APIs
https://spacelaunchnow.me/api/3.3.0/

https://open-notify.org/

https://www.n2yo.com/api/

https://api.le-systeme-solaire.net/swagger/#/bodies/get_bodies


https://celestrak.com/