from os import name, system
from sys import exit
import time
import random

# function to clear the console screen based on current OS
def clearScreen():
	if name == 'nt':
		_ = system('cls')
	else:
		_ = system('clear')


##### SETUP #####
motd = ["Totally not a snake btw!", "This is NOT Pong!", "May the juice be with you!", "I swear these messages aren't random!", "42 is the answer to everything", "Do people even read these?", "\"Hello there!\" :D", "RTFM", "The monster under your bed is a lie!", "I forgot to write this one...", "\"Arch Linux btw\"", "Don't name the character Tom!", "Have you tried hard mode already?", "Maybe you should try to beat the game!", "Computer says NO!", "Frozen Hot Dogs!", "The most underrated game of 2022!", "101% functional with negative bugs!", "Maybe there are more tips where this came from...", "Route will be recalculated...", "You can trust the funny Skeleton!", "You aren't actually the player!", "You can (probably) safely ignore most of these!"]
# interchangeable words as tuples, allows for use of similar strings (e.g. north & up ) in commands
UP = 'up', 'north'
DOWN = 'down', 'south'
LEFT = 'left', 'west'
RIGHT = 'right', 'east'
BACK = 'back', 'b'
EXIT = 'exit', 'x', 'e'
HELP = 'help', 'h', 'man'
PLAY = 'play', 'p'

# dictionary linking zones to other zones
zones = {
        'Hall' : {
                DOWN : 'Kitchen',
                UP : 'Library',
                RIGHT : 'Dining Room',
                LEFT : 'Laboratory',
                'item' : 'Key',
                'monster' : False
            },
        'Kitchen' : {
                UP : 'Hall',
                'monster' : False
            },
        'Dining Room' : {
                LEFT : 'Hall',
                DOWN : 'Garden',
                'item' : 'Potion',
                'monster' : False
            },
        'Garden' : {
                UP : 'Dining Room',
                'monster' : False
            },
        'Library' : {
                DOWN : 'Hall',
                RIGHT : 'Office',
                'item' : 'Book of Life',
                'monster' : False
            },
        'Office' : {
                LEFT : 'Library',
                UP: 'Bedroom',
                DOWN : 'Dining Room',
                'monster' : False
            },
        'Laboratory' : {
                RIGHT : 'Hall',
                LEFT : 'Secret Room',
                'item' : 'Beam-O-Mat',
                'monster' : False
            },
        'Secret Room' : {
                RIGHT : 'Laboratory',
                'item' : 'The Number 42',
                'monster' : False
            },
        'Bedroom' : {
                DOWN : 'Office',
                'monster' : False
            }
	}

# dont do this btw?
def resetZones():
    zones.clear()
    zones.update({
        'Hall' : {
                DOWN : 'Kitchen',
                UP : 'Library',
                RIGHT : 'Dining Room',
                LEFT : 'Laboratory',
                'item' : 'Key',
                'monster' : False
            },
        'Kitchen' : {
                UP : 'Hall',
                'monster' : False
            },
        'Dining Room' : {
                LEFT : 'Hall',
                DOWN : 'Garden',
                'item' : 'Potion',
                'monster' : False
            },
        'Garden' : {
                UP : 'Dining Room',
                'monster' : False
            },
        'Library' : {
                DOWN : 'Hall',
                RIGHT : 'Office',
                'item' : 'Book of Life',
                'monster' : False
            },
        'Office' : {
                LEFT : 'Library',
                UP: 'Bedroom',
                DOWN : 'Dining Room',
                'monster' : False
            },
        'Laboratory' : {
                RIGHT : 'Hall',
                LEFT : 'Secret Room',
                'item' : 'Beam-O-Mat',
                'monster' : False
            },
        'Secret Room' : {
                RIGHT : 'Laboratory',
                'item' : 'The Number 42',
                'monster' : False
            },
        'Bedroom' : {
                DOWN : 'Office',
                'monster' : False
            }
	})

# player class initializing the attributes for the player
class player:
	def __init__(self):
		self.location = 'Hall'
		self.game_over = False
		self.win = False
		self.inventory = []
myPlayer = player()

# dont do this btw?
def resetPlayer():
    myPlayer.location = 'Hall'
    myPlayer.game_over = False
    myPlayer.win = False
    myPlayer.inventory = []


##### GAME FUNCTIONALITY #####
def printMenu():
	print(f'''
+————————————————————————————————————————————————————————————————————+
|The critically acclaimed game, with a free trial that lasts forever!|
+————————————————————————————————————————————————————————————————————+

 Tip:   {random.choice(motd)}

+——<Commands>————————————————————————————————————————————————————————+
|			      > play <                               |
|			      > help <                               |
|			      > exit <                               |
+————————————————————————————————————————————————————————————————————+
''')

