#!/usr/bin/env python3.6.1
# coding=utf-8

# SKYRIM 2: THE SCROLL IS NOT YOUNG
# Copyright (c) 2017 Jake Ledoux All Rights Reserved.

import sys

if '-?' in sys.argv or '-help' in sys.argv:
	print("\nSkyrim 2 Launch Arguments:\n\n\t"+
	"-nointro (Disable intro)\n\t"
	"-nosave (Disable autosave)\n\t"
	"-noload (Bypass existing saved game)\n\t"
	"-? or -help (Returns this screen)\n"
	)
	sys.exit()

import os, time, random, copy, json, time
from msvcrt import getch # Keypresses on Windows. Cross-platform later.
from colorama import init, Fore, Back, Style
from data import termsize, art

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
			print_message("Kaching!")
			char.bag = {'armor_bone' : 1, 'sword_bone' : 1, 'bow_bone' : 1, 'health_elixir' : 9999}
			char.arrows = 1
			char.gold = 99999999
			char.hp = [1000,1000]
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
		f.write(json.dumps(char.arrows)+"\n")

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
	if os.path.isfile("data/save.corn") and "-noload" not in sys.argv:
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
			char.arrows = json.loads(f.readline().strip())

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
				menu_list2[x] += "\t"+Back.WHITE+Fore.BLACK+menu_list[x]
			else:
				menu_list2[x] += "\t"+menu_list[x]
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
		action = menu(weapons, Style.BRIGHT+"WEAPON SELECTION"+Style.RESET_ALL+"\n\nArrows: "+str(char.arrows),"E/Enter: Equip - F: Drop", special_f=True, menu_item=menu_item)
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
				print("\n"+Style.BRIGHT+Back.RED+"You are already fully healed.")
				enter()
			else:
				action = action[:action.index(":")]
				char.hp[0] += stats.heal[get_item(action)]
				if char.hp[0] > char.hp[1]:
					char.hp[0] = char.hp[1]
				use_item(get_item(action))
				clear()
				print("\nYou use 1 "+action+" for a total of "+str(stats.heal[get_item(action)])+" healing points.")
				print("Current HP: "+get_hp())
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

def enter(silent=False):
	if not silent:
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

def print_message(intext):
	clear()
	prefix = ""
	for i in range(int(round(termsize.getTerminalSize()[1]/2))-1):
		prefix += "\n"
	for i in range(int(round((termsize.getTerminalSize()[0]-len(intext))/2))):
		prefix += " "
	print(prefix+intext)
	prefix2 = "\n"
	for i in range(int(round(termsize.getTerminalSize()[0]/2))-5):
		prefix2 += " "
	print(prefix2,end="")
	enter()

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
	print("\t"+Fore.BLACK+Back.WHITE+"╔═══════════════════════════════════╗\n"+
		  "\t║                                   ║")
	for i in wrapped_message:
		suffix = ""
		for i2 in range(30-len(i)):
			suffix += " "
		suffix += "  ║"
		print("\t"+Fore.BLACK+Back.WHITE+"║   "+i+suffix)
	print('\t'+Fore.BLACK+Back.WHITE+'║                                   ║\n\t╚═══════════════════════════════════╝\n')
	print()
	enter()

