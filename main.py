#!/usr/bin/env python
# coding=utf-8

# SKYRIM 2: THE SCROLL IS NOT YOUNG
# Copyright (c) 2017 Jake Ledoux All Rights Reserved.

import os, time, sys, random, copy, json
from msvcrt import getch # Keypresses on Windows. Cross-platform later.

# Getting keypresses for menus
def getkey():
	key = ord(getch())
	if key in [9, 27]: #Tab, ESC
		return 'esc'
	elif key in [13, 101]: #E, Enter
		return 'enter'
	elif key == 32: # Spacebar
		return 'space'
	elif key == 102:
		return 'f'
	elif key == 113:
		return 'q'
	elif key == 115: # S
		return 'down'
	elif key == 119: # W
		return 'up'
	elif key == 224: #Special keys (arrows, f keys, ins, del, etc.)
		key = ord(getch())
		if key == 82: # Insert
			clear()
			print("Kaching!")
			char.bag = {'armor_bone' : 1, 'sword_bone' : 1, 'bow_bone' : 1, 'health_elixir' : 9999}
			char.gold = 99999999
			char.hp = [1000,1000]
			enter()
		elif key == 80: #Down arrow
			return 'down'
		elif key == 72: #Up arrow
			return 'up'

# Drawing menus
# menu_list = List of options, pre_text = String displayed before menu, post_text = String displayed after menu
def menu(menu_list, pre_text = None, post_text = None, special_f=False, special_q=False, menu_item=0):
	while True:
		menu_list2 = []
		clear()

		#Print pre_text
		if pre_text != None:
			print(pre_text+"\n")

		# Appending cursor to menu options
		for x in range(0, len(menu_list)):
			menu_list2 += " "
		for x in range(0, len(menu_list)):
			if menu_list[x] in ['Back','Quit','Run','Cancel']:
				menu_list2[x] += "\n "
			if x == menu_item:
				menu_list2[x] += " > "+menu_list[x]
			else:
				menu_list2[x] += "   "+menu_list[x]
			print(menu_list2[x])

		#Print post_text
		if post_text != None:
			print("\n"+post_text)

		# Get and handle keypresses
		key = getkey()
		if key == "esc":
			return "Back"
		elif key == "up":
			menu_item -= 1
		elif key == "down":
			menu_item += 1

		elif special_f and key == "f" and menu_list[menu_item].strip() not in ['Back','Quit','Run','Cancel']:
			return "special_f "+menu_list[menu_item].strip()
		elif special_q and key == "q" and menu_list[menu_item].strip() not in ['Back','Quit','Run','Cancel']:
			return "special_q "+menu_list[menu_item].strip()

		# Wrap bottom and top of menus
		if menu_item > len(menu_list)-1:
			menu_item = 0
		elif menu_item < 0:
			menu_item = len(menu_list)-1

		if key == "enter" :
			return menu_list[menu_item].strip() # Returns the string option selected

def save():
	with open("data/save.corn","w+") as f:
		f.write(json.dumps(char.quest_active)+"\n")
		f.write(json.dumps(char.hp)+"\n")
		f.write(json.dumps(char.xp)+"\n")
		f.write(json.dumps(char.lvl)+"\n")
		f.write(json.dumps(char.gold)+"\n")
		f.write(json.dumps(char.deathwish)+"\n")
		f.write(json.dumps(char.hand)+"\n")
		f.write(json.dumps(char.armor)+"\n")
		f.write(json.dumps(char.bag)+"\n")
		f.write(json.dumps(stats.time)+"\n")

