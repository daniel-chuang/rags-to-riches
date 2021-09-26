# Imports
from functions import engPrint, engInp, mapPrint, defAnswer, move, updateMap, returnToPrev
import time
import random
currenthealthregen = [0, 0]

# Functions for Battle
def battleCalc(health, healthregen, attack, enemyname, enemyhealth, enemyattack, enemyitems, inventory, inp, firstturn = False, status = "", color="red"):
  global potionused, escape, maxhealth, currenthealthregen
  if inp in ["a", "attack", "attack enemy", "attack " + enemyname, "a " + enemyname]:
    if random.randint(0, 10) < 3:
      engPrint("You have critically striked for %s damage!" % str(2*attack), "red")
      enemyhealth -= 2 * attack
    elif random.randint(0, 10) == 9:
      engPrint("You have missed the enemy with your attack!", "red")
    else:
      enemyhealth -= attack
      engPrint("You have attacked successfully for %s damage." % (attack), "red")
  elif inp in ["i", "inventory", "check inventory", "check i", "open i", "open inventory"]:
    engPrint("Your inventory: " + str(inventory), "red")
    return health, healthregen, attack, enemyhealth, enemyattack
  elif inp == "potion" and potionused == False and "potion" in inventory:
    currenthealthregen = [healthregen[0], healthregen[1]]
    potionused = True
  elif inp in ["run", "escape", "e", "run away", "escape from " + enemyname]:
    if random.randint(1, 1000) >= 1000 * (enemyhealth/enemymaxhealth):
      engPrint("You failed to escape...")
    else:
      engPrint("You escaped successfully!")
      escape = True
      return health, healthregen, attack, enemyhealth, enemyattack
  elif firstturn != True:
    engPrint("Sorry, that was an invalid move... You can either 'attack', check what you have in your 'inventory', use an item in your inventory by typing its name (e.g \"potion\"), or 'escape.'", "red")
    return health, healthregen, attack, enemyhealth, enemyattack
  if firstturn == False:
    health -= enemyattack
  engPrint("Your health: %s                     Enemy health: %s" % (str(health), str(enemyhealth)), color)
  if health < 1:
    engPrint("You have died in combat to %s." % (enemyname), "red")
    time.sleep(1)
    quit()
  if currenthealthregen[1] != 0:
    health += currenthealthregen[0]
    if currenthealthregen[1] == 1:
      engPrint("You have regenerated %s health. You are now at %s health! The effect of your health potion has run out." % (currenthealthregen[0], health), "red")
    else:
      engPrint("You have regenerated %s health. You are now at %s health!" % (currenthealthregen[0], health), "red")
    currenthealthregen[1] -= 1
  return health, healthregen, attack, enemyhealth, enemyattack

# First battle against Gremlin
def battleTutorial(health, healthregen, attack, enemyname, enemyhealth, enemyattack, enemyitems, inventory):
  global potionused, currenthealthregen
  maxhealth = health
  potionused = False
  enemyhealth, enemyattack, enemyitems = 40, 4, []
  health, healthregen, attack, enemyhealth, enemyattack = battleCalc(health, healthregen, attack, enemyname, enemyhealth, enemyattack, enemyitems, inventory, "", True)
  inp = engInp('You are currently engaged in combat with %s! You can attack the enemy with "a", or "attack". Try it out!' % (enemyname), "red").lower()
  defAnswer(inp, ["a", "attack", "attack enemy", "attack " + enemyname, "a " + enemyname], [], failMessage = 'Attack your enemy with "a" or "attack"!', color = "red")
  health, healthregen, attack, enemyhealth, enemyattack = battleCalc(health, healthregen, attack, enemyname, enemyhealth, enemyattack, enemyitems, inventory, "a")
  inp = engInp('You successfully attacked! It looks like %s attacked you back, and you lost some health as well. Check your inventory, I\'ll provide you with a magical health potion. Use it to regenerate health over 3 turns. Be careful though, you can only use it once a battle. You can use your items during battle by first typing "i" or "inventory", and then the item you would like to use.' % (enemyname), "red").lower()
  defAnswer(inp, ["i", "inventory", "check inventory", "check i", "open i", "open inventory"], [], failMessage = 'Open your inventory with "i" or "inventory"!', color = "red")
  inventory.append("potion")
  engPrint("You have acquired an infinite potion of healing!", "red")
  engPrint("Your inventory: " + str(inventory), "red")
  defAnswer(inp, ["potion"], [], failMessage = 'Use a potion to regenerate your health back! (reminder, you can use an item by typing the name of the item)', color = "red")
  health, healthregen, attack, enemyhealth, enemyattack = battleCalc(health, healthregen, attack, enemyname, enemyhealth, enemyattack, enemyitems, inventory, "potion")
  while enemyhealth > 0:
    inp = engInp("Keep attacking the enemy!", "red").lower()
    defAnswer(inp, ["a", "attack", "attack enemy", "attack " + enemyname, "a " + enemyname], [], failMessage = 'Keep attacking the enemy!', color = "red")
    health, healthregen, attack, enemyhealth, enemyattack = battleCalc(health, healthregen, attack, enemyname, enemyhealth, enemyattack, enemyitems, inventory, "a")
  inp = engInp('You slide under your enemy\'s legs, get up, and stab them swiftly in their back. With a groan, they fall to the ground and perish. However, another enemy is approaching! Fortunately, you can run from the battle with "e", or "escape". The chance you have of escaping lowers for each time you attack the enemy.', "red").lower()
  defAnswer(inp, ["run", "escape", "e", "run away", "escape from " + enemyname], [], failMessage = 'Quick! Run away with "e" or "escape"!', color = "red")
  engPrint("You have escaped successfully.", "red")
  engPrint("Your wounds are closing rather quickly... You have restored your health back to %s. Due to your fast healing body, your health will recover completely after every battle." % (maxhealth), "red")