def combat(enemy, run=True, safe=False, speak="Where do you think you're going?"):
	scene_active = True
	enemy['name'] = Style.BRIGHT+enemy['name']+Style.RESET_ALL
	while scene_active:
		action = menu(['Attack','Use Item','Switch Weapon','Run'],"Enemy: "+enemy['name']+"\nEnemy HP: "+get_hp(enemy), "HP: "+get_hp())
		advance_time(random.randint(10,30))
		critical_attack = False
		if action == "Attack":
			if "bow" in char.hand and char.arrows > 1:
				critial_okay = True
			elif "bow" not in char.hand:
				crit_okay = True
			else:
				crit_okay = False
			if random.randrange(10) and crit_okay:
				print_message(Style.BRIGHT+Fore.CYAN+"Critical attack! x3 damage!")
				critical_attack = True
			if enemy['can_block'] and "bow" not in char.hand:
				action = menu(hml,"Where do you aim?")
				hit = hml.index(action) == random.randint(0,2)
				if critical_attack:
					hit = True
				if hit:
					print_message("Clean hit!")
				else:
					print_message("The enemy blocks your attack!")
					hit = False
			elif "bow" in char.hand:
				if char.arrows > 0:
					print_message("You fire your bow...")
					bow_aim = random.randint(1,4)
					if bow_aim <= enemy['size'] or critical_attack:
						hit = True
						print_message("...and hit the "+Style.BRIGHT+enemy['name']+"!")
					else:
						hit = False
						print_message("...and miss.")
				else:
					hit = False
					print_message("You're out of arrows!")

			if hit:
				attack = int(round((stats.dmg[char.hand] * 1-(enemy['dfc']/100))))
				clear()
				if critical_attack:
					attack *= 3
				enemy['hp'][0] -= attack
				print_message("You deal "+Style.BRIGHT+Fore.RED+str(attack)+" damage.")
			if enemy['hp'][0] < 1:
				clear()
				suffix = " is killed." if safe == False else " is defeated."
				print("The attacking "+enemy['name']+suffix)
				xp_earned = int(round(5*enemy['hp'][1]))
				gold_earned = int(round(enemy['hp'][1]*((random.randrange(100)+50)/100)))
				char.xp += xp_earned
				char.gold += gold_earned
				print("\n  You gain:")
				print("\t  "+Style.BRIGHT+str(xp_earned)+Style.RESET_ALL+" XP.")
				print("\t  "+Fore.YELLOW+str(gold_earned)+Style.RESET_ALL+" gold.\n")
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
					print_message("You manage to run away safely.")
				else:
					attack = int(round(((enemy['dmg']*(1-(random.randrange(10)/20)))*(1-(stats.dfc[char.armor]/100)))/2))
					char.hp[0] -= attack
					print_message("You run away, but not before suffering "+Style.BRIGHT+Fore.RED+str(attack)+" damage.")
					if char.hp[0] <= 0:
						die()
						scene_active = False
						return False
				scene_active = False
				return True
			else:
				dialogue(enemy['name'],speak)

		attack = int(round((enemy['dmg']*(1-(random.randrange(10)/20)))*(1-(stats.dfc[char.armor]/100))))
		char.hp[0] -= attack
		clear()
		print_message("The enemy attacks! You suffer "+Style.BRIGHT+Fore.RED+str(attack)+" damage.")
		if char.hp[0] <= 0:
			die()
			scene_active = False
			return False

def die():
	clear()
	print_message(Fore.RED+Style.BRIGHT+"YOU DIED.")
	print_message("You have lost your items and 100 gold has been deducted from you stash.")
	char.bag = copy.deepcopy(char.default_bag)
	char.hp[0] = char.hp[1]
	char.gold -= 100
	char.deathwish = False
	if char.gold < 0:
		char.gold = 0
	hand = "fists"
	armor = "rags"

def get_hp(enemy=None):
	if enemy:
		hp = enemy['hp']
	else:
		hp = char.hp

	if hp[0] <= hp[1]/5:
		return Style.BRIGHT+Fore.RED+str(hp[0])+"/"+Style.NORMAL+str(hp[1])
	elif hp[0] <= hp[1]/1.3333:
		return Style.BRIGHT+Fore.YELLOW+str(hp[0])+"/"+Style.NORMAL+str(hp[1])
	else:
		return Style.BRIGHT+Fore.GREEN+str(hp[0])+"/"+Style.NORMAL+str(hp[1])

def reward(amount, name=None, silent=False):
	if not silent:
		clear()
		border = ["╔══","║  ","  ║","","╚══","═╝",""]
		if name == None:
			outtext = "You have been rewarded "+str(amount)+" gold!"
		else:
			outtext = name+" has rewarded you "+str(amount)+" gold!"
		prefix = ""
		for i in range(int(round((termsize.getTerminalSize()[1]/2)))-3):
			print()
		for i in range(int(round((termsize.getTerminalSize()[0]/2)-(len(outtext)/2)))-6):
			prefix += " "
		for i in range(len(outtext)):
			border[0] += "═"
			border[3] += " "
		for i in range(int(round((len(outtext)-len("Press enter."))/2))):
			border[6] += "═"
		border[0] += "══╗"
		for i in range(len(border[0]) - len(border[4]+border[6]+"Press enter."+border[6]+border[5])):
		 	border[5] = "═"+border[5]
		print(prefix+Back.YELLOW+Fore.BLACK+border[0])
		print(prefix+Back.YELLOW+Fore.BLACK+border[1]+border[3]+border[2])
		print(prefix+Back.YELLOW+Fore.BLACK+border[1]+Style.BRIGHT+Fore.WHITE+outtext+Style.NORMAL+Fore.BLACK+border[2])
		print(prefix+Back.YELLOW+Fore.BLACK+border[1]+border[3]+border[2])
		print(prefix+Back.YELLOW+Fore.BLACK+border[4]+border[6]+"Press enter."+border[6]+border[5])

		enter(True)
	char.gold += amount