def load():
	with open("data/db.corn","r") as f:
		state = None
		temp = f.read()
		for i in temp.split("\n"):
			if i == '':
				continue
			if '[WEAPONS]' in i:
				state = 'weapons'
			elif '[AID]' in i:
				state = 'aid'
			elif '[ARMOR]' in i:
				state = 'armor'
			else:
				if state == 'weapons':
					stats.values[i.split("\t")[2]] = int(i.split("\t")[0])
					stats.dmg[i.split("\t")[2]] = int(i.split("\t")[1])
					stats.names[i.split("\t")[2]] = i.split("\t")[3]
				elif state == 'aid':
					stats.values[i.split("\t")[2]] = int(i.split("\t")[0])
					stats.heal[i.split("\t")[2]] = int(i.split("\t")[1])
					stats.names[i.split("\t")[2]] = i.split("\t")[3]
				elif state == 'armor':
					stats.values[i.split("\t")[2]] = int(i.split("\t")[0])
					stats.dfc[i.split("\t")[2]] = int(i.split("\t")[1])
					stats.names[i.split("\t")[2]] = i.split("\t")[3]
	if os.path.isfile("data/save.corn"):
		with open("data/save.corn","r") as f:
			char.quest_active = json.loads(f.readline().strip())
			char.hp = json.loads(f.readline().strip())
			char.xp = json.loads(f.readline().strip())
			char.lvl = json.loads(f.readline().strip())
			char.gold = json.loads(f.readline().strip())
			char.deathwish = json.loads(f.readline().strip())
			char.hand = json.loads(f.readline().strip())
			char.armor = json.loads(f.readline().strip())
			char.bag = json.loads(f.readline().strip())
			stats.time = json.loads(f.readline().strip())

def dialogue(name, speech, menu_list = None):
	menu_item = 0
	while True:
		menu_list2 = []
		clear()
		message = speech
		# Character dialogue
		print("\n\t      "+name+":")
		suffix = ""
		for i in range(len(name)+1):
			suffix += "═"
		suffix += "═╧"
		for i in range(30-len(suffix)):
			suffix += "═"
		print('\t╔═══╧═'+suffix+'╗\n\t║                                   ║')
		wrapped_message = []
		while len(message) > 30:
			for i in range(30,-1,-1):
				if message[i] == " ":
					wrapped_message += [message[:i].strip()]
					message = message[i:]
					break
		wrapped_message += [message.strip()]
		for i in wrapped_message:
			suffix = ""
			for i2 in range(30-len(i)):
				suffix += " "
			suffix += "  ║"
			print("\t║   "+i+suffix)
		print('\t║                                   ║\n\t╚═══════════════════════════════════╝\n')

		if menu_list == None:
			print('\n')
			enter()
			return

		# Appending cursor to menu options
		for x in range(0, len(menu_list)):
			menu_list2 += " "
		for x in range(0, len(menu_list)):
			if menu_list[x] in ['Back','Quit','Run','Cancel']:
				menu_list2[x] += "\n "
			if x == menu_item:
				menu_list2[x] += "\t> "+menu_list[x]
			else:
				menu_list2[x] += "\t  "+menu_list[x]
			print(menu_list2[x])

		# Get and handle keypresses
		key = getkey()
		if key == "up":
			menu_item -= 1
		elif key == "down":
			menu_item += 1

		# Wrap bottom and top of menus
		if menu_item > len(menu_list)-1:
			menu_item = 0
		elif menu_item < 0:
			menu_item = len(menu_list)-1

		if key == "enter" :
			return menu_item

def clear():
	os.system("cls" if os.name == "nt" else "clear")

def get_name(item):
	return stats.names[item]

def get_item(name):
	return list(stats.names.keys())[list(stats.names.values()).index(name)]

def switch_weapon():
	menu_item = 0
	while True:
		weapons = []
		for i in char.bag:
			if i in stats.dmg:
				if i == char.hand:
					weapons += [get_name(i)+" [ACTIVE]"]
				else:
					weapons += [get_name(i)]
		weapons += ['Back']
		action = menu(weapons, "WEAPON SELECTION","E/Enter: Equip - F: Drop", special_f=True, menu_item=menu_item)
		if action not in ['Cancel','Back']:

			if "[ACTIVE]" in action:
				action = " ".join(action.split(" ")[:-1])

			if "special_f" in action:
				action = " ".join(action.split(" ")[1:])
				use_item(get_item(action))
				if char.hand not in char.bag:
					char.hand = "fists"
			else:
				char.hand = get_item(action)
			try:
				menu_item = weapons.index(action)
			except:
				menu_item = weapons.index(action+" [ACTIVE]")
		else:
			break

