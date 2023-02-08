# BTD 6 Farmer | Gameplanner Branch
<span style="font-size:16px;">Inspired from [RavingSmurfGB/Py_AutoBloons](https://github.com/RavingSmurfGB/Py_AutoBloons)</span>

[![Python application](https://github.com/linus-jansson/btd6farmer/actions/workflows/check_bot.yml/badge.svg?branch=main)](https://github.com/linus-jansson/btd6farmer/actions/workflows/check_bot.yml) 

Join the [Discord](https://discord.gg/qyKT6bzqZQ) for support, updates and sharing gameplans.

Feel free to make a pull request if you have any improvements or create a issue if something isn't working correctly!

# Make sure to read the main branch README.md for more information about the bot! This is only going to explain the usage of the gameplanner branch!
## Table Of Contents (TODO)
- [Setup file](#setup_file)
- [Gameplan file](#gameplan_file)
- [Instruction types](#instruction_types)
- [Gameplanner](#gameplanner)
    - [Placing Towers](#placing_towers)
    - [Keybinds](#keybinds)
        - [Upgrading Towers](#upgrading_towers)
        - [Changing Static Target](#changing_static_target)
        - [Changing Target](#changing_target)
        - [Starting Round](#starting_round)
        - [Save and Exit](#save_and_exit)
- [Stats](#stats)
- [Keyword cheatsheet](#keywords)
    - [Gamemodes](#gamemodes)
    - [Difficulties](#difficulties)
    - [Maps](#maps)
    - [Heros](#heros)
    - [Monkeys](#monkeys)


<a name="setup_file"/>

### setup.json
The setup file is used for the bot to know which hero, map, difficulty and gamemode it should use.
It should be named `setup.json` and be placed in the same directory as the gameplan.

```json
{
    "VERSION": "1",
    "HERO": "OBYN",
    "MAP": "DARK_CASTLE",
    "DIFFICULTY": "HARD_MODE",
    "GAMEMODE": "STANDARD_GAME_MODE",
}
```
> `Hero` - Which hero to use *[list of avaliable heros](#heros)*  \
> `MAP` - Which map to use *[list of avaliable maps](#maps)* \
> `DIFFICULTY` - Which Difficulty to use *[list of avaliable difficultues](#difficulties)* \
> `GAMEMODE` - Which Gamemode to use *[list of avaliable Gamemodes](#gamemodes)* \

At the end of the planner it will ask you if you want to save the setup file. If you answer yes it will save the setup file to the same directory as the instructions.

<a name="gameplan_file"/>

### instructions.json
#### Creating the gameplan and example
The gameplan is a json file that contains the round as a key and the value as an array with instructions. 
All coordinates are normalized to you'r screen resolution, to work with a wider range of computers. (a value between 0 and 1)

The following example instruction places a tower on the absolute center of the map and starts the game in fast forward mode, on round 3. See [instruction types](#instruction_types) for more information about the different types of instructions. 

```json
{
    "3": [
        {
            "INSTRUCTION_TYPE": "PLACE_TOWER",
            "ARGUMENTS": {
                "TOWER": "TOWER_TYPE",
                "POSITION": [ 0.5, 0.5 ]
            }
        },
        {
            "INSTRUCTION_TYPE": "START",
            "ARGUMENTS": {
                "FAST_FORWARD": true,
            }
        }
    ]
}

```

<a name="instruction_types"/>

##### instruction types
- `START` - Indicates the game
    - `FAST_FORWARD` - (true / false) Defaults to True. Should the bot play in fast forward mode?
- `PLACE_TOWER` - Place a tower on the map
    - `MONKEY` - Type of monkey to place 
    - `LOCATION` - [x, y] position of tower to be placed 
- `UPGRADE_TOWER` - Upgrade a tower on the map
    - `LOCATION` - [x, y]  position of tower to be upgraded
    - `UPGRADE_PATH` - [top, middle, bottom] array of upgrades eg [1, 0, 1]
- `CHANGE_TARGET` - changes target of a tower
    - `LOCATION` - [x, y] location of the tower
    - `TARGET` - target or targets eg [ "FIRST", "LAST", "STRONG" ]. Can be a string or a array of targets
    - `TYPE` - (SPIKE or REGULAR) [*Heli & gunner not yet supported*]
    - `DELAY` - *(optional)* Defaults to 3 delay between each target change. Can also be an array of delays. Can be one delay eg `2` for 2 seconds or multiple `[1, 3, 4]` to sleep for 1 second, 3 seconds and 4 seconds respectively for each target change.
- `REMOVE_TOWER` - Removes a tower
    - `LOCATION` - [x, y] location of the tower
- `SET_STATIC_TARGET`
    - `LOCATION` - [x, y] location of tower
    - `TARGET_LOCATION` - [x, y] location of target
- `END` - (OPTIONAL) Finished instructions


An instruction array in a round can have multiple objects that will be executed after each other. for example:
```json
    //...
    "33": [
        {
            "INSTRUCTION_TYPE": "PLACE_TOWER",
            "ARGUMENTS": {
                "MONKEY": "DRUID",
                "LOCATION": [ 0.399609375, 0.35347222222222224 ]
            }
        },
        {
            "INSTRUCTION_TYPE": "PLACE_TOWER",
            "ARGUMENTS": {
                "MONKEY": "DRUID",
                "LOCATION": [ 0.43984375, 0.35555555555555557 ]
            }
        },
        {
            "INSTRUCTION_TYPE": "PLACE_TOWER",
            "ARGUMENTS": {
                "MONKEY": "DRUID",
                "LOCATION": [ 0.479296875, 0.35833333333333334 ]
            }
        }
    ]
    //...
```

<a name="gameplanner"/>

# Gameplanner
The gameplanner is the tool you're looking for in this branch. It's a tool that can generate a gameplan for you based on keybinds.
This makes it easier for us to make Gameplans by actually playing the map and placing towers, only downside is YOU HAVE TO USE key binds for tower placements, upgrades and target changes. To use, run the GamePlanner.bat file and follow the instructions.

<a name="placing_towers"/>
## Keybinds to place towers
|Tower|Keybind|
|--|--|
"DART"|"q"
"BOOMERANG"|"w"
"BOMB"|"e"
"TACK"|"r"
"ICE"|"t"
"GLUE"|"y"
"SNIPER"|"z"
"SUBMARINE"|"x"
"BUCCANEER"|"c"
"ACE"|"v"
"HELI"|"b"
"MORTAR"|"n"
"DARTLING"|"m"
"WIZARD"|"a"
"SUPER"|"s"
"NINJA"|"d"
"ALCHEMIST"|"f"
"DRUID"|"g"
"BANANA"|"h"
"ENGINEER"|"l"
"SPIKE"|"j"
"VILLAGE"|"k"
"HERO"|"u"

When you start the planner it will ask you for a keybind to place a tower, you can only cancel this by pressing `ESC`. After you've placed a tower, it will ask you for the next keybind, until you press `O` to finish the gameplan.

<a name="keybinds"/>
## Keybinds
|Keybind|Action|
|--|--|
"O"|"Finish gameplan and exit + Start setup file configs"
"Ctrl+D"|"Upgrade Tower"
"Ctrl+R"|"Start Round"
"Ctrl+T"|"Change Static Target"
"Ctrl+C"|"Change Target"

You can use these keybinds instead of placing a tower

<a name="upgrading_towers"/>
### Upgrading towers
First, after using the keybind, click the tower you want to upgrade.
Use the keyboard keybinds for upgrading top, middle and bottom path. You can not use the mouse as the gameplanner relies on keybinds

|Keybind|Path|
|--|--|
","|"Top"
"."|"Middle"
"/"|"Bottom"

<a name="changing_static_target"/>
### Changing Static Target
First, after using the keybind, click the tower you want to change the target of.
Then, click the target position you want to change to.

<a name="changing_target"/>
### Changing Target
First, after using the keybind, click the tower you want to change the target of. NOTE: HOLD SHIFT WHILE CLICK TO SET IT TO SPIKE TYPE, otherwise it will be regular.
Then choose the target with the keyboard keybinds as shown below.

<details>
<summary>SPIKE TYPE</summary>
|Keybind|Target|
|--|--|
"1"|"NORMAL"
"2"|"CLOSE"
"3"|"FAR"
"4"|"SMART"
</details>

<details>
<summary>REGULAR TYPE</summary>
|Keybind|Target|
|--|--|
"1"|"FIRST"
"2"|"LAST"
"3"|"CLOSE"
"4"|"STRONG"
</details>

<a name="starting_round"/>
### Starting Round
Using the keybind it will add the starting round instruction, always fast fowrwarded

<a name="save_and_exit"/>
### Save and exit
Finally after you've finished the gameplan, you can save it by pressing `O`, then it will ask if you'd like to make a setup file. Note: This fully uses the console, no keybinds here.
This will ask for:
Hero (Defaults to QUINCY)
Map (Default to MONKEY_MEADOWS)
Difficulty (Default to EASY)
Gamemode (Default to STANDARD_GAME_MODE)

[CheatSheet](#keywords)

<a name="stats"/>

### Stats
[Experience points per level](https://bloons.fandom.com/wiki/Experience_Point_Farming)
|Rounds|Beginner|Intermediate|Advanced|Expert|
|--|--|--|--|--|
|1-40 (Easy)|21 400|23 540|25 680|27 820|
|31-60 (Deflation)|45 950|50 545|55 140|59 735|
|1-60 (Medium)|56 950|62 645|68 340|74 035|
|3-80 (Hard)|126 150|138 765|151 380|163 995|
|6-100 (Impoppable/CHIMPS)|231 150|254 265|277 380|300 495|

<a name="keywords"/>

#### Keyword cheatsheet for the setup file and the gameplan

<a name="gamemodes"/>
<details>
<summary>Gamemodes</summary>

|Gamemode|Keyword in file|
|--|--|
|Chimps|CHIMPS_MODE|
|Chimps|CHIMPS|
|Deflation|DEFLATION|
|Apopalypse|APOPALYPSE|
|Reverse|REVERSE|
|Military Only|MILITARY_ONLY|
|Magic monkeys only|MAGIC_MONKEYS_ONLY|
|Double HP MOABS|DOUBLE_HP_MOABS|
|Half cash|HALF_CASH|
|Alternate Bloons Rounds|ALTERNATE_BLOONS_ROUNDS|
|Impoppable|IMPOPPABLE|
|Standard|STANDARD_GAME_MODE|

</details>

<a name="difficulties"/>
<details>
<summary>Difficulties</summary>

|Difficulty|Keyword in file|
|--|--|
|Easy|EASY_MODE|
|Medium|MEDIUM_MODE|
|Hard|HARD_MODE|

</details>

<a name="maps"/>
<details>
<summary>Maps</summary>

|Monkey|Keyword in file|
|--|--|
|Monkey Meadow|MONKEY_MEADOW|
|Tree Stump|TREE_STUMP|
|Town Center|TOWN_CENTER|
|Scrapyard|SCRAPYARD|
|The Cabin|THE_CABIN|
|Resort|RESORT|
|Skates|SKATES|
|Lotus Island|LOTUS_ISLAND|
|Candy Falls|CANDY_FALLS|
|Winter Park|WINTER_PARK|
|Carved|CARVED|
|Park Path|PARK_PATH|
|Alpine Run|ALPINE_RUN|
|Frozen Over|FROZEN_OVER|
|In The Loop|IN_THE_LOOP|
|Cubism|CUBISM|
|Four Circles|FOUR_CIRCLES|
|Hedge|HEDGE|
|End Of The Road|END_OF_THE_ROAD|
|Logs|LOGS|
|Covered Garden|COVERED_GARDEN|
|Quarry|QUARRY|
|Quiet Street|QUIET_STREET|
|Bloonarius Prime|BLOONARIUS_PRIME|
|Balance|BALANCE|
|Encrypted|ENCRYPTED|
|Bazaar|BAZAAR|
|Adora's Temple|ADORAS_TEMPLE|
|Spring Spring|SPRING_SPRING|
|KartsNDarts|KARTSNDARTS|
|Moon Landing|MOON_LANDING|
|Haunted|HAUNTED|
|Downstream|DOWNSTREAM|
|Firing Range|FIRING_RANGE|
|Cracked|CRACKED|
|Streambed|STREAMBED|
|Chutes|CHUTES|
|Rake|RAKE|
|Spice Islands|SPICE_ISLANDS|
|Midnight Mansion|MIDNIGHT_MANSION|
|Sunken Columns|SUNKEN_COLUMNS|
|X Factor|XFACTOR|
|Mesa|MESA|
|Geared|GEARED|
|Spillway|SPILLWAY|
|Cargo|CARGO|
|Pat's Pond|PATS_POND|
|Peninsula|PENINSULA|
|High Finance|HIGH_FINANCE|
|Another Brick|ANOTHER_BRICK|
|Off The Coast|OFF_THE_COAST|
|Cornfield|CORNFIELD|
|Underground|UNDERGROUND|
|Sanctuary|SANCTUARY|
|Ravine|RAVINE|
|Flooded Valley|FLOODED_VALLEY|
|Infernal|INFERNAL|
|Bloody Puddles|BLOODY_PUDDLES|
|Workshop|WORKSHOP|
|Quad|QUAD|
|Dark Castle|DARK_CASTLE|
|Muddy Puddles|MUDDY_PUDDLES|
|#Ouch|OUCH|

</details>

<a name="heros"/>
<details>
<summary>Heros</summary>

|Monkey|Keyword in setupfile|
|--|--|
|Quincy|QUINCY|
|Gwendolin|GWENDOLIN|
|Striker Jones|STRIKER_JONES|
|Obyn Greenfoot|OBYN|
|Captain Churchill|MONKEY|
|Benjamin|BENJAMIN|
|Ezili|EZILI|
|Pat Fusty|PAT_FUSTY|
|Adora|ADORA|
|Admiral Brickell|ADMIRAL_BRICKELL|
|Etienne|ETIENNE|
|Sauda|SAUDA|
|Psi|PSI|
|Geraldo|GERALDO|

</details>

<a name="monkeys"/>
<details>
<summary>Monkeys</summary>

|Monkey|Keyword in instruction|
|--|--|
|Hero|HERO|
|Dart Monkey|DART|
|Boomerang Monkey|BOOMERANG|
|Bomb Shooter|BOMB|
|Tack Shooter|TACK|
|Ice Monkey|ICE|
|Glue Gunner|GLUE|
|Sniper Monkey|SNIPER|
|Monkey Sub|SUBMARINE|
|Monkey Buccaneer|BUCCANEER|
|Monkey Ace|ACE|
|Heli Pilot|HELI|
|Mortar Monkey|MORTAR|
|Dartling Gunner|DARTLING|
|Wizard Monkey|WIZARD|
|Super Monkey|SUPER|
|Ninja Monkey|NINJA|
|Alchemist|ALCHEMIST|
|Druid|DRUID|
|Banana Farm|BANANA|
|Spike factory|SPIKE|
|Monkey Village|VILLAGE|
|Engineer Monkey|ENGINEER|

</details>