def reward_item(giftid,amount=1,name=None, silent=False):
	if not silent:
		clear()
		border = ["╔══","║  ","  ║","","╚══","╝",""]
		if name == None:
			outtext = "You have been given ["+get_name(giftid)+"] x"+str(amount)+"."
		else:
			outtext = name+" has given you ["+get_name(giftid)+"] x"+str(amount)+"."
		prefix = ""
		for i in range(int(round((termsize.getTerminalSize()[1]/2)))-3):
			print()
		for i in range(int(round((termsize.getTerminalSize()[0]/2)-(len(outtext)/2)))-6):
			prefix += " "
		for i in range(len(outtext)):
			border[0] += "═"
			border[3] += " "
		for i in range(int(round((len(outtext)-len("Press enter."))/2))):
			border[6] += "═"
		border[0] += "══╗"
		for i in range(len(border[0]) - len(border[4]+border[6]+"Press enter."+border[6]+border[5])):
		 	border[5] = "═"+border[5]
		print(prefix+Back.YELLOW+Fore.BLACK+border[0])
		print(prefix+Back.YELLOW+Fore.BLACK+border[1]+border[3]+border[2])
		print(prefix+Back.YELLOW+Fore.BLACK+border[1]+Style.BRIGHT+Fore.WHITE+outtext+Style.DIM+Fore.BLACK+border[2])
		print(prefix+Back.YELLOW+Fore.BLACK+border[1]+border[3]+border[2])
		print(prefix+Back.YELLOW+Fore.BLACK+border[4]+border[6]+"Press enter."+border[6]+border[5])

		enter(True)
	if giftid in char.bag:
		char.bag[giftid] += amount
	else:
		char.bag[giftid] = amount

hml =['High','Middle','Low']

# All the character's data
class char:
	quest_active = 0
	hp = [100, 100] # [CURRENT HP, MAX HP]
	xp = 0
	lvl = 0
	gold = 0
	arrows = 0
	deathwish = False
	hand = "fists"
	armor = "rags"
	bag = {'fists' : 1, "rags" : 1, "nothing" : 1} # The Player's inventory. {"potions" : 2, "sword_iron" : 1}
	default_bag = {'fists' : 1, "rags" : 1, "nothing" : 1}

# Catch-all class where I put non-character related data
class stats:
	dfc = {}
	heal = {}
	names = {}
	dmg = {}
	values = {}
	enemies = [ # Database of enemies and their stats, Size is from 1 to 3
			{'name' : 'Bear', 'hp' : [20,20], 'dmg' : 30, 'dfc' : 5, 'can_block': False, 'size': 3},
			{'name' : 'Tree Monkey', 'hp' : [3,3], 'dmg' : 5, 'dfc' : 0, 'can_block': False, 'size': 1},
			{'name' : 'Wanderer', 'hp' : [10,10], 'dmg' : 15, 'dfc' : 30, 'can_block': True, 'size': 2},
			{'name' : 'Dragonling', 'hp' : [15,15], 'dmg' : 18, 'dfc' : 10, 'can_block': False, 'size': 2},
			{'name' : 'Warlock', 'hp' : [50,50], 'dmg' : 35, 'dfc' : 30, 'can_block': True, 'size': 2},
	]
	time = [7,0] # Hours, Minutes
	shopbag = {}

# Initiate Game
if os.name == "nt":
	os.system("title SKYRIM 2")
load()
init(autoreset=True)