def switch_armor():
	menu_item = 0
	while True:
		armor = []
		for i in char.bag:
			if i in stats.dfc:
				if i in char.armor:
					armor += [get_name(i)+" [ACTIVE]"]
				else:
					armor += [get_name(i)]
		armor += ['Back']
		action = menu(armor, "CLOTHING SELECTION","E/Enter: Equip - F: Drop", special_f=True, menu_item=menu_item)
		if action not in ['Cancel','Back']:
			if "[ACTIVE]" in action:
				action = " ".join(action.split(" ")[:-1])

			if "special_f" in action:
				action = " ".join(action.split(" ")[1:])
				use_item(get_item(action))
				if char.armor not in char.bag:
					char.armor = "nothing"
			else:
				char.armor = get_item(action)
			try:
				menu_item = armor.index(action)
			except:
				menu_item = armor.index(action+" [ACTIVE]")
		else:
			break

def use_aid():
	menu_item = 0
	while True:
		items = []
		for i in char.bag:
			if i in stats.heal:
				items += [get_name(i)+": "+str(char.bag[i])]
		items += ['Back']
		action = menu(items, "ITEM SELECTION","E/Enter: Use - F: Drop", special_f=True, menu_item=menu_item)

		if action not in ['Back','Cancel']:
			if "special_f" in action:
				action = action[:action.index(":")]
				action = " ".join(action.split(" ")[1:])
				use_item(get_item(action))

			elif char.hp[0] == char.hp[1]:
				print("\nYou are already fully healed.")
				enter()
			else:
				action = action[:action.index(":")]
				char.hp[0] += stats.heal[get_item(action)]
				if char.hp[0] > char.hp[1]:
					char.hp[0] = char.hp[1]
				use_item(get_item(action))
				clear()
				print("\nYou use 1 "+action+" for a total of "+str(stats.heal[get_item(action)])+" healing points.")
				print("Current HP: "+str(char.hp[0])+"/"+str(char.hp[1]))
				if get_item(action) in char.bag:
					print("You now have "+str(char.bag[get_item(action)])+" remaing "+action+"s.")
				else:
					print("You have no remaing "+action+"s.")
				enter()
			for i in items:
				if " ".join(i.split(" ")[1:]) == action:
					menu_item = items.index(action)
					break
		else:
			break

def enter():
	print("Press enter.")
	key = None
	while key != 'enter':
		key = getkey()
	clear()

def use_item(item):
	if item not in ['fists','nothing']:
		char.bag[item] -= 1
		if char.bag[item] < 1:
			del char.bag[item]

def advance_time(minutes):
	stats.time[1] += minutes
	if stats.time[1] >= 60:
		stats.time[0] += stats.time[1]//60
		stats.time[1] = stats.time[1]%60
	if stats.time[0] > 23:
		stats.time[0] -= 24

def get_time():
	ampm = "PM"	if stats.time[0] > 11 else "AM"
	hour = stats.time[0]
	minute = str(stats.time[1])
	if hour == 0:
		hour = 12
	elif hour > 12:
		hour -= 12
	if len(minute) < 2:
		minute = "0"+minute
	return str(hour)+":"+minute+" "+ampm

def sign(object, message, alive=True):
	clear()
	if alive:
		print(object+":\n")
	else:
		print("The "+object+" reads:\n")
	wrapped_message = []
	while len(message) > 30:
		for i in range(30,-1,-1):
			if message[i] == " ":
				wrapped_message += [message[:i].strip()]
				message = message[i:]
				break
	wrapped_message += [message.strip()]
	for i in wrapped_message:
		print("\t"+i)
	print()
	enter()