# print a help screen
def printHelp():
    print(f'''
+————————————————————————————————————————————————————————————————————+
|                               Help                                 |
+————————————————————————————————————————————————————————————————————+

 Goal of the game:  
                    Don't get killed and escape!

 Use commands to interact with the game world.
 Most screens have the available commands shown on screen.
 For some commands short forms work aswell! (see full list below)


 Use the command 'back' or 'b' to resume the game!

+——<Full list of commands>———————————————————————————————————————————+
|       Game:                                                        |
|                       go [direction]                               |
|                     -> moves in the specified direction            |
|                       valid directions are:                        |
|                           north, south, west, east                 |
|                           up, down, left, right                    |
|                                                                    |
|                       get [item]                                   |
|                     -> takes the specified item                    |
|                                                                    |
|                                                                    |
|       Menus:                                                       |
|                       play (short: 'p')                            |
|                                                                    |
|                       help (short: 'h', 'man')                     |
|                     -> prints this screen                          |
|                                                                    |
|                       exit (short: 'e', 'x')                       |
|                                                                    |
|                       back (short: 'b')                            |
|                     -> resume playing (only in help screen)        |
|                                                                    |
+————————————————————————————————————————————————————————————————————+
''')

# print UI elements for the actual game screen
def printUI():
    spacer = f'                                     |'
    curItem = ''
    if 'item' in zones[myPlayer.location]:
        curItem = zones[myPlayer.location]['item']
    else:
        curItem = ''
    # slice/remove spaces to match with border box
    areaSpacer = (spacer[len(myPlayer.location):])
    itemSpacer = (spacer[len(curItem):])
    print(f'''
+————————————————————————————————————————————————————————————————————+
|   Current Area:               {myPlayer.location}{areaSpacer}
|   Item in Area:               {curItem}{itemSpacer}
+————————————————————————————————————————————————————————————————————+

+——<Inventory>———————————————————+  +——<Map>—————————————————————————+''')
    printMI()
    print(f'''
+——<Commands>————————————————————————————————————————————————————————+
|			        go [direction]                       |
|			        get [item]                           |
+————————————————————————————————————————————————————————————————————+
''')

# print map and inventory
def printMI():
    miString = []
    tmp = ''
    map = []
    inventory = []
    map = buildMapString().splitlines()
    inventory = buildInventoryString(map.count('\n'), inventory.count('\n')).splitlines()

    if len(map) == len(inventory):
        for i in range(len(map)):
            miString.append(f'{inventory[i]}  {map[i]}')
    elif len(map) > len(inventory):
        for i in range(len(map)):
            if (len(inventory)) > i:
                miString.append(f'{inventory[i]}  {map[i]}')
            else:
                miString.append(f'                                    {map[i]}')
    elif len(map) < len(inventory):
        for i in range(len(inventory)):
            if (len(map)) > i:
                miString.append(f'{inventory[i]}  {map[i]}')
            else:
                miString.append(f'{inventory[i]}')
    print('\n'.join(miString))

# build map dynamically from current player location and surrounding zones
def buildMapString():
    spacer = '|                                |'
    uAbrv = '  '
    dAbrv = '  '
    lAbrv = '  '
    rAbrv = '  '

    for direction in [UP, DOWN, LEFT, RIGHT]:
        if direction in zones[myPlayer.location]:
            if direction == UP:
                uAbrv = (zones[myPlayer.location][direction])[:2]
            elif direction == DOWN:
                dAbrv = (zones[myPlayer.location][direction])[:2]
            elif direction == LEFT:
                lAbrv = (zones[myPlayer.location][direction])[:2]
            else:
                rAbrv = (zones[myPlayer.location][direction])[:2]
            
    mapString = f'''{spacer}
|             +————+             |
|             | {uAbrv} |             |
|             +————+             |
|      +————+ +————+ +————+      |
|      | {lAbrv} | |>{myPlayer.location[:2]}<| | {rAbrv} |      |
|      +————+ +————+ +————+      |
|             +————+             |
|             | {dAbrv} |             |
|             +————+             |
{spacer}
+————————————————————————————————+'''
    return mapString

# build the inventory list string from myPlayer.inventory
def buildInventoryString(mapLines = 0, invLines = 0):
    spacer = '|                                |'
    invString = spacer
    if invLines == 0 or invLines < mapLines:
        for item in myPlayer.inventory:
            invSpacer = (spacer[len(item)+8:])
            invString = f'{invString}\n|       {item}{invSpacer}'
        while invString.count('\n') < mapLines:
            invString = f'{invString}\n{spacer}'
    else:
        for item in myPlayer.inventory:
            invSpacer = (spacer[len(item)+8:])
            invString = f'{invString}\n|       {item}{invSpacer}'
    invString = f'{invString}\n{spacer}\n+————————————————————————————————+'
    return invString

