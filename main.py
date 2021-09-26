# Rags to Riches
# This iteration has a working introduction, map walking, forest scene, a new map dimension to fit the screen, updated void text

# Imports
from functions import engPrint, engInp, mapPrint, defAnswer, move, updateMap, returnToPrev
from battle import battleTutorial, battleLootedCamp, battleKnights

from termcolor import colored
import time

# Initialize game
print("\033[H\033[J") # clear terminal

# Setting up different game information
inventory = ["letter / magical map", "ragged clothing"]
trueMap = [['Void', 'Resource Market', 'Holy Temple', 'Holy Fountain', 'Demonic Path',
  'Void', 'Void'],
 ['Recruiting Station', 'Crime City', 'Chambers', 'Heavenly Forge',
  'Demonic Temple', 'Port Shore', 'Void'],
 ['Copper Mine', 'Looted Camps', 'Path (Top)', 'Elkwood Forest',
  'Elkwood Forest', 'Port Shore Dock', 'Void'],
 ['Void', 'Void', 'Path (Bottom)', 'Elkwood Forest', 'Elkwood Forest',
  'Elkwood Forest', 'Void'],
 ['Void', 'Void', 'Knights', 'Elkwood Forest', 'Elkwood Forest',
  'Forest Hideout', 'Void'],
 ['Void', 'Void', 'Red Knights', 'Plains', 'Plains', 'Hilly Plains', 'Void'],
 ['Moat', 'Moat', 'Moat', 'Moat', 'Moat', 'Flat Plains', 'Void'],
 ['Moat', 'Castle Plaza', 'Castle Center', 'Castle Plaza', 'Moat',
  'Mine Entrance', 'Iron Mine']]
magicMap = [['', '', '', '', '', '', ''],
 ['', '', 'Chambers', '', '', '', ''],
 ['', '', '', '', '', '', ''],
 ['', '', '', '', '', '', ''],
 ['', '', '', '', '', '', ''],
 ['', '', '', '', '', '', ''],
 ['', '', '', '', '', '', ''],
 ['', '', '', '', '', '', '']]
ycord = 1
xcord = 2
# "Check if true" variables. Basically, these act as checkpoints. In the future, since I made so many of these, it might be clever to put them in a dictionary instead.
metoldman = False 
attackoldman = False
attackmetoldman = False
foughtGremlin = False
foughtThugs = False
foughtKnights = False
mineAccess = False
upgradedPotion = False
visitedCopperMines = False
dead = False

# Battle Stats
attack = 5
maxhealth = 40
health = maxhealth
healthregen = [3, 3] # Health Regen In Combat, First Term is Regen Value, the Second Term is Regen Turns

# Gameplay Functions
def introduction():
  engPrint('You open the paper and read it:')
  engPrint('Those with the strongest materials will make the strongest weapons, and those in possession of the strongest weapons will hold ultimate authority. \n\nTravel on the Southern path and go East after a while, you will find me in Elkwood Forest. You probably don\'t remember me, but I have a debt to repay to you. I will make you a set of wooden tools.', "red")
  print(colored('.' * 50 + "\n", "red"))
  engPrint('By the way, since you forgot everything, this might be helpful to know.', "red")
  inp = engInp('You can check what you have on you by typing "inventory" or "i." Here, try doing so.', "red").lower()
  defAnswer(inp, ["i", "inventory"], [])
  print("Your inventory: ")
  print(inventory, end="\n\n")
  inp = engInp('As you probably saw from checking your inventory, this letter also serves as a magical map, which will update the locations that you have visited. The  ★  indicates your current location. You can read the map by typing "map" or "m." It\'s a wonderful function, so you might as well use it (like, right now)!', "red").lower()
  defAnswer(inp, ["m", "map"], [])
  mapPrint(magicMap, xcord, ycord)
  inp = engInp('You can look around you by typing "look" or "l." Try it out!', "red").lower()
  engPrint('You can move East by typing "east" or "e", West by typing "west" or "w", North by typing "n" or "north", and South by typing "s" or "south". If you ever forget all of this, you can also type "help" or "h" in order to read this message again. Alright, now go and find me in Elkwood Forest! (South-East Direction)', "red")
  print(colored('.' * 50 + "\n", "red"))
  print("")

