import mouse
import keyboard
import os
import json
import time
from Utils.monitor import width, height
import Utils.static as static
from Utils.BotUtils import BotUtils

sound = True # Set to False if you don't want to hear the beeps

if sound:
    if os.name == 'nt': # Windows
        from winsound import Beep # THIS IS WINDOWS ONLY
    else: # Linux
        def Beep(frequency, duration):
            # Linux beep: apt-get install beep
            os.system(f'beep -f {frequency} -l {duration}')
else:
    def Beep(frequency, duration): # Dummy function
        pass

save_path = "gameplans/NewGameplan"

if not os.path.isdir(save_path):
    os.makedirs(save_path)

inst = BotUtils(DEBUG=True)

result = {}
setup = {}
last_round = "1"

def stepformat(type, args):
    step = {}
    step["INSTRUCTION_TYPE"] = type
    step["ARGUMENTS"] = {}
    for arg in args:
        step["ARGUMENTS"][arg] = args[arg]

    return step

def play_beep(freq, time=300): #800 beep, 450 boop
    Beep(freq, time)


def find_tower(letter):
    for tower in static.tower_keybinds:
        if static.tower_keybinds[tower] == letter:
            return tower
    return None

def add_tower_step(step_args, round):
    global result, last_round

    step = stepformat("PLACE_TOWER", {"MONKEY": step_args[0], "LOCATION": [step_args[1], step_args[2]]})

    if round is None:
        round = last_round
    else:
        last_round = round = str(round)
        
    if round in result:
        result[round].append(step)
    else:
        result[round] = [step]

def upgrade_tower_step(step_args, path, round):
    global result, last_round

    step = stepformat("UPGRADE_TOWER", {"LOCATION": [step_args[0], step_args[1]], "UPGRADE_PATH": path})

    if round is None:
        round = last_round
    else:
        last_round = round = str(round)
        
    if round in result:
        result[round].append(step)
    else:
        result[round] = [step]

def set_static_target_step(tower_args, target_args, round):
    global result, last_round

    step = stepformat("SET_STATIC_TARGET", {"LOCATION": [tower_args[0], tower_args[1]], "TARGET": [target_args[0], target_args[1]]})

    if round is None:
        round = last_round
    else:
        last_round = round = str(round)
        
    if round in result:
        result[round].append(step)
    else:
        result[round] = [step]

def change_target_step(tower_args, target_args, round):
    global result, last_round

    step = stepformat("CHANGE_TARGET", {"LOCATION": [tower_args[0], tower_args[1]], "TYPE":target_args[0], "TARGET": target_args[1]})

    if round is None:
        round = last_round
    else:
        last_round = round = str(round)
        
    if round in result:
        result[round].append(step)
    else:
        result[round] = [step]

def start_round_step(round):
    global result, last_round

    step = stepformat("START", {"FAST_FORWARD": True})

    if round is None:
        round = last_round
    else:
        last_round = round = str(round)
        
    if round in result:
        result[round].append(step)
    else:
        result[round] = [step]
    
def clean():
    os.system('cls' if os.name == 'nt' else 'clear')  #-- Added this for Linux
    for tower in static.tower_keybinds:
        print(static.tower_keybinds[tower].upper() + ". " +tower)

    print("Choose a tower to place, press ctrl+d to upgrade, ctrl+t set_static_target, ctrl+c change_target, ctrl+r start, press O to save and exit")