def handleMovement():
    cmd = ''
    while True:
        printUI()
        cmd = input('>')
        cmd = cmd.lower()
        if cmd == "":
            clearScreen()
            print('\nInvalid Command! See \'Commands\' or use the \'help\' command!')
        else:
            spcCount = cmd.count(' ')
            if spcCount:
                cmd = cmd.split(' ')
            # move/go logic
            if cmd[0] == 'go':
                if cmd[1] in UP and UP in zones[myPlayer.location]:
                    myPlayer.location = zones[myPlayer.location][UP]
                    clearScreen()
                elif cmd[1] in DOWN and DOWN in zones[myPlayer.location]:
                    myPlayer.location = zones[myPlayer.location][DOWN]
                    clearScreen()
                elif cmd[1] in LEFT and LEFT in zones[myPlayer.location]:
                    myPlayer.location = zones[myPlayer.location][LEFT]
                    clearScreen()
                elif cmd[1] in RIGHT and RIGHT in zones[myPlayer.location]:
                    myPlayer.location = zones[myPlayer.location][RIGHT]
                    clearScreen()
                else:
                    clearScreen()
                    print('\nYou can\'t go that way! ')
            # get item logic
            elif cmd[0] == 'get':
                itemName = ''
                # handle itemnames with spaces
                if spcCount >= 2:
                    for i in range(spcCount):
                        if i == 0:
                            itemName = cmd[i+1]
                        else:
                            itemName = f'{itemName} {cmd[i+1]}'
                else:
                    itemName = cmd[1]
                if 'item' in zones[myPlayer.location] and itemName in zones[myPlayer.location]['item'].lower():
                    myPlayer.inventory += [itemName]
                    clearScreen()
                    print(f'\n{itemName} got!')
                    del zones[myPlayer.location]['item']
                else:
                    clearScreen()
                    print(f'\nThere is no {itemName} in this room!')
            # print the help screen ingame
            elif cmd[0] in HELP:
                clearScreen()
                helpScreen(True)
                break
            else:
                clearScreen()
                print('\nInvalid Command! See \'Commands\' or use the \'help\' command!')
            # handle win/lose conditions below
            if zones[myPlayer.location]['monster'] == True:
                clearScreen()
                print('\nA monster has killed you! GAME OVER!')
                myPlayer.game_over = True
                break
            if myPlayer.location == 'Garden' and 'key' in myPlayer.inventory and 'potion' in myPlayer.inventory:
                clearScreen()
                print('\nYou escaped the house... YOU WIN!')
                myPlayer.win = True
                myPlayer.game_over = True
                break
            if myPlayer.location == 'Laboratory' and 'book of life' in myPlayer.inventory or 'beam-o-mat' in myPlayer.inventory:
                clearScreen()
                print('\nYou escaped into your own Pocket Dimension... YOU WIN!')
                myPlayer.win = True
                myPlayer.game_over = True
                break
            if myPlayer.location == 'Secret Room' and 'the number 42' in myPlayer.inventory:
                clearScreen()
                print('\n42!?!?!?!... YOU WIN?!?')
                myPlayer.win = True
                myPlayer.game_over = True
                break

# main game loop
def gameMain():
    choice = ''
    while myPlayer.game_over == False:
        handleMovement()

    while True:
        if myPlayer.win:
            print('\nCongratulations on beating the game!\nDo you want to close the game?\nY/N?\n')
        else:
            print('\nBetter luck next time...\nDo you want to close the game?\nY/N?\n')
        choice = input('>')
        choice = choice.lower()
        if choice in ['y', 'yes']:
            exit()
        elif choice in ['n', 'no']:
            resetPlayer()
            resetZones()
            main()
        else:
            clearScreen()
            print('\nInvalid Command! Use the command \'back\' (or \'b\') to resume playing!')


# help screen loop
def helpScreen(isIngame = None):
    c = ''
    while True:
        printHelp()
        c = input('>')
        c = c.lower()
        if c in BACK:
            if isIngame:
                clearScreen()
                gameMain()
                break
            else:
                clearScreen()
                mainMenu()
                break
        else:
            clearScreen()
            print('\nInvalid Command! Use the command \'back\' (or \'b\') to resume playing!')

# main menu loop
def mainMenu():
    choice = ''
    #use while True with breaks since looping with choice == '' ends up not working properly when pressing enter without an input? 
    while True:
        printMenu()
        choice = input('>')
        choice = choice.lower()
        if choice in PLAY:
            clearScreen()
            gameMain()
            break
        elif choice in HELP:
            clearScreen()
            helpScreen(False)
            break
        elif choice in EXIT:
            clearScreen()
            exit()
        else:
            clearScreen()
            print('\nInvalid Command! See \'Commands\' or use the \'help\' command!')

def randomizeMonster():
    keys = list(zones.keys())
    keys.remove('Hall')
    rnd = random.choice(keys)
    zones[rnd]['monster'] = True


# main function calls
def main():
    randomizeMonster()
    clearScreen()
    mainMenu()

if __name__ == '__main__':
    main()