# INTRO
if '-nointro' not in sys.argv: # Check if the script was run with -nointro
	prefix = ""
	for i in range(int(round(termsize.getTerminalSize()[1]/2))-1):
		prefix += "\n"
	for i in range(int(round((termsize.getTerminalSize()[0]-30)/2))):
		prefix += " "
	clear()
	time.sleep(1)
	print(prefix+"........ ......... ........")
	time.sleep(.2)
	clear()
	print(prefix+"bethesda softworks presents...")
	time.sleep(.2)
	clear()
	print(prefix+"BETHESDA SOFTWORKS PRESENTS...")
	time.sleep(2)
	clear()
	print(prefix+"bethesda softworks presents...")
	time.sleep(.2)
	clear()
	print(prefix+"........ ......... ........")
	time.sleep(.2)
	clear()
	time.sleep(2)

	prefix = ""
	prefix2 = ""

	for i in range(int(round(termsize.getTerminalSize()[1]/2))-art.logo[3]):
		prefix += "\n"
	for i in range(int(round(termsize.getTerminalSize()[0]/2))-art.logo[2]):
		prefix2 += " "
	clear()
	print(prefix)
	for i in art.logo[0].split("\n"):
		print(prefix2+Style.BRIGHT+Fore.BLACK+i)
	time.sleep(.2)
	clear()
	print(prefix)
	for i in art.logo[0].split("\n"):
		print(prefix2+Style.DIM+Fore.WHITE+i)
	time.sleep(.2)
	clear()
	print(prefix)
	for i in art.logo[1].split("\n"):
		print(prefix2+Style.NORMAL+Fore.WHITE+i)
	time.sleep(.2)
	clear()
	print(prefix)
	for i in art.logo[1].split("\n"):
		print(prefix2+Style.BRIGHT+Fore.WHITE+i)
	time.sleep(2)
	prefix2 = ""
	for i in range(int(round(termsize.getTerminalSize()[0]/2))-5):
		prefix2 += " "
	print(prefix2,end="")
	enter()
	prefix = ""
	prefix2 = ""

	for i in range(int(round(termsize.getTerminalSize()[1]/2))-art.logo[3]):
		prefix += "\n"
	for i in range(int(round(termsize.getTerminalSize()[0]/2))-art.logo[2]):
		prefix2 += " "
	print(prefix)
	for i in art.logo[1].split("\n"): # 1
		print(prefix2+Style.BRIGHT+Fore.WHITE+i)
	time.sleep(.2)
	clear()
	print(prefix)
	for i in art.logo[1].split("\n"): # 2
		print(prefix2+Style.NORMAL+Fore.WHITE+i)
	time.sleep(.2)
	clear()
	print(prefix)
	for i in art.logo[0].split("\n"): # 3
		print(prefix2+Style.DIM+Fore.WHITE+i)
	time.sleep(.2)
	clear()
	print(prefix)
	for i in art.logo[0].split("\n"): # 4
		print(prefix2+Style.BRIGHT+Fore.BLACK+i)
	time.sleep(.2)
	clear()
	time.sleep(2)