def combat(enemy, run=True, safe=False):
	scene_active = True
	while scene_active:
		action = menu(['Attack','Use Item','Switch Weapon','Run'],"Enemy: "+enemy['name']+"\nEnemy HP: "+str(enemy['hp'][0])+"/"+str(enemy['hp'][1]), "HP: "+str(char.hp[0])+'/'+str(char.hp[1]))
		advance_time(random.randint(10,30))
		if action == "Attack":
			attack = int(round((stats.dmg[char.hand] * 1-(enemy['dfc']/100))))
			clear()
			if random.randrange(10) == 9:
				print("Critical attack! x3 damage!")
				attack *= 3
			enemy['hp'][0] -= attack
			print("You attack and deal "+str(attack)+" damage.")
			enter()
			if enemy['hp'][0] < 1:
				clear()
				suffix = " is killed." if safe == False else " is defeated."
				print("The attacking "+enemy['name']+suffix)
				xp_earned = int(round(5*enemy['hp'][1]))
				gold_earned = int(round(enemy['hp'][1]*((random.randrange(100)+50)/100)))
				char.xp += xp_earned
				char.gold += gold_earned
				print("You gain:")
				print("\t"+str(xp_earned)+" XP.")
				print("\t"+str(gold_earned)+" gold.")
				enter()
				if char.xp >= 1000:
					char.xp -= 1000
					char.lvl += 1
					char.hp[1] += 10
					char.hp[0] = char.hp[1]
					print("You've leveled up! You are now level "+str(char.lvl)+".")
					enter()
				scene_active = False
				return True

		elif action == 'Switch Weapon':
			switch_weapon()

		elif action == 'Use Item':
			use_aid()

		elif action == 'Run' or 'Back':
			if run:
				clear()
				escape = random.randrange(2)
				if escape == 0:
					print("You manage to run away safely.")
					enter()
				else:
					attack = int(round(((enemy['dmg']*(1-(random.randrange(10)/20)))*(1-(stats.dfc[char.armor]/100)))/2))
					char.hp[0] -= attack
					print("You run away, but not before suffering "+str(attack)+" damage.")
					enter()
					if char.hp[0] <= 0:
						die()
						scene_active = False
						return False
				scene_active = False
				return True
			else:
				dialogue(enemy['name'],"Where do you think you're going?")

		attack = int(round((enemy['dmg']*(1-(random.randrange(10)/20)))*(1-(stats.dfc[char.armor]/100))))
		char.hp[0] -= attack
		clear()
		print("Enemy attacks. You suffer "+str(attack)+" damage.")
		enter()
		if char.hp[0] <= 0:
			die()
			scene_active = False
			return False

def die():
	clear()
	print("YOU DIED.")
	print("You have lost your items and 100 gold has been deducted from you stash.")
	char.bag = copy.deepcopy(char.default_bag)
	char.hp[0] = char.hp[1]
	char.gold -= 100
	char.deathwish = False
	if char.gold < 0:
		char.gold = 0
	hand = "fist"
	armor = "rags"
	enter()

def reward(amount, name=None, silent=False):
	if not silent:
		clear()
		if name == None:
			print("You have been rewarded "+str(amount)+" gold!")
		else:
			print(name+" has rewarded you "+str(amount)+" gold!")
		enter()
	char.gold += amount

def reward_item(giftid,amount=1,name=None, silent=False):
	if not silent:
		clear()
		if name == None:
			print("You have been given ["+get_name(giftid)+"] x"+str(amount)+".")
		else:
			print(name+" has given you ["+get_name(giftid)+"] x"+str(amount)+".")
		enter()
	if giftid in char.bag:
		char.bag[giftid] += amount
	else:
		char.bag[giftid] = amount

