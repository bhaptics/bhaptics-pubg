# bhaptics-pubg

## Requirements
* opencv-python
* numpy
* pynput
* websocket-client
* d3dshot
* cx_freeze 


## Description
### When the player is attacked(Reducee HP)
* Damage which over 15 damage
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
* Interacting with key F
* Detecting kill log 
* Heartbeat effects on the vest when your health is low and very low
* Detect game states(ingame, practice mode, falling, waiting room)

### Developmented but not included main

z_named files are raw codes which not included in main
* Run by key events and map movements(Completed)
* Vehicle differentiation(Completed)
* Explosion events using sound detection(Failed)
* Impact detection by screen wobble(Failed)
* Detecting zone by map color image(Failed)
