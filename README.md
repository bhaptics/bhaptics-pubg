# bhaptics-pubg

## SUMMARY

bHaptics Tactsuit integration mod for PLAYERUNKNOWN'S BATTLEGROUNDS(PUBG). 
Many different haptic effects on Vest including feedback from enemy attac, gun damage, player weapon fire, reload,
item changing, healing, heartbeat and more. By screen captureing and key events, program detects these events 

## Settings
* **BORDERLESS** game screen setting.
* **English** game language setting

## Requirements

Developed on Python 3.7.9 64-bit
* opencv-python
* numpy
* pynput
* websocket-client
* d3dshot
* cx_freeze 

## Description
### When the player is attacked(Reducee HP)
* Damage which over 7 damage
* Bluezone Haptic per 1 damage accumulation

### When the player fights
* Which type the player attacks (Punch, Throw, Fire) 
* Gun reload when completed reload
* Different haptic depending on which slot the weapon was swapped.
* Aim when player using gun

### When the player is riding vehicle

Air sequence is binded with different methods
* Airplane - Free fall - Parachute active - Parachute - Landing
* Car and Boat

Program can returns each ridings speed value

### Special Events
* Using heal items and gas
* Interacting with key F like open door and pick helmet.
* Detecting kill log
* Heartbeat effects on the vest when your health is low.
* Detect game states(ingame, practice mode, falling, waiting room)

### Developmented but not included main

z_named files are raw codes which not included in main
* Run by key events and map movements(Completed)
* Vehicle differentiation(Completed)
* Explosion events using sound detection(Failed)
* Impact detection by screen wobble(Failed)
* Detecting zone by map color image(Failed)

## CONFIGURATION

This mod has a Settings window in the application. 
Player can modify intensity of haptics and test the effects by click the button.
Modified intensities are applyed when clicked "apply" button
If the setting window is closed, the program exits
Player can check which haptic events are playing.
By chaning tacts files on TactFiles folder. Player can change types of haptics

![Player GUI](https://user-images.githubusercontent.com/76416010/108648563-ea848280-74fe-11eb-957b-59ccf682415b.png)


## Issues
* As this program mostly depending on screen capturing, the full-screen gameplay is compulsory.
* d3dshot screen capture module halts when PUBG is executing Full-screen mode.
* Unstable resolution availability
* If the player use mouse wheel for weapon swap, the program will not know which slot of weapon is holding.