def main():
  global xcord, ycord, magicMap, trueMap
  # Begin main gameplay loop
  while True:
    global prevxcord, prevycord
    prevxcord, prevycord = xcord, ycord
    inp = engInp("What will you do?").lower()
    if inp in ["m", "map"]: # Map Command
      mapPrint(magicMap, xcord, ycord)
      continue
    elif inp in ["i", "inventory"]: # Inventory Command
      print(inventory, end="\n\n")
      continue
    else: # Invalid Command
      xcord, ycord, msg = move(xcord, ycord, inp, magicMap, trueMap)
      if msg == "":
        msg = "I didn't understand your command so nothing happened."
      magicMap = updateMap(xcord, ycord, magicMap, trueMap)
    engPrint(msg + " You are currently at the " + magicMap[ycord][xcord] + ".")
    turnContinue = False
    checkLocation()
    if turnContinue == True:
      continue
    if dead == True: # Death check
      engPrint("Rest in Pieces, you are dead now... Good game...")
      break

# checks if the current location of the user triggers any special events
def checkLocation():
  global xcord, ycord, prevycord, prevxcord, turnContinue, inp
  forest()
  knights()
  moat()
  void()
  pathbottom()
  mineEntrance()
  lootedcamps()
  religionGrounds()
  crimeCity()
  resourceMarket()
  copperMines()
def forest(): # This is what happens if the user encounters the old man in the forest
  global xcord, ycord, prevycord, prevxcord, attackoldman, metoldman, turnContinue, inp, dead, attack, attackmetoldman
  if magicMap[ycord][xcord] == "Forest Hideout" and metoldman == False: # Forest Scene
    inp = engInp("You have found the old man! His face is wrinkled, he is leaning on a shiny cane, and you can make out some type of lotus symbol on his robes. Will you approach him?", "red").lower()
    while True:
      if inp in ["yes", "y", "approach"]:
        engPrint("You move closer to him, though staying cautious. 'Welcome, old friend!' He says cheerfully. 'Can you go get me some wood? There's some on the ground there, though I'm afraid my body is too old to pick it up. I'll make you the set of wooden tools as promised.' For some reason, you feel as if you have a grudge against him...", "red")
        inp = engInp("What will you do?", "red").lower()
        while True:
          if inp in ["kill", "a", "attack", "kill old man", "attack old man", "kill man", "attack man"]:
            if attackoldman == False:
              engPrint("'You should know that you are far too weak to fight me right now. We might have been equals in the past, but you are nothing now.' He lifts his cane, which is suddenly glimmering in the light of the sun. You can feel your body being distorted. 'I'll return you to where you came from. Come and find me again. But don't try anything funny next time!'", "red")
              xcord, ycord = 2, 1 # teleports the user back to their starting point
              attackoldman = True
              attackmetoldman = True
              break
            elif attackoldman == True:
              engPrint("Well, I warned ya. Now you're dead.", "red") # kills the user if they have tried to kill the old man already before
              dead = True
              break
              
          elif inp in ["pick up wood", "find wood", "pick wood", "get wood", "collect wood", "gather wood", "acquire wood"]:
            inventory.append("wood")
            print("You have acquired some wood! Right now your inventory consists of: ", end="")
            print(inventory)
            engPrint("'Perfect! I'll get to making you some tools right now.'" , "red")
            engPrint("." * 30, speed=0.1)
            inventory.remove("wood")
            inventory.append("wooden pickaxe")
            inventory.append("wooden sword")
            attack = 8
            print("You have lost the wood, and you have acquired a set of wooden tools! Your inventory now consists of: ", end="")
            print(inventory)
            metoldman = True
            break
          elif inp in ["no", "n", "I don't want to", "don't pick up wood"]:
            engPrint("'Ah, a friend of nature, are we now? Well, it seems like you've kept some of your old tendecies. Well, you won't survive without some tools, so I'll give you an old set of mine.'" , "red")
            inventory.append("weird pickaxe") 
            inventory.append("weird sword")
            attack = 9
            print("You have acquired a set of weird tools! Your inventory now consists of: ")
            print(inventory)
            metoldman = True
            break
          inp = engInp("Sorry, I don't quite understand, what do you want to do?", "red").lower()
      elif inp in ["no", "n"]:
        engPrint("You have retreated to the " + magicMap[prevycord][prevxcord])
        ycord, xcord = prevycord, prevxcord
        break
      if metoldman == True:
        engPrint("The old man has left the forest after giving you the tools.", "red")
        break
      elif dead == True:
        time.sleep(1)
        quit()
        break
      elif attackmetoldman == True:
        engPrint("You have been teleported back to the Chambers")
        break
      else:
        inp = engInp("Sorry, I don't know what you mean. Will you approach him?", "red").lower()