# Battle against clubs at the Looted Camps
def battleLootedCamp(health, healthregen, attack, enemyname, enemyhealth, enemyattack, enemyitems, inventory):
  global potionused, escape, enemymaxhealth, currenthealthregen
  potionused, escape = False, False
  currenthealthregen = [0, 0]
  enemyhealth, enemymaxhealth, enemyattack, enemyitems = 20, 20, 5, []
  health, healthregen, attack, enemyhealth, enemyattack = battleCalc(health, healthregen, attack, enemyname, enemyhealth, enemyattack, enemyitems, inventory, "", True)
  engPrint('You are currently engaged in combat with a %s!' % (enemyname), "red")
  while enemyhealth > 0:
    inp = engInp("What will you do?", "red").lower()
    health, healthregen, attack, enemyhealth, enemyattack = battleCalc(health, healthregen, attack, enemyname, enemyhealth, enemyattack, enemyitems, inventory, inp)
    if escape == True:
      break
  if escape == False:    
    engPrint("The Thug looks exhausted from the battle. You seize this opportunity to swifly slice him in half, and his remnants collapse to the ground.", "red")
  else:
    return False # Also returning so that the main loop knows if you defeated the enemy or not
  enemyname = "Leader of the Thugs"
  engPrint('\n\nYou are now in combat with the %s!' % (enemyname), "red")
  enemyhealth, enemymaxhealth, enemyattack, enemyitems = 40, 40, 5, []
  health, healthregen, attack, enemyhealth, enemyattack = battleCalc(health, healthregen, attack, enemyname, enemyhealth, enemyattack, enemyitems, inventory, "", True)
  while enemyhealth > 0:
    inp = engInp("What will you do?", "red").lower()
    health, healthregen, attack, enemyhealth, enemyattack = battleCalc(health, healthregen, attack, enemyname, enemyhealth, enemyattack, enemyitems, inventory, inp)
    if escape == True:
      break
  if escape == False:    
    engPrint('The Leader of the Thugs wearily drops to the ground, defeated. As he dies, you pick up his leather armor, which is brand new (other than the wounds you just made on them). You have also acquired a couple gold coins from inside a pocket of his.', "red")
    return True # Returning so that the main loop knows if you defeated the enemy or not
  else:
    return False # Also returning so that the main loop knows if you defeated the enemy or not

# Battle against the knights
def battleKnights(health, healthregen, attack, enemyname, enemyhealth, enemyattack, enemyitems, inventory):
  global potionused, escape, enemymaxhealth
  potionused, escape = False, False
  enemyhealth, enemymaxhealth, enemyattack, enemyitems = 40, 40, 7, []
  health, healthregen, attack, enemyhealth, enemyattack = battleCalc(health, healthregen, attack, enemyname, enemyhealth, enemyattack, enemyitems, inventory, "", True)
  for i in range(2):
    enemyname = "Knight"
    enemyhealth, enemymaxhealth, enemyattack, enemyitems = 40, 40, 7, []
    engPrint('You are currently engaged in combat with a %s!' % (enemyname), "red")
    while enemyhealth > 0:
      inp = engInp("What will you do?", "red").lower()
      health, healthregen, attack, enemyhealth, enemyattack = battleCalc(health, healthregen, attack, enemyname, enemyhealth, enemyattack, enemyitems, inventory, inp)
      if escape == True:
        break
    if escape == False:    
      engPrint("You spot a creak in the Knight's chestplate. You swiftly insert your sword into the fracture, fatally piercing his heart.", "red")
    else:
      return False # Also returning so that the main loop knows if you defeated the enemy or not
  enemyname = "Knight Jones, Leader of the Silver Knights"
  engPrint('\n\nYou are now in combat with %s!' % (enemyname), "red")
  enemyhealth, enemymaxhealth, enemyattack, enemyitems = 55, 55, 9, []
  health, healthregen, attack, enemyhealth, enemyattack = battleCalc(health, healthregen, attack, enemyname, enemyhealth, enemyattack, enemyitems, inventory, "", True)
  while enemyhealth > 0:
    inp = engInp("What will you do?", "red").lower()
    health, healthregen, attack, enemyhealth, enemyattack = battleCalc(health, healthregen, attack, enemyname, enemyhealth, enemyattack, enemyitems, inventory, inp)
    if escape == True:
      break
  if escape == False:    
    engPrint('Knight Jones, Leader of the Silver Knights, adknowledges that he is about to be defeated by you. Out of sheer pride, he takes his sword and cuts his head off, as he would rather die before losing to someone who isn\'t a knight.', "red")
    engPrint('This is perfect for you! Since he decided to cut his head off, his armor is still in good condition. You successfully take it from his corpse and equip it.' , "red")
    return True # Returning so that the main loop knows if you defeated the enemy or not
  else:
    return False # Also returning so that the main loop knows if you defeated the enemy or not