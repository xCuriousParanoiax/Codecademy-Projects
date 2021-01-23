import sys
import random
import colorama
from collections import Counter
from colorama import Fore, Style


# Unfinished # Needs fixing


trainers = []


commands_list = ("enemy", "active", "potions", "pokemons", "attack", "end", "quit", "help", "clear")

pokemon_names = ("Pikachu", "Charmander", "Squirtle", "Bulbasaur", "Nidoran")
#potions = ("paralyze", "weaken", "infect", "lock", "force", "poison", "double", "heal", "revive", "immune", "free")
potions = ("paralyze", "weaken", "lock", "force", "double", "heal", "revive", "immune", "free")

description = {
		"paralyze": "None", 
		"weaken": "None", 
		"infect": "None", 
		"lock": "None", 
		"force": "None", 
		"poison": "None", 
		"double": "None", 
		"immune": "None", 
		"free": "None",
		"heal": "Will give your active Pokemon full health back. Cannot be used on knocked out Pokemons to revive them.", 
		"revive": "Will revive your active Pokemon (if knocked out) giving it 15% of its original health back. A revived Pokemon may fall captive when knocked out."
		}

pika = ("Pikachu", 10, "Electric")
char = ("Charmander", 9, "Fire")
sqrt = ("Squirtle", 8, "Water")
bulb = ("Bulbasaur", 7, "Grass")
nid = ("Nidoran", 6, "Poison")

#pokemons = (pika, char, sqrt, bulb, nid)
pokemons = (char, sqrt, bulb)

calc = {
		"Normal": {
				"Ghost": 0,
				"Rock": 0.5, "Steel": 0.5
				},

		"Fire": {
				"Grass": 2, "Ice": 2, "Bug": 2, "Steel": 2,
				"Fire": 0.5, "Water": 0.5, "Rock": 0.5, "Dragon": 0.5
				},

		"Water": {
				"Fire": 2, "Ground": 2, "Rock": 2,
				"Water": 0.5, "Grass": 0.5, "Dragon": 0.5
				},
		"Electric": {
				"Ground": 0,
				"Water": 2, "Flying": 2,
				"Electric": 0.5, "Grass": 0.5, "Dragon": 0.5
				},
		"Grass": {
				"Water": 2, "Ground": 2, "Rock": 2,
				"Fire": 0.5, "Grass": 0.5, "Poison": 0.5, "Flying": 0.5, "Bug": 0.5, "Dragon": 0.5, "Steel": 0.5
				},
		"Ice": {
				"Grass": 2, "Ground": 2, "Flying": 2, "Dragon": 2,
				"Fire": 0.5, "Water": 0.5, "Ice": 0.5, "Steel": 0.5
				},
		"Fighting": {
				"Ghost": 0,
				"Normal": 2, "Ice": 2, "Rock": 2, "Dark": 2, "Steel": 2,
				"Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Fairy": 0.5
				},
		"Poison": {
				"Steel": 0,
				"Grass": 2, "Fairy": 2,
				"Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5
				},
		"Ground": {
				"Flying": 0,
				"Grass": 0.5, "Bug": 0.5,
				"Fire": 2, "Electric": 2, "Poison": 2, "Rock": 2, "Steel": 2
				},
		"Flying": {
				"Grass": 2, "Fighting": 2, "Bug": 2,
				"Electric": 0.5, "Rock": 0.5, "Steel": 0.5
				},
		"Psychic": {
				"Dark": 0,
				"Fighting": 2, "Poison": 2,
				"Psychic": 0.5, "Steel": 0.5
				},
		"Bug": {
				"Grass": 2, "Psychic": 2, "Dark": 2,
				"Fire": 0.5, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Ghost": 0.5, "Steel": 0.5, "Fairy": 0.5
				},
		"Rock": {
				"Fire": 2, "Ice": 2, "Flying": 2, "Bug": 2,
				"Fighting": 0.5, "Ground": 0.5, "Steel": 0.5
				},
		"Ghost": {
				"Normal": 0,
				"Dark": 0.5,
				"Psychic": 2, "Ghost": 2
				},
		"Dragon": {
				"Fairy": 0,
				"Dragon": 2,
				"Steel": 0.5
				},
		"Dark": {
				"Psychic": 2, "Ghost": 2,
				"Fighting": 0.5, "Dark": 0.5, "Fairy": 0.5
				},
		"Steel": {
				"Ice": 2, "Rock": 2, "Fairy": 2,
				"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Steel": 0.5
				},
		"Fairy": {
				"Fighting": 2, "Dragon": 2, "Dark": 2,
				"Fire": 0.5, "Poison": 0.5, "Steel": 0.5
				}
	}