def moat():
  global xcord, ycord, prevycord, prevxcord, turnContinue, inp
  if magicMap[ycord][xcord] == "Moat" and "boots of waterwalking" not in inventory: # Moat checking if user has water boots
      ycord, xcord = returnToPrev("Sorry, you'd drown if you went into the moat. If only you had something to help you stay afloat...", prevycord, prevxcord, magicMap)
      turnContinue = True
def knights():
  global xcord, ycord, prevycord, prevxcord, turnContinue, inp, health, maxhealth
  if trueMap[ycord][xcord] in ["Knights"]:
    if "copper sword" not in inventory and "leather armor" not in inventory and "copper sword" not in inventory: # Checking if void
      ycord, xcord = returnToPrev("The knights in front of you look quite well trained. Moreover, they are glistening with iron armor and swords. While you are more skilled at fighting than them, you might need better equipment to face all three of them...", prevycord, prevxcord, magicMap)
      turnContinue = True
    else:
      foughtKnights = battleKnights(health, healthregen, attack, "Thug", 0, 0, [], inventory)
      if foughtKnights == False:
        ycord, xcord = returnToPrev("", prevycord, prevxcord, magicMap)
      else:
        inventory.append("iron armor")
        health = 80
        maxhealth = health
      turnContinue = True
def void():
  global xcord, ycord, prevycord, prevxcord, turnContinue, inp
  if trueMap[ycord][xcord] in ["Void"]: # Checking if void
    ycord, xcord = returnToPrev("You cannot move this way, because the location is nothing but void. The destruction seems like it is from a massive battle between two powerful forces. It's almost as if this part of the land has been erased from existance...", prevycord, prevxcord, magicMap)
    turnContinue = True
def pathbottom():
  global xcord, ycord, prevycord, prevxcord, turnContinue, inp, foughtGremlin
  if trueMap[ycord][xcord] in ["Path (Bottom)"] and foughtGremlin == False:
    battleTutorial(health, healthregen, attack, "The Gnarly Gremlin", 40, 5, [], inventory)
    foughtGremlin = True
def mineEntrance():
  global xcord, ycord, prevycord, prevxcord, turnContinue, inp, foughtGremlin
  if trueMap[ycord][xcord] in ["Mine Entrance"] and mineAccess == False:
    ycord, xcord = returnToPrev("You don't have access to the Iron mine yet. Maybe you can find someone in the city to let you in...", prevycord, prevxcord, magicMap)
    turnContinue = True
def lootedcamps():
  global xcord, ycord, prevycord, prevxcord, turnContinue, inp, foughtThugs, health, maxhealth
  if trueMap[ycord][xcord] in ["Looted Camps"] and foughtGremlin == False:
    ycord, xcord = returnToPrev("The Thugs at the looted camps look rather intimidating. You should probably first fight the Gremlin on the path south to the chamber.", prevycord, prevxcord, magicMap)
  elif trueMap[ycord][xcord] in ["Looted Camps"] and foughtThugs == False:
    foughtThugs = battleLootedCamp(health, healthregen, attack, "Thug", 30, 5, [], inventory)
    if foughtThugs == False:
      engPrint("You should probably seek stronger weapons... Perhaps the wooden tools from the old man in the Forest Hideout (South-East) will suffice.")
      ycord, xcord = returnToPrev("", prevycord, prevxcord, magicMap)
    else:
      inventory.append("leather armor")
      inventory.append("gold coins")
      health = 60
      maxhealth = health
    turnContinue = True