# All the character's data
class char:
	quest_active = 0
	hp = [100, 100] # [CURRENT HP, MAX HP]
	xp = 0
	lvl = 0
	gold = 0
	deathwish = False
	hand = "fists"
	armor = "rags"
	bag = {'fists' : 1, "rags" : 1, "nothing" : 1} # The Player's inventory. {"potions" : 2, "sword_iron" : 1}
	default_bag = {'fists' : 1, "rags" : 1, "nothing" : 1}

# Catch-all class where I put non-character related data
class stats:
	dmg = {'fists' : 2, 'sword_iron': 6} # The damage stats of each weapon
	heal = {'potion' : 20, 'sweet_roll' : 2}
	dfc = {'rags' : 1, 'nothing' : 0} # Effectiveness of armor from 0 to 100
	names = {}
	values = {}
	enemies = [ # Database of enemies and their stats
			{'name' : 'Bear', 'hp' : [20,20], 'dmg' : 30, 'dfc' : 5},
			{'name' : 'Tree Monkey', 'hp' : [3,3], 'dmg' : 5, 'dfc' : 0},
			{'name' : 'Wanderer', 'hp' : [10,10], 'dmg' : 20, 'dfc' : 30}
	]
	time = [7,0] # Hours, Minutes
	shopbag = {}

# LOAD GAME
load()

# INTRO
if '-nointro' not in sys.argv: # Check if the script was run with -nointro
	clear()
	print("Bethesda Softworks presents...")
	time.sleep(3)
	print("\n\nSKYRIM 2: THE SCROLL IS NOT YOUNG")
	time.sleep(2)
	enter()

