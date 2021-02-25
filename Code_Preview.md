# Preview
This programm is PUBG image detection module.  
It takes PUBG game screenshot and analyze it for bHaptic tactsuit or tactot.  
Take about 25 FPS screenshot.  
Best performance on 1920x1080, tested on 3440X1440  
Cause of d3dshot module, it needs BORDERLESS and ENGLISH PUBG game play


# Program Controller
## main.py
### main()
Make keyboard and mouse listener on  
Init images like number images  
Set mainflow() into new thread  
Set timer() into new thread  
Set GUI and if UI closes, all thread stops and program ends
### timer()
Screenshot frame rate controller
### mainflow()
Take screenshot  
Check what is screen's game phase  
Depends on game phase, execute stream() or airflow()
### stream()
Analyze gameplay screenshot. 
Passes what types of haptics this page needs.  
Detect Damage, Kill, Action, Bluezone, Vehicle, Reload, Swap, Aim  
### airflow()
Manage airplane->freefall->parachute->landing sequence  
Passes each types of haptics

## haptics.py
Play haptics  
Skip if same haptic type is playing  
Different type of haptic takes different alt

# Main game phase
![points](https://user-images.githubusercontent.com/76416010/108980497-12c2db80-76cf-11eb-942a-c915c2ee3d2c.png)

## isgame.py
Check 1, 2  
Number part white high, JOINED part white low.  
NOTGAME : 1 off  
PREGAME : Detects "MATCH STARTS IN"  
INGAME : 1 on, 2 off  
PRACTICE : 1 on, 2 on  

## findfire.py
### findfire()
Mouse left clicked, 3 on
* Punch : 5 off, 4 off
* Trhow : 5 off, 4 on
* Fire : 5 on, 4 change
### findaim()
* Aim : mouse right clicked, 3 on, 5 on
### reload()
* Reload : Within 150 screen, 4 on, 5 change

### bullet_num() 
Cut 4 into pieces (ex : 150 -> 1, 5, 0), check number images, returns bullet num

## findvehicle.py
### findvehicle() 
* Car : 9 gas log matches
Can get speed and vehicle type

## findweapon.py
### getwepnum()
* Swap : keyboard 1,2,3,4,5,x pressed, 4 or 5 change
Save previous 4, 5 stats and keyboard input to make swapin haptic
## findkill.py
### findkill()
* Kill : 10 red part is separated, 10 white part is on

## findaction.py
### findaction()
* Action : 8 circular gauge on, 7 matches
### findinter() 
* Interaction : 7 'F' matches

## getHP.py
### getHP()
Check 6. Get y direction sum.
When HP bar's first pixel is different to background.
Check the pixel's continuity.
When HP up is detected, check 5 more frames.
### damage()
* Bluezone : Check 6, accumulated over 1 HP reduce
* Damage : Check 6, more than 7 HP reduce
### isdead() :
Check 6, when 6 detected 0 HP and killer's name detected.

# Air Phase
![Air](https://user-images.githubusercontent.com/76416010/109091955-1602a980-7759-11eb-9c03-e553304d4a72.png)
## findplane.py
### findplane()
* Airplane : 1 on, 3 on
## findfalling.py
### findfalling()
Get speed when 1 on, 2 on, 4 on || 1 on, 2 off, 4 off
Cut 4 into pieces (ex : 217 -> 2, 1, 7), check number images, returns bullet num
## falltype()
* Freefall : Speed over 126
* Parachute actvie : First time speed under 126
* Parachute : After parachute active
* Landing : 2 on, 4 off
## isfalling()
Detect KM/H at 4 to check falling at practice mode
## isground() 
Check map's white to check player is on ground, not a setting or inventory page.

# Not Used Methods
## z_findexplode.py
Get sound output, apply Fourier transform and tried to get explode sound.  
Takes too many resources and hard to detect specific sounds
## z_findimpact.py
Tried to detect falling impact by screen shaking.  
## z_findrun.py
It successfully detects running by keyboard input and map movement.  
Too many haptic when it executes.