def religionGrounds():
  global xcord, ycord, prevycord, prevxcord, turnContinue, inp, foughtThugs, health, maxhealth
  if trueMap[ycord][xcord] in ["Holy Temple", "Holy Fountain", "Demonic Path", "Demonic Temple", "Heavenly Forge"]:
    ycord, xcord = returnToPrev("You cannot enter any religious grounds without the blessing of a God.", prevycord, prevxcord, magicMap)
def crimeCity():
  global xcord, ycord, prevycord, prevxcord, turnContinue, inp, foughtThugs, health, maxhealth
  if trueMap[ycord][xcord] in ["Crime City"] and foughtThugs == False:
    ycord, xcord = returnToPrev("You try to enter Crime City, but you spot a group of a dozen Thugs. There are too many to deal with, but if you can take out their Leader, which you overhear is currently at the Looted Camps (South of Crime City), you will be able to enter the city freely.", prevycord, prevxcord, magicMap)
def resourceMarket():
  global xcord, ycord, prevycord, prevxcord, turnContinue, inp, foughtThugs, health, maxhealth, healthregen, upgradedPotion
  if trueMap[ycord][xcord] in ["Resource Market"] and upgradedPotion == False:
    engPrint("Welcome to the Resource Market, friend! Let's get you some better potions. In exchange, I'll be taking that gold of yours.", "green")
    engPrint("Your first choice is a large health potion. Right now, your potion regenerates 3 health per turn, over 3 turns. This potion regenerates 8 health per turn, over 3 turns.", "green")
    engPrint("Your second choice is a magical health potion. This potion regenerates 5 health per turn, over a duration of 5 turns.", "green")
    inp = engInp("Would you like to upgrade your potion to a large health potion, or the magical health potion?", "green").lower()
    while inp not in ["magical health potion", "large health potion"]:
      inp = engInp("Sorry, that isn't a valid selection. Would you like to upgrade your potion to a Large Health Potion, or the Magical Health Potion?", "green").lower()
    engPrint("Your potion has been upgraded successfully! In exchange, you have lost your gold coins.")
    if inp == ["magical health potion"]:
      healthregen = [8, 3]
    else:
      healthregen = [5, 5]
    inventory.remove("gold coins")
    upgradedPotion = True

def copperMines():
  global xcord, ycord, prevycord, prevxcord, turnContinue, inp, foughtThugs, health, maxhealth, healthregen, upgradedPotion, visitedCopperMines
  if trueMap[ycord][xcord] in ["Copper Mine"] and visitedCopperMines == False:
    inp = engInp("You are at the entrance to the Copper Mines. Would you like to enter the mine?", "red").lower()
    while True:
      if inp in ["yes", "y"]:
        inventory.append("copper ore")
        inp = engInp("You enter the Copper Mines. You use your pickaxe from the old man, and slowly chip away at some copper ore. After you have gotten a significant amount of copper, you are about to leave the mine, but you find some explosives nearby. Would you like to pick them up?", "red").lower()
        while True:
          if inp in ["yes", "y", "pick up explosives", "get explosives", "pick them up"]:
            engPrint("You have acquired the explosives! Try using them in combat sometime.")
            inventory.append("explosives")
            turnContinue = True
            visitedCopperMines = True
            break
          elif inp in ["no", "n"]:
            turnContinue = True
            engPrint("You don't pick up the explosives, and leave the mine.")
            visitedCopperMines = True
            break
          else:
            inp = engInp("That isn't a valid move. Please input a different decision.", "red").lower()
        break
      elif inp in ["no", "n", "leave"]:
        ycord, xcord = returnToPrev("You have successfully left the copper Mines.", prevycord, prevxcord, magicMap)
        break
      else:
        inp = engInp("That isn't a valid choice. Please input a different decision.", "red").lower()


# Beginning of game, character has just woken up.
engPrint("You awake in a chamber. Your hands are swollen, and you feel rough leather rags on your chest.") 
engPrint("There is a scrap of paper in your pocket.")

# Instructional Letter (Info + Tutorial)
inp = engInp("Would you like to read the paper?").lower()
if inp not in ["skip", "s"]:
  defAnswer(inp, ["y", "yes", "read"], ["n", "no"])
  introduction()
main()