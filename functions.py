# Imports
import time
from termcolor import colored


textspeed = 0.005
# -------------------Functions-------------------
# Stuttered Text Function
def engPrint(string, color="white", space=True, speed=textspeed): # Prints stuff, but with stuttered timing, so like undertale engine.
  for i in string:
    time.sleep(speed)
    print(colored(i, color), end="", flush=True)
  if space == True:
    print("\n")

print("hello worldd", end="\n")

def engInp(string, color="white", space=True, speed=textspeed): # Acts as input() but with stuttered text
  engPrint(string[0:len(string)-1], color, False, speed)
  inp = input(colored(string[len(string)-1] + "\n", color))
  if space == True:
    print("\n")
  return inp

def mapPrint(lst, xcord, ycord, color="white"): # Prints a map (aka a 2d array)
  largestlen = 0
  for i in range(len(lst)):
    for z in range(len(lst[i])):
      if z == xcord and i == ycord:
        lst[i][z] += " ★"
        if len(lst[i][z]) > largestlen:
          largestlen = len(lst[i][z])
        lst[i][z] = lst[i][z][0:len(lst[i][z])-2]
      elif len(lst[i][z]) > largestlen:
        largestlen = len(lst[i][z])

  engPrint("The Magical Map")
  for i in range(len(lst)):
    print("-+-" + ("-" * largestlen + "-+-") * len(lst[i]))
    print(" | " +(" " * (largestlen) + " | ") * len(lst[i]))
    for z in range(len(lst[i])):
      print(" | " + colored(lst[i][z], color), end="")
      if i == ycord and z == xcord:
        print(" ★", end="")
        print(" " * (largestlen - len(lst[i][z]) - 2), end="")
      else:
        print(" " * (largestlen - len(lst[i][z])), end="")
    print(" | ")
    print(" | " +(" " * (largestlen) + " | ") * len(lst[i]))
  #print("-" * (largestlen * len(i)) + "_" * (3*(len(i)+1)))
  print("-+-" + ("-" * largestlen + "-+-") * len(lst[i]))
  print("")

# Makes it so that the user must answer a certain answer, yes, or no
def defAnswer(inp, yesAnswers, noAnswers, noMessage = "Hmm... I have a bad feeling about that decision. Maybe try something different?", failMessage = "Sorry, I don't know what you mean. Please input another answer.", color = "white"):
  while True: 
    if isinstance(inp, str):
      if inp in yesAnswers:
        break
      if inp in noAnswers:
          inp = engInp(noMessage, color).lower()
          continue
    inp = engInp(failMessage, color).lower()

# Updates the map when there is a new location
def updateMap(xcord, ycord, magicMap, trueMap):
  try:
    if magicMap[ycord][xcord] != trueMap[ycord][xcord]:
      magicMap[ycord][xcord] = trueMap[ycord][xcord]
  except:
    print(ycord, xcord)
  return(magicMap)

# Moves the character (also calls the updateMap function)
def move(xcord, ycord, direction, magicMap, trueMap):
  msg = ""
  newxcord = xcord
  newycord = ycord
  if direction in ["e", "east"]:
    if xcord > len(trueMap[0]) - 2:
      msg = "Sorry, you have reached a dead-end. You cannot move in this direction."
    else:
      newxcord = xcord + 1
      msg = "You have successfully moved east."
  elif direction in ["w", "west"]:
    if xcord < 1:
      msg = "Sorry, you have reached a dead-end. You cannot move in this direction."
    else:
      newxcord = xcord - 1
      msg = "You have successfully moved west."
  elif direction in ["n", "north"]:
    if ycord < 1:
      msg = "Sorry, you have reached a dead-end. You cannot move in this direction."
    else:
      newycord = ycord - 1
      msg = "You have successfully moved north."
  elif direction in ["s", "south"]:
    if ycord > len(trueMap) - 2:
      return(xcord, ycord, "Sorry, you have reached a dead-end. You cannot move in this direction.")
    else:
      newycord = ycord + 1
      msg = "You have successfully moved south."
  return(newxcord, newycord, msg)
"""  if trueMap[newycord][newxcord] in ["Void"]:
      updateMap(newxcord, newycord, magicMap, trueMap)
      return(xcord, ycord, "You cannot move this way, because the location is nothing but void. The destruction seems like it is from a massive battle between two powerful forces. It's almost as if this part of the land has been erased from existance...\n\n")"""

# Returns character to previous position, and also prints a message if needed
def returnToPrev(msg, prevycord, prevxcord, map):
    if len(msg) != 0:
      engPrint(msg)
    engPrint("You have retreated to the " + map[prevycord][prevxcord])
    return(prevycord, prevxcord)