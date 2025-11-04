import random, config, os, json, events
from classes import Party, Voter

# LOAD SAVE DATA
if not os.path.exists("profile.json"):
	NAME = ""
	while NAME == "":
		NAME = input("$ Enter your full name: ")
	json_data = {"Name": NAME, "High score": 0}
	with open("profile.json", "w") as json_file:
		json.dump(json_data, json_file, indent=4)
else:
	with open("profile.json", "r") as file:
		PROFILE_DATA = json.load(file)
		NAME = PROFILE_DATA["Name"]



COUNTRY = config.COUNTRY
ARCHETYPES = config.ARCHETYPES

PARTIES = []

def dialogue(choices):
	# get input from the player
	for i in range(len(choices)):
		print(str(i+1) + ") " + choices[i])
	while True: # check if they chose a valid choice
		choice = int(input("$ "))
		if 0 < choice <= len(choices):
			break
	print()
	return(choice)

def do_event(event):
	# do an event, this is a massive function!
	global PLAYER_PARTY, VOTERS, EVENT_QUEUE, COMPLETED_EVENTS
	match event:
	
		case "stance_renberg":
			print("A neighboring country known as Renberg has been cracking down on 'traitors' lately, imprisoning civil rights leaders. You must decide the party's official stance.")
			case "stance_renberg":
				choice = dialogue({
				"We must grant refuge to victims of Renberg's oppression"
				"Their politics are their business"
				"(publicly express approval for Rumburg's government)"
				})
			completed_events(stance_renberg) = choice
			if choice == 1:
				PLAYER_PARTY.LIBERAL += 0.5
				PLAYER_PARTY.SOCIALIST += 0.5
				PLAYER_PARTY.CONSERVATIVE -= 1.0
				PLAYER_PARTY.NATIONALIST -= 2.5
				PLAYER_PARTY.move_politics(0.25, social=-10)
				print("Liberals and socialists are satisfied with your proactive response.")
			elif choice == 2:
				PLAYER_PARTY.SOCIALIST -= 0.5
				PLAYER_PARTY.CONSERVATIVE += 2.0
				PLAYER_PARTY.move_politics(1.25, social=0)
				print("Conservatives are happy with your response.")
			elif choice == 3:
				PLAYER_PARTY.
			
	input("$ Press enter to continue: ")
	print()
	
intro = "Welcome to " + COUNTRY + "! This is the 19" + str(38 + 4 * random.randint(1, 6)) + " General Election, and you are running for president. You will create and name a new party, determine its stance on several divisive political topics, and create a campaign!"
# there will also be a political debate and a speech that heavily affect the charisma modifier
# plus, chances to fabricate scandals, and a few scandals of your own to deal with
print(intro)
input("$ Press enter to continue: ")
print()

# create parties
available_archetypes = list(ARCHETYPES.keys())
print("Here are this election's leading parties:")
for i in range(config.PARTY_COUNT):
	print("—")
	archetype = random.choice(available_archetypes)
	if i == 0:
		party = Party(archetype, incumbent=True)
		incumbent_archetype = archetype # use this for certain events
	else:
		party = Party(archetype)
	available_archetypes.remove(archetype)
	PARTIES.append(party)
	party_text = party.name + " (" + party.initials + ")"
	if party.incumbent:
		party_text += ", incumbent"
	print(party_text)
	print("Leader: " + party.leader + ", Policies: " + party.archetype)
	print(party.motto + ".")
print("—")
input("$ Press enter to continue: ")
print()

# voter demographics
input("$ Now, for the voter demographics: ")
# generate voters
VOTERS = []
VOTER_ARCHETYPES = {"Liberal": 0, "Nationalist": 0, "Conservative": 0, "Capitalist": 0, "Socialist": 0, "Communist": 0, "Independent": 0}
# first, generate loyalists per party
for party in PARTIES:
	for _ in range(random.randint(100, 200)):
		economy = party.economy + random.randint(-2, 2)
		social = party.social + random.randint(-2, 2)
		voter = Voter(economy, social)
		VOTERS.append(voter)
		VOTER_ARCHETYPES[party.archetype] += 1 # for info, later
# generate loyalists for a "ghost party"
archetype = random.choice(available_archetypes)
for _ in range(random.randint(25, 100)):
	economy = ARCHETYPES[archetype][0]
	social = ARCHETYPES[archetype][1]
	voter = Voter(economy, social)
	VOTERS.append(voter)
	VOTER_ARCHETYPES[archetype] += 1
# generate people without a partisan agenda
archetypes = list(ARCHETYPES.keys())
for _ in range(random.randint(350, 500)):
	archetype = random.choice(archetypes)
	economy = ARCHETYPES[archetype][0]
	social = ARCHETYPES[archetype][1]
	voter = Voter(economy, social)
	VOTERS.append(voter)
	VOTER_ARCHETYPES[archetype] += 1
# extra liberals and conservatives
for _ in range(100):
	archetype = random.choice(("Liberal", "Conservative"))
	economy = ARCHETYPES[archetype][0]
	social = ARCHETYPES[archetype][1]
	voter = Voter(economy, social)
	VOTERS.append(voter)
	VOTER_ARCHETYPES[archetype] += 1
# finally, true independents
for _ in range(random.randint(75, 150)):
	economy = random.randint(-10, 10)
	social = random.randint(-10, 10)
	voter = Voter(economy, social, independent=True)
	VOTERS.append(voter)
	VOTER_ARCHETYPES["Independent"] += 1
# print voter demographics
for key in list(VOTER_ARCHETYPES.keys()):
	print(key + "s:" + (" " * (20 - len(key))) + str(VOTER_ARCHETYPES[key] * 10000 + random.randint(0, 9999)))
input("$ Press enter to continue: ")
print()
# now, create a new party with you as the leader
print("Now, it's time to create a new party, with you, " + NAME + ", as its leader!")
party_name = "a"
while party_name.strip()[0][0] == party_name.strip()[0][0].lower():
	party_name = input("$ Enter your party's name: ")
	if len(party_name.strip()) == 0:
		party_name = "a"
		continue
	if party_name.strip()[0][0] == party_name.strip()[0][0].lower():
		print()
		print("Invalid party name! Must be capitalized")
print()
# party motto
party_motto = ""
while len(party_motto) == 0:
	party_motto = input("$ Enter your party's motto (no ending punctuation): ")
print()	
# print this party, now
party = Party("New Party", name=party_name, motto=party_motto, leader=NAME)
party.archetype = party_name # make a new archetype out of the name (this can have funny results)
for entry in ("party", "Party", COUNTRY, " of ", " and "):
	party.archetype = party.archetype.replace(entry, "")
PLAYER_PARTY = party # add this to PARTIES at the end when calculating election results
party_text = party.name + " (" + party.initials + ")"
print(party_text)
print("Leader: " + party.leader + ", Policies: " + party.archetype)
print(party.motto + ".")
input("$ Press enter to continue: ")
print()
# intro events
EVENT_QUEUE = []
COMPLETED_EVENTS = {}
for _ in range(3):
	event = random.choice(events.INTRO_EVENTS)
	events.INTRO_EVENTS.remove(event)
	EVENT_QUEUE.append(event)
# now, do these events
for event in EVENT_QUEUE:
	do_event(event)