class Potions:

	def heal(self):
		'''Will give the active Pokemon max health back. Cannot be used on knocked out Pokemons to revive them.'''
		if self.active_pokemon.knocked_out:
			print(f"{Fore.LIGHTRED_EX}Can't heal a knocked out Pokemon. You must revive it first!")
		elif self.active_pokemon.current_health == self.active_pokemon.max_health:
			print(f"{Fore.LIGHTRED_EX}{self.active_pokemon.name}'s already at max health!")
		else:
			self.active_pokemon.current_health = self.active_pokemon.max_health
			self.potions_collection["heal"] -= 1
			print(f"{Fore.LIGHTGREEN_EX}{self.active_pokemon.name} is back to max health!")

	def revive(self):
		'''Will revive a Pokemon that's knocked out giving it 15% of its max health back'''
		if self.active_pokemon.knocked_out == True:
			self.active_pokemon.knocked_out = False
			self.active_pokemon.current_health = self.active_pokemon.max_health * 0.15
			self.active_pokemon.risks_capture = True
			self.potions_collection["revive"] -= 1
			print(f'{Fore.LIGHTGREEN_EX}{self.active_pokemon.name} revived with 15% of it\'s original health back!')
			print(f'{Fore.RED}Note: a revived Pokemon may get captured if it gets knocked out again!')
		else:
			print(f"{Fore.LIGHTRED_EX}Only a knocked out Pokemon can be revived!")


	def double(self):
		if not self.active_pokemon.knocked_out:
			self.active_pokemon.attack_power *= 2
			self.active_pokemon.doubled = 3
			self.potions_collection["double"] -= 1
		else:
			print(f"{Fore.LIGHTRED_EX}You can't use this potion on a knocked out Pokemon!")

	def immune(self):
		if not self.active_pokemon.knocked_out:
			self.active_pokemon.immune = 3
			self.potions_collection["immune"] -= 1
		else:
			print(f"{Fore.LIGHTRED_EX}You can't use this potion on a knocked out Pokemon!")

	def weaken(self, other):
		if not other.active_pokemon.knocked_out:
			other.active_pokemon.weakened = 3
			self.potions_collection["weaken"] -= 1
		else:
			print(f"{Fore.LIGHTRED_EX}You can't use this potion on a knocked out Pokemon!")

	def paralyze(self, other):
		if not other.active_pokemon.knocked_out:
			other.active_pokemon.paralyzed = 3
			self.potions_collection["paralyze"] -= 1
		else:
			print(f"{Fore.LIGHTRED_EX}You can't use this potion on a knocked out Pokemon!")

	def lock(self, other):
		if not other.active_pokemon.knocked_out:
			other.active_pokemon.locked = 3
			self.potions_collection["lock"] -= 1
		else:
			print(f"{Fore.LIGHTRED_EX}You can't use this potion on a knocked out Pokemon!")

	def force(self, other):
		viable_choices = [other.pokemon_collection[pokemon] for pokemon in other.pokemon_collection.keys() if not other.pokemon_collection[pokemon].knocked_out and other.pokemon_collection[pokemon] != other.active_pokemon]
		if len(viable_choices) > 0:
			other.active_pokemon.locked = 0
			other.active_pokemon = random.choice(viable_choices)
			self.potions_collection["force"] -= 1
		else:
			print(f"{Fore.LIGHTRED_EX}Can't force {other.name} to switch Pokemons! They have no other viable choices!")

	def free(self):
		if not self.active_pokemon.knocked_out:
			self.active_pokemon.paralyzed = 0
			self.active_pokemon.locked = 0
			self.potions_collection["free"] -= 1
		else:
			print(f"{Fore.LIGHTRED_EX}You can't use this potion on a knocked out Pokemon!")