while True:
    clean()
    while True:
        k = keyboard.read_key().lower()
        if k in static.tower_keybinds.values() and not keyboard.is_pressed("ctrl"): # Place tower
            letter = k
            break
        elif k == 'o': # Save and exit
            play_beep(300,500)
            with open(f'{save_path}/instructions.json', 'w') as f:
                json.dump(result, f, indent=3)
            
            d = input("Do you want to make the setupfile? (yes/y), press enter to skip.")
            if "y" in d.lower():
                setup["VERSION"] = "1"

                hero = input("Hero: ").upper()
                if hero not in static.hero_positions:
                    print("Invalid hero, defaulting to Quincy")
                    hero = "QUINCY"
                setup["HERO"] = hero

                map = input("Map: ").upper()
                if map not in static.maps:
                    print("Invalid map, defaulting to MONKEY_MEADOW")
                    map = "MONKEY_MEADOW"
                setup["MAP"] = map

                difficulty = input("Difficulty: ").upper()
                if difficulty not in ["EASY_MODE", "MEDIUM_MODE", "HARD_MODE"]:
                    print("Invalid difficulty, defaulting to EASY_MODE")
                    difficulty = "EASY_MODE"
                setup["DIFFICULTY"] = difficulty

                gamemode = input("Gamemode: ").upper()
                if gamemode not in ["CHIMPS_MODE","CHIMPS","PRIMARY_ONLY","DEFLATION","APOPALYPSE","REVERSE","MILITARY_ONLY","MAGIC_MONKEYS_ONLY","DOUBLE_HP_MOABS","HALF_CASH","ALTERNATE_BLOONS_ROUNDS","IMPOPPABLE","STANDARD_GAME_MODE"]:
                    print("Invalid gamemode, defaulting to STANDARD_GAME_MODE")
                    gamemode = "STANDARD_GAME_MODE"
                setup["GAMEMODE"] = gamemode

                with open(f'{save_path}/setup.json', 'w') as f:
                    json.dump(setup, f, indent=3)
            exit()
        elif k == 'd' and keyboard.is_pressed("ctrl"): # Upgrade
            err = None
            print("Click on the map where you want to upgrade, or esc to cancel")
            round = inst.getRound()
            play_beep(700)
            while True:
                if mouse.is_pressed(button='left'):
                    play_beep(800)
                    x, y = mouse.get_position()
                    w_norm, h_norm = x / width, y / height
                    top = 0
                    middle = 0
                    bottom = 0
                    print("press , to upgrade top path, . to upgrade middle path, / to upgrade bottom path, or esc to finish")
                    while True:
                        print("top: " + str(top) + " middle: " + str(middle) + " bottom: " + str(bottom))
                        key = keyboard.read_key()
                        match key:
                            case ",": top += 1; play_beep(350,200)
                            case ".": middle += 1; play_beep(300,200)
                            case "/": bottom += 1; play_beep(400,200)
                            case "esc": break
                        while keyboard.is_pressed(key):
                            pass
                        
                    if any([top>5, middle>5, bottom>5]):
                        err = "Can't upgrade a tower more than 5 times"
                        break
                    elif top>=1 and middle>=1 and bottom>=1:
                        err = "Can't upgrade more than 2 paths at once"
                        break

                    upgrade_tower_step((w_norm,h_norm),[top,middle,bottom],round)
                    play_beep(800)
                    break
                elif keyboard.is_pressed("esc"):
                    play_beep(450)
                    break
            clean()
            if err:
                print(err)
        elif k == 't' and keyboard.is_pressed("ctrl"): # set static target
            print("Click on the map where the tower is, or esc to cancel")
            round = inst.getRound()
            play_beep(700)
            while True:
                if mouse.is_pressed(button='left'):
                    play_beep(800)
                    x, y = mouse.get_position()
                    w_norm, h_norm = x / width, y / height
                    print("Click on the map where you want to set the target, or esc to cancel")
                    while mouse.is_pressed(button='left'):
                        pass
                    while True:
                        if mouse.is_pressed(button='left'):
                            play_beep(350)
                            x, y = mouse.get_position()
                            w_norm_target, h_norm_target = x / width, y / height
                            set_static_target_step((w_norm,h_norm),(w_norm_target,h_norm_target),round)
                            break
                        elif keyboard.is_pressed("esc"):
                            play_beep(450)
                            break
                    break
                elif keyboard.is_pressed("esc"):
                    play_beep(450)
                    break
            clean()
        elif k == 'c' and keyboard.is_pressed("ctrl"): # change target
            print("Click on the map where the tower is, if shift is pressed: SPIKE else REGULAR, or esc to cancel")
            round = inst.getRound()
            play_beep(700)
            while True:
                if mouse.is_pressed(button='left'):
                    if keyboard.is_pressed("shift"):
                        type = "SPIKE"
                        target_list = ["NORMAL", "CLOSE", "FAR", "SMART"]
                    else:
                        type = "REGULAR"
                        target_list = ["FIRST","LAST","CLOSE","STRONG"]

                    play_beep(900)

                    x, y = mouse.get_position()
                    w_norm, h_norm = x / width, y / height
                    target = None
                    for num, item in enumerate(target_list):
                        print(str(num+1) + ". " + item)
                    print("Choose target number, or esc to cancel")
                    while True:
                        k = keyboard.read_key().lower()
                        match k:
                            case "1": target = target_list[0]; break
                            case "2": target = target_list[1]; break
                            case "3": target = target_list[2]; break
                            case "4": target = target_list[3]; break
                            case "esc": play_beep(450); break

                    if target:
                        play_beep(800)
                        change_target_step((w_norm,h_norm),(type,target),round)
                        break
                elif keyboard.is_pressed("esc"):
                    play_beep(450)
                    break
            clean()
        elif k == 'r' and keyboard.is_pressed("ctrl"): # start
            print("Setting starting round")
            play_beep(800)
            start_round_step(inst.getRound())

    tower = find_tower(letter)
    if tower:
        play_beep(650)
        print("Click on the map where you want to place the tower, or esc to cancel")
        while True:
            if mouse.is_pressed(button='left'):
                x, y = mouse.get_position()
                w_norm, h_norm = x / width, y / height
                time.sleep(1.3)
                round = inst.getRound()
                add_tower_step((tower, w_norm, h_norm), round)
                play_beep(800)
                break
            elif keyboard.is_pressed("esc"):
                play_beep(450)
                break