# GAME LOOP
menu_item = 0
while True:

	# Double check item validities
	if char.hand not in char.bag:
		char.hand = "fists"
		if char.armor not in char.bag:
			char.armor = "nothing"

	# Scene selection
	scenes = ['Shop','Wilderness','The King\'s Castle','Inventory','Quit']
	scene = menu(scenes, 'Gold: '+Fore.YELLOW+str(char.gold)+Style.RESET_ALL+
	'\nHP: '+get_hp()+Style.RESET_ALL+
	'\nXP: '+Fore.WHITE+Style.BRIGHT+str(char.xp)+Style.NORMAL+'/1000'+Style.RESET_ALL+'\nLevel: '+Fore.WHITE+Style.BRIGHT+str(char.lvl)+Style.RESET_ALL,
	" "+Back.WHITE+Fore.BLACK+" "+get_time()+" ", menu_item=menu_item)

	scene_active = True # When this is false, the loop returns to the main menu

	# Buy and sell items
	if scene == "Shop":
		stats.shopbag = {}
		for i in list(stats.names.keys()):
			stats.shopbag[i] = 100
		menu_item = 0
		while scene_active:
			if stats.time[0] < 8 or stats.time[0] > 20:
				clear()
				sign("sign on the door","SHOP IS CLOSED. OUR HOURS ARE 8 AM TO 9 PM EXCEPT ON HOLIDAYS. FREE WIFI INSIDE.", False)
				advance_time(5)
				scene_active = False
				continue
			action = menu(['Buy','Sell','Back'], Style.BRIGHT+'SHOP', menu_item=menu_item)
			if action == "Back":
				scene_active = False
			elif action == "Buy":
				menu_item = 0
				while True:
					action = menu(['Weapons','Clothing','Aid','Back'], Style.BRIGHT+'SHOP: BUY', menu_item=menu_item)
					if action == 'Weapons':
						menu_item = 0
						while True:
							advance_time(random.randint(8,15))
							items = []
							for i in stats.shopbag:
								if i not in stats.dmg: or i in ['fists','nothing','king_goose']
									continue
								tabs = "\t\t" if len(get_name(i)) >= 12 else "\t\t\t"
								items += [get_name(i)+tabs+"Value: "+str(stats.values[i])+"\tStock: "+str(stats.shopbag[i])]
							items += ['Back']
							action = menu(items, Style.BRIGHT+'SHOP: BUY: WEAPONS\n\nShopkeeper\'s Gold: '+Style.RESET_ALL+Fore.YELLOW+"INFINITE (WIP)"+Style.RESET_ALL+Style.BRIGHT+"\nYour Gold: "+Style.RESET_ALL+Fore.YELLOW+str(char.gold),"E/Enter: Buy", menu_item=menu_item)
							if action not in ['Cancel','Back']:
								action = action[:action.index("\t")].strip()
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
									print("\n"+Style.BRIGHT+Back.RED+"You don't have enough gold!")
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
					elif action == 'Clothing':
						menu_item = 0
						while True:
							advance_time(random.randint(8,15))
							items = []
							for i in stats.shopbag:
								if i not in stats.dfc: or i in ['fists','nothing','king_goose']
									continue
								tabs = "\t\t" if len(get_name(i)) >= 12 else "\t\t\t"
								items += [get_name(i)+tabs+"Value: "+str(stats.values[i])+"\tStock: "+str(stats.shopbag[i])]
							items += ['Back']
							action = menu(items, Style.BRIGHT+'SHOP: BUY: CLOTHING\n\nShopkeeper\'s Gold: '+Style.RESET_ALL+Fore.YELLOW+"INFINITE (WIP)"+Style.RESET_ALL+Style.BRIGHT+"\nYour Gold: "+Style.RESET_ALL+Fore.YELLOW+str(char.gold),"E/Enter: Buy", menu_item=menu_item)
							if action not in ['Cancel','Back']:
								action = action[:action.index("\t")].strip()
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
									print("\n"+Style.BRIGHT+Back.RED+"You don't have enough gold!")
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
								menu_item = 1
								break
					elif action == 'Aid':
						menu_item = 0
						while True:
							advance_time(random.randint(8,15))
							items = []
							for i in stats.shopbag:
								if i not in stats.heal or i in ['fists','nothing','king_goose']:
									continue
								tabs = "\t\t" if len(get_name(i)) >= 12 else "\t\t\t"
								items += [get_name(i)+tabs+"Value: "+str(stats.values[i])+"\tStock: "+str(stats.shopbag[i])]
							items += ['Back']
							action = menu(items, Style.BRIGHT+'SHOP: BUY: AID\n\nShopkeeper\'s Gold: '+Style.RESET_ALL+Fore.YELLOW+"INFINITE (WIP)"+Style.RESET_ALL+Style.BRIGHT+"\nYour Gold: "+Style.RESET_ALL+Fore.YELLOW+str(char.gold),"E/Enter: Buy", menu_item=menu_item)
							if action not in ['Cancel','Back']:
								action = action[:action.index("\t")].strip()
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
									print("\n"+Style.BRIGHT+Back.RED+"You don't have enough gold!")
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
								menu_item = 2
								break
					elif action == "Back":
						menu_item = 0
						break
			elif action == "Sell":
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
					action = menu(items, Style.BRIGHT+"SHOP: SELL"+Style.RESET_ALL+"\n\nShopkeeper's Gold: INFINITE\nYour Gold: "+str(char.gold),"E/Enter: Sell - F: Drop", special_f=True, menu_item=menu_item)
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
			elif action == 'Back':
				scene_active = False
				menu_item = 0

	# Fight random enemies
	elif scene == "Wilderness":
		if char.quest_active == 2.5:
			print_message("You enter the wilderness looking for the King's lost goose...")
			print_message("As you continue forward, you spot a sign down the path.")
			sign("sign on the tree","WE HAVE YOUR DUMB GOOSE. CATCH US IF YOU CAN.",False)
			print_message("You sprint down the path...")
			dialogue("?","Hey, you!")
			print_message("You turn around and see a young punk emerge from the bushes.")
			dialogue("Punk","That's right, I'm talking to you. You want your goose? You're going to have to get through me!")
			if not combat({'name' : 'Punk', 'hp' : [10,10], 'dmg' : 1, 'dfc' : 0, 'can_block': True, 'size': 2},False,True):
				continue
			dialogue("Punk","No fair!")
			print_message("A tall Nord walks out of the bushes.")
			dialogue("Tall Nord","I see you've defeated my young apprentice, but you're not gonna get through me!")
			dialogue("Tall Nord","POWER OF THE SUN, FLOW THROUGH ME!!!")
			if not combat({'name' : 'Tall Nord', 'hp' : [30,30], 'dmg' : 8, 'dfc' : 20, 'can_block': True, 'size': 2},False,True):
				continue
			dialogue("Tall Nord","I- I\'ve been defeated in combat. How can this be?",
			["You did alright.","You suck and so does your apprentice.","Can I have the goose now?","Give me the goose or taste my blade."])
			print_message("The tall Nord puts two fingers in his mouth and whistles loudly.")
			print_message("A large, fat bear with makeshift armor comes stumbling out of the bushes.")
			dialogue("Tall Nord","Roller, attack!")
			if not combat({'name' : 'Roller the Bear', 'hp' : [50,50], 'dmg' : 30, 'dfc' : 30, 'can_block': False, 'size': 3},False,speak="Get back here! [in bear]"):
				continue
			dialogue("Tall Nord","Roller, NOOOO!")
			dialogue("Roller the Bear","*roars in defeat*")
			print_message("The bear rolls over dead.")
			action = dialogue("Tall Nord","Fine... take the goose. It's just ahead, straight down the path. Just... please don't kill us.",
			['Fine. Just this once.','Run.','Request denied.','*mimic the lightsaber ignition sound with your mouth*'])
			if action in [0,1]:
				dialogue("Tall Nord","Thank you! Thank you!")
				print_message('The Nord and punk scurry off into the bushes.')
			else:
				print_message("You swiftly behead both the Nord and the punk.")
			print_message("After a few minutes of walking down the path, you come across the King's goose.")
			dialogue("Goose","HONK")
			print_message("You grab the goose. It honks and struggles, but you manage to stuff it in your bag.")
			reward_item("king_goose",silent=True)
			enter()
			char.quest_active = 3
		else:
			combat(copy.deepcopy(stats.enemies[random.randrange(len(stats.enemies))]))

	elif scene == 'The King\'s Castle':
		advance_time(30)
		if char.quest_active == -1:
			clear()
			print_message("There are no more quests. Nice job...")
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
				print_message("The goose jumps out of your bag and onto the King's lap.")
				dialogue("The King","Can it be? My beloved goose has been returned to me!")
				action = dialogue("The King","How can I ever repay you?",
				["No need, sir.","Your happiness is enough for me.","Gold will do.","The crown."])
				if action in [0,1]:
					dialogue("The King","Ha! You are too much. Here, take this. I insist.")
					reward(500, "The King")
					use_item("king_goose")
				elif action == 2:
					dialogue("The King","Hm. Well, at least you're honest.")
					reward(200, "The King")
					use_item("king_goose")
				elif action ==3:
					dialogue("The King","Soon perhaps. But that conversation is for another day. In the meantime, take this.")
					reward(200, "The King")
					use_item("king_goose")
				char.quest_active = -1

		if char.deathwish:
			dialogue("The King","Guards! Arrest this man!")
			if not combat({'name' : 'Royal Guard', 'hp' : [20,20], 'dmg' : 20, 'dfc' : 50, 'can_block': True, 'size': 2}, False):
				char.deathwish = False
				continue
			dialogue("Royal Guard Commander","Brother! He's...dead... YOU'LL PAY FOR THIS!!!")
			if not combat({'name' : 'Royal Guard Commander', 'hp' : [30,30], 'dmg' : 30, 'dfc' : 50, 'can_block': True, 'size': 2}, False):
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
				if combat({'name' : 'The King', 'hp' : [30,30], 'dmg' : 50, 'dfc' : 50, 'can_block': True, 'size': 2}, False):
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
		if '-nosave' not in sys.argv:
			save()
		clear()
		print("Thanks for playing!")
		sys.exit()

	menu_item = scenes.index(scene)