#potions = ("infect", "poison")

class Pokemon:

	def __init__(self, name, level, pokemon_type):
		self.name = name
		self.level = level
		self.pokemon_type = pokemon_type

		self.max_health = level * 10
		self.current_health = level * 10
		self.attack_power = level

		self.risks_capture = False
		self.knocked_out = False
		self.immune = 0
		self.weakened = 0
		self.paralyzed = 0
		self.doubled = 0
		self.locked = 0

	def __repr__(self):
		spaces = " " * (15 - len(self.name))
		return f"{self.name} {spaces} Level: {self.level}   -   Attack power: {self.attack_power}   -   Health: {self.current_health}   -   Type: {self.pokemon_type}"

	def stats(self):
		print(f"\nName: {self.name}\nLevel: {self.level}\nType: {self.pokemon_type}\nAttack power: {self.attack_power}\nHealth: {self.current_health}\n")

class Trainer(Potions):
	def __init__(self, name):
		self.name = name
		self.potions_collection = Counter(random.choices(potions, k=7))
		#self.potions_collection = Counter(random.choices(potions, k=1))
		self.captured_counter = 1

		self.random_pokemons = random.sample(pokemons, k=3)

		self.pokemon_collection = {}
		self.gen_pokeomns(self.random_pokemons)

		self.active_pokemon = self.pokemon_collection[list(self.pokemon_collection.keys())[0]]

	def gen_pokeomns(self, random_pokemons):
		for pokemon in random_pokemons:
			pokemon_name, pokemon_level, pokemon_type = pokemon
			self.pokemon_collection[pokemon_name] = Pokemon(pokemon_name, pokemon_level, pokemon_type)

	def switch_pokemon(self, pokemon_name):
		if pokemon_name == self.active_pokemon.name:
			print(f"{Fore.LIGHTGREEN_EX}{self.active_pokemon.name} is already your active fighter!")
		elif self.active_pokemon.locked:
			print(f'{Fore.RED}Your Pokemon is in lock mode! You can\'t switch to another one unless you "free" it!')
		else:
			self.active_pokemon = self.pokemon_collection[pokemon_name]

	def __repr__(self):
		return f"I'm {self.name} and I'm a Pokemon master!"