# GAME LOOP
menu_item = 0
while True:
	# Scene selection
	scenes = ['Shop','Wilderness','Quest','Inventory','Quit']
	scene = menu(scenes, 'Gold: '+str(char.gold)+'\nHP: '+str(char.hp[0])+'/'+str(char.hp[1])+'\nXP: '+str(char.xp)+'/1000\nLevel: '+str(char.lvl),
	get_time(), menu_item=menu_item)

	scene_active = True # When this is false, the loop returns to the main menu

	# Buy and sell items
	if scene == "Shop":
		stats.shopbag = {}
		for i in list(stats.names.keys()):
			stats.shopbag[i] = 100
		menu_item = 0
		while scene_active:
			if stats.time[0] < 8 or stats.time[0] > 21:
				clear()
				sign("sign on the door","SHOP IS CLOSED. OUR HOURS ARE 8 AM TO 9 PM EXCEPT ON HOLIDAYS. FREE WIFI INSIDE.", False)
				advance_time(5)
				scene_active = False
				continue
			action = menu(['Buy','Sell','Back'], 'SHOP', menu_item=menu_item)
			if action == "Back":
				scene_active = False
			elif action == "Buy":
				menu_item = 0
				while True:
					advance_time(random.randint(8,15))
					items = []
					for i in stats.shopbag:
						items += [get_name(i)+" (Amount: "+str(stats.shopbag[i])+" / Value: "+str(stats.values[i])+")"]
					items += ['Back']
					action = menu(items, "SHOP: BUY\n\nShopkeeper's Gold: INFINITE\nYour Gold: "+str(char.gold),"E/Enter: Buy", menu_item=menu_item)
					if action not in ['Cancel','Back']:
						action = action[:action.index("(")].strip()
						if char.gold >= stats.values[get_item(action)]:
							stats.shopbag[get_item(action)] -= 1
							if stats.shopbag[get_item(action)] < 1:
								del stats.shopbag[get_item(action)]
							try:
								char.bag[get_item(action)] += 1
							except:
								char.bag[get_item(action)] = 1
							char.gold -= stats.values[get_item(action)]
						else:
							print("\nNot enough money!")
							enter()
						for i in items:
							try:
								if i[:i.index("(")].strip() == action:
									menu_item = items.index(i)
									break
							except:
								if i == action:
									menu_item = items.index(i)
									break
					else:
						menu_item = 0
						break
			elif action == "Sell":
				menu_item = 0
				while True:
					advance_time(random.randint(8,15))
					items = []
					for i in char.bag:
						if i not in ['nothing','fists']:
							if i in [char.hand,char.armor]:
								items += [get_name(i)+" [ACTIVE]"+" (Amount: "+str(char.bag[i])+" / Value: "+str(int(round(stats.values[i]*.7)))+")"]
							else:
								items += [get_name(i)+" (Amount: "+str(char.bag[i])+" / Value: "+str(int(round(stats.values[i]*.7)))+")"]
					items += ['Back']
					action = menu(items, "SHOP: SELL\n\nShopkeeper's Gold: INFINITE\nYour Gold: "+str(char.gold),"E/Enter: Sell - F: Drop", special_f=True, menu_item=menu_item)
					if action not in ['Cancel','Back']:
						try:
							action = action[:action.index("[")].strip()
							print(action)
						except:
							action = action[:action.index("(")].strip()
						if "special_f" in action:
							action = " ".join(action.split(" ")[1:])
							use_item(get_item(action))
							if char.hand not in char.bag:
								char.hand = "fists"
							if char.armor not in char.bag:
								char.armor = "nothing"
						else:
							use_item(get_item(action))
							if char.hand not in char.bag:
								char.hand = "fists"
							if char.armor not in char.bag:
								char.armor = "nothing"
							char.gold += int(round(stats.values[get_item(action)]*.7))
						try:
							stats.shopbag[get_item(action)] += 1
						except:
							stats.shopbag[get_item(action)] = 1
						for i in items:
							try:
								if i[:i.index("(")].strip() == action:
									menu_item = items.index(i)
									break
							except:
								if i == action:
									menu_item = items.index(i)
									break
					else:
						menu_item = 1
						break

	# Fight random enemies
	elif scene == "Wilderness":
		if char.quest_active == 2.5:
			clear()
			print("You enter the wilderness looking for the King's lost goose...")
			enter()
			print("As you continue forward, you spot a sign down the path.")
			enter()
			sign("sign on the tree","WE HAVE YOUR DUMB GOOSE. CATCH US IF YOU CAN.",False)
			print("You sprint down the path...")
			enter()
			dialogue("?","Hey, you!")
			print("You turn around and see a young punk emerge from the bushes.")
			enter()
			dialogue("Punk","That's right, I'm talking to you. You want your goose? You're going to have to get through me!")
			if not combat({'name' : 'Punk', 'hp' : [10,10], 'dmg' : 1, 'dfc' : 0},False,True):
				continue
			dialogue("Punk","No fair!")
			print("A tall Nord walks out of the bushes.")
			enter()
			dialogue("Tall Nord","I see you've defeated my young apprentice, but you're not gonna get through me!")
			dialogue("Tall Nord","POWER OF THE SUN, FLOW THROUGH ME!!!")
			if not combat({'name' : 'Tall Nord', 'hp' : [30,30], 'dmg' : 8, 'dfc' : 20},False,True):
				continue
			dialogue("Tall Nord","I- I\'ve been defeated in combat. How can this be?",
			["You did alright.","You suck and so does your apprentice.","Can I have the goose now?","Give me the goose or taste my blade."])
			clear()
			print("The tall Nord puts two fingers in his mouth and whistles loudly.")
			enter()
			print("A large, fat bear with makeshift armor comes stumbling out of the bushes.")
			enter()
			dialogue("Tall Nord","Roller, attack!")
			if not combat({'name' : 'Roller the Bear', 'hp' : [50,50], 'dmg' : 30, 'dfc' : 30},False):
				continue
			dialogue("Tall Nord","Roller, NOOOO!")
			dialogue("Roller the Bear","*roars in defeat*")
			clear()
			print("The bear rolls over dead.")
			enter()
			action = dialogue("Tall Nord","Fine... take the goose. It's just ahead, straight down the path. Just... please don't kill us.",
			['Fine. Just this once.','Run.','Request denied.','*mimic the lightsaber ignition sound with your mouth*'])
			clear()
			if action in [0,1]:
				dialogue("Tall Nord","Thank you! Thank you!")
				print('The Nord and punk scurry off into the bushes.')
				enter()
			else:
				print("You swiftly behead both the Nord and the punk.")
				enter()
			print("After a few minutes of walking down the path, you come across the King's goose.")
			enter()
			dialogue("Goose","HONK")
			print("You grab the goose. It honks and struggles, but you manage to stuff it in your bag.")
			reward_item("king_goose",silent=True)
			enter()
			char.quest_active = 3
		else:
			combat(copy.deepcopy(stats.enemies[random.randrange(len(stats.enemies))]))

	elif scene == 'Quest':
		advance_time(30)
		if char.quest_active == -1:
			clear()
			print("There are no more quests. Nice job...")
			enter()

		if char.quest_active == 0:
			action = dialogue("The King","Hm. Go get me a sweetroll, my boy! Here's 1 gold, it should suffice.",
			['Yes sir.','With haste, my liege.','Why? Haven\'t you had enough sweets already?','Buzz off, old man.'])
			if action in [0,1]:
				dialogue("The King","God speed!")
				reward(1, silent=True)
				char.quest_active = 1
				continue
			elif action in [2]:
				dialogue("The King","Get out of my sight.")
			elif action == 3:
				dialogue("The King","Not yet learned learned your place, have you? I can fix that.")
				char.deathwish = True

		if char.quest_active == 1:
			action = dialogue("The King","Oh, I see you've returned! Have you brought my long-awaited snack?",
			['Yes, here it is.','No, not yet.','What did you want again?','I don\'t want to get it for you anymore.'])

			if action == 0:
				if "sweet_roll" in char.bag:
					dialogue("The King","Yes! Give it, quick!")
					use_item('sweet_roll')
					dialogue("The King","Mmmm! Oh yes! So delicious. -Oh right, your reward. Take this for a job well done!")
					reward(200,"The King")
					dialogue("The King","I look forward to using your services again soon.")
					char.quest_active = 2
				else:
					dialogue("The King","Untrue! Why do you tease me so?")
			elif action == 1:
				dialogue("The King","Oh please hurry!")
			elif action == 2:
				dialogue("The King","A sweetroll. With haste!")
			elif action == 3:
				dialogue("The King","Very well. I shall find someone else to do my bidding.")
				char.quest_active = 0

		elif char.quest_active == 2:
			action = dialogue("The King","Ah! My loyal squire has returned. Just in time, too! I have another task for you.",
			['What is it?','Get on with it.','Not now, can\'t you see I\'m busy?','I\'m done being your errand boy.'])
			if action in [0,1]:
				action = dialogue("The King","My beloved goose has run off into the wilderness. Can you please find him and bring him back?",
				['Consider it done.','Do you think I can make it in time?','I\'m not sure I can do this, it\'s dangerous in there.', 'Your goose is dead.'])
				char.quest_active = 2.5
				if action == 0:
					dialogue("The King","Your loyalty will not go unnoticed. Best of luck to you!")
					continue
				elif action == 1:
					dialogue("The King","Not if we continue discussing it! Be on your way!")
					continue
				elif action == 2:
					dialogue("The King","I see... hm, well take these. They may help you on your journey.")
					reward_item("health_draught",2,"The King")
					continue
				elif action == 3:
					action = dialogue("The King","You shut your dirty mouth! Get to work at once!",
					['Sorry, sir. It will be done.','Fine.','Not gonna happen.','Your goose is dead.'])
					if action in [0,1]:
						dialogue("The King","Good. Now be on your way!")
						continue
					else:
						dialogue("The King","Not yet learned learned your place, have you? I can fix that.")
						char.deathwish = True


			elif action == 2:
				dialogue("The King","I will grant you a break. Though, be mindful lest you forget your place.")
			elif action == 3:
				dialogue("The King","Not yet learned learned your place, have you? I can fix that.")
				char.deathwish = True

		elif char.quest_active == 2.5:
			dialogue("The King","Please, do not return until you've found my goose!")
		elif char.quest_active == 3:
			dialogue("The King","Ah, you've returned! With my goose, I hope.")
			if "king_goose" not in char.bag:
				action = dialogue("But, I don't see him in your bag. Why is that?",
				["He's in there somewhere.","Maybe he got out.","He was worthless anyway.","It was just a dumb goose."])
				if action in [0,1]:
					if "king_goose" in stats.shopbag:
						dialogue("The King","Liar! You sold my goose to the local shopkeeper!")
					else:
						dialogue("The King","Oh... oh no. No-no-no. Did you... eat... my beloved goose?",
						['Someone stole him from me!','No! He must have run off somewhere.','Guilty.','And he tasted delicious.'])
				dialogue("The King","You will pay for your crimes!")
				char.deathwish = True
			else:
				clear()
				print("The goose jumps out of your bag and onto the King's lap.")
				dialogue("The King","Can it be? My beloved goose has been returned to me!")
				action = dialogue("The King","How can I ever repay you?",
				["No need, sir.","You happiness is enough for me.","Gold will do.","The crown."])
				if action in [0,1]:
					dialogue("The King","Ha! You are too much. Here, take this. I insist.")
					reward(500, "The King")
				elif action == 2:
					dialogue("The King","Hm. Well, at least you're honest.")
					reward(200, "The King")
				elif action ==3:
					dialogue("The King","Soon perhaps. But that conversation is for another day. In the meantime, take this.")
					reward(200, "The King")
				char.quest_active = -1

		if char.deathwish:
			dialogue("The King","Guards! Arrest this man!")
			if not combat({'name' : 'Royal Guard', 'hp' : [20,20], 'dmg' : 20, 'dfc' : 50}, False):
				char.deathwish = False
				continue
			dialogue("Royal Guard Commander","Brother! He's...dead... YOU'LL PAY FOR THIS!!!")
			if not combat({'name' : 'Royal Guard Commander', 'hp' : [30,30], 'dmg' : 30, 'dfc' : 50}, False):
				char.deathwish = False
				continue
			action = dialogue("The King","You've defeated my elite guards? This can't be! Please, spare me, and I'll let you take the throne.",
			['Sounds like a deal.','No, I\'m not fit for kingship.','That\'s what I thought. Now get out of my sight, slime.','You\'re not getting out of this one THAT easy.'])
			if action in [0,2]:
				dialogue("Ruler formerly known as King","As you wish, sire.")
				char.quest_active = -1
				char.deathwish = False
			elif action == 1:
				dialogue("The King","You're an honorable man. I can dig that. Please, take this as a token of my gratitude.")
				reward(500, "The King")
				char.quest_active = 2
				char.deathwish = False
			elif action == 3:
				dialogue("The King","So be it!")
				if combat({'name' : 'The King', 'hp' : [30,30], 'dmg' : 50, 'dfc' : 50}, False):
					char.quest_active = -1
				char.deathwish = False

	elif scene == 'Inventory':
		while scene_active:
			action = menu(['Weapons','Clothing','Aid','Back'],'INVENTORY')
			if action == 'Weapons':
				switch_weapon()
			elif action == 'Clothing':
				switch_armor()
			elif action == 'Aid':
				use_aid()
			elif action == 'Back':
				scene_active = False
	# ):
	elif scene in ['Quit','Back']:
		save()
		clear()
		print("Thanks for playing!")
		sys.exit()

	menu_item = scenes.index(scene)