class Game:

	def __init__(self):
		self.player_1 = Trainer(self.pick_names("one"))
		self.player_2 = Trainer(self.pick_names("two"))
		self.other_player = self.player_2
		self.player_1.playing = True
		self.player_2.playing = False
		self.player_1.has_attacked = False
		self.player_2.has_attacked = False
		self.append_objects(self.player_1, self.player_2)
		#self.board  = {self.player_1: {}, self.player_2: {}}

	def pick_names(self, num):
		while True:
			player = input(f"Insert name for player {num}: ")
			if player.isalpha() and len(player) >= 4:
				break
			else:
				print(f"{Fore.LIGHTRED_EX}Player name must be four or more characters long and consist of letters only!{Style.RESET_ALL}")
		return player

	def append_objects(self, *objects):
		for obj in objects:
			trainers.append(obj)

	def quit(self):
		strng = f"{self.other_player.name} wins!!".upper()
		print(f"{Fore.LIGHTWHITE_EX}{strng}")
		sys.exit()

	def start_msg(self):
		print("\nLet's start! Here's a list of all the commands that you can use:")
		self.help_msg()
		print("""
Each of you will be given three Pokemons and seven potions which are selected randomly.
One of the Pokemons will be automatically set as your active fighter on your first turn.
But you don't have to stick with it, you can switch to another Pokemon that you have using the "switchto" command as mentioned above.
You must use the command "end" when you're done making your moves to allow the other player to make his.
""")

	def help_msg(self):
		print("""
Type:

"end"                                  to end your turn
"help"                                 to see this help message
"quit"                                 to quit the game (and lose)
"clear"                                to clear the screen
"enemy"                                to view the enemy's stats
"active"                               to view your active Pokemon's stats
"attack"                               to attack the other player's active Pokemon with you active Pokemon
"potions"                              to view the potions you have
"pokemons"                             to view the pokemons you have
"usepo" [potion name]                  to use a potion
"switchto" [pokemon name]              to switch your active Pokemon with another Pokemon that you have
""")

	def list_potions(self, player):
		if any(player.potions_collection.values()):
			print("\nYou have:\n")
			for key,value in player.potions_collection.items():
				if player.potions_collection[key] > 0:
					print(f"{key}: {value}  -  {description[key]}")
		else:
			print("\nYou have no potions left!")
		print()

	def list_pokemons(self, player):
		print("\nYou have:\n")
		for pokemon in sorted(player.pokemon_collection, key=lambda p: +len(p)):
			player.pokemon_collection[pokemon].stats()
		print()

	def capture(self, attacker, victim):
		capture = random.choice([True, False])
		if capture == True:
			self.knock_out(victim.active_pokemon)
			self.defeated(victim)
			captured = victim.active_pokemon
			del victim.pokemon_collection[captured.name]
			self.defeated(victim)
			strng = f"{attacker.name} captured {victim.name}'s {victim.active_pokemon.name}!!".upper()
			print(f"{Fore.LIGHTWHITE_EX}{strng}")
			if captured.name in attacker.pokemon_collection:
				captured.name += f"_{attacker.duplicates_counter}"
				attacker.captured_counter += 1
			attacker.pokemon_collection[captured.name] = captured
			victim.active_pokemon = random.choice([victim.pokemon_collection[pokemon] for pokemon in victim.pokemon_collection.keys()])
		else:
			self.knock_out(victim.active_pokemon)
			self.defeated(victim)
			print(f"{Fore.RED}{victim.name}'s {victim.active_pokemon.name} knocked out!")

	def calculate_damage(self, attacker, victim):
		if victim.active_pokemon.pokemon_type in calc[attacker.active_pokemon.pokemon_type]:
			damage = attacker.active_pokemon.attack_power * calc[attacker.active_pokemon.pokemon_type][victim.active_pokemon.pokemon_type]
		else:
			damage = attacker.active_pokemon.attack_power
		if victim.active_pokemon.immune:
			damage = attacker.active_pokemon.attack_power / 2
		if victim.active_pokemon.weakened:
			damage *= 2
		return damage

	def knock_out(self, pokemon):
		pokemon.locked = 0
		pokemon.immune = 0
		pokemon.doubled = 0
		pokemon.weakened = 0
		pokemon.paralyzed = 0
		pokemon.knocked_out = True
		pokemon.current_health = 0

	def attack(self, attacker, victim):
		if attacker.has_attacked == True:
			print(f"{Fore.LIGHTRED_EX}You've already used your attack for this turn!")
		elif attacker.active_pokemon.paralyzed:
			print(f'{Fore.LIGHTRED_EX}Your Pokemon is paralyzed and can\'t attack right now! "free" it or use another Pokemon to attack!')
		else:
			damage = self.calculate_damage(attacker, victim)
			if victim.active_pokemon.current_health <= damage:
				if victim.active_pokemon.risks_capture:
					self.capture(attacker, victim)
				else:
					self.knock_out(victim.active_pokemon)
					self.defeated(victim)
					print(f"{Fore.RED}{victim.name}'s {victim.active_pokemon.name} knocked out!")
			else:
				victim.active_pokemon.current_health -= damage
			attacker.has_attacked = True
			#for trainer in trainers:
			#	trainer.active_pokemon.stats()

	def defeated(self, player):
		if len(player.pokemon_collection) < 1:
			if player == self.player_1:
				strng = f"{self.player_2.name} wins!!".upper()
			else:
				strng = f"{self.player_1.name} wins!!".upper()
			print(f"{Fore.LIGHTWHITE_EX}{strng}")
			sys.exit()
		else:
			pokemons_left = [player.pokemon_collection[pokemon].knocked_out for pokemon in player.pokemon_collection]
			if not False in pokemons_left and not player.potions_collection["revive"] > 0:
				if player == self.player_1:
					strng = f"{self.player_2.name} wins!!".upper()
				else:
					strng = f"{self.player_1.name} wins!!".upper()
				print(f"{Fore.LIGHTWHITE_EX}{strng}")
				sys.exit()

	def check(self, list_of_players):
		for player in list_of_players:
			if player.active_pokemon.immune:
				player.active_pokemon.immune -= 1
			if player.active_pokemon.weakened:
				player.active_pokemon.weakened -= 1
			if player.active_pokemon.paralyzed:
				player.active_pokemon.paralyzed -= 1
			if player.active_pokemon.doubled:
				player.active_pokemon.doubled -= 1
				if not player.active_pokemon.doubled:
					player.active_pokemon.attack_power = player.active_pokemon.level
			if player.active_pokemon.locked:
				player.active_pokemon.locked -= 1

	def end_turn(self, player):
		if player.active_pokemon.knocked_out:
			print(f'{Fore.LIGHTRED_EX}Your Pokemon is knocked out! You must "revive" it or "switchto" another Pokemon before ending your turn!')
		else:
			player.playing = False
			player.has_attacked = False
			self.other_player.playing = True
			self.other_player = player
			self.check(trainers)

	def run_command(self, player, command):
		if command == "quit":
			self.quit()
		elif command == "end":
			self.end_turn(player)
		elif command == "help":
			self.help_msg()
		elif command == "clear":
			print("\n" * 20)
		elif command == "potions":
			self.list_potions(player)
		elif command == "pokemons":
			self.list_pokemons(player)
		elif command == "active":
			player.active_pokemon.stats()
		elif command == "enemy":
			self.other_player.active_pokemon.stats()
		else:
			if player.active_pokemon.knocked_out:
				print(f'{Fore.LIGHTRED_EX}Your Pokemon is knocked out! "revive" it or "switchto" another one to be able to attack!')
			else:
				self.attack(player, self.other_player)

	def use_potion(self, player,  method_name):
		offense = ("lock", "force", "weaken", "paralyze")
		if method_name not in offense:
			function = getattr(player, method_name)
			function()
		else:
			function = getattr(player, method_name)
			function(self.other_player)


	def handle_commands(self, player, command):
		if command in pokemon_names:
			if command in player.pokemon_collection:
				player.switch_pokemon(command)
			else:
				print(f"{Fore.LIGHTRED_EX}{command} is not in your collection!")
		elif command in player.pokemon_collection:
			player.switch_pokemon(command)
		elif command in potions:
			if player.potions_collection[command] > 0:
				self.use_potion(player, command)
			else:
				print(f"{Fore.LIGHTRED_EX}Sorry, you're out of stock!")
		elif command in commands_list:
			self.run_command(player, command)
		else:
			print(f"{Fore.LIGHTRED_EX}Command not found!")

	def start_turn(self, player):
		while player.playing:
			if player == self.player_1:
				print(f"{Fore.LIGHTCYAN_EX}{player.name}'s move: ", end="")
			else:
				print(f"{Fore.LIGHTYELLOW_EX}{player.name}'s move: ", end="")
			command = input().strip()
			self.handle_commands(player, command)

	def start_game(self):
		#self.start_msg()
		while True:
			self.start_turn(self.player_1)
			self.start_turn(self.player_2)


if __name__ == "__main__":
	Game().start_game()
