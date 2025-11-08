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
		print("Welcome back, " + NAME + "!")
print()



COUNTRY = config.COUNTRY
ARCHETYPES = config.ARCHETYPES
MONEY = 5
PARTIES = []

def dialogue(choices):
	# get input from the player
	for i in range(len(choices)):
		print(str(i+1) + ") " + choices[i])
	while True: # check if they chose a valid choice
		choice = input("$ ")
		try:
			choice = int(choice)
		except ValueError:
			continue
		if 0 < choice <= len(choices):
			break
	print()
	return(choice)

def do_event(event):
	# do an event, this is a massive function!
	global PLAYER_PARTY, VOTERS, EVENT_QUEUE, COMPLETED_EVENTS
	COMPLETED_EVENTS[event] = True
	
	if event == "stance_lavitia":
		print("A neighboring country known as Lavitia has been cracking down on 'traitors' lately, imprisoning civil rights leaders. You must decide the party's official stance.")
		choice = dialogue((
		"We must grant refuge to victims of Lavitia's oppression",
		"Their politics are their business",
		"We will join them in this endeavor! Viva Lavitia!",
		))
		COMPLETED_EVENTS[event] = choice
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
			PLAYER_PARTY.move_politics(1.25, social=3)
			print("Conservatives are happy with your response, but most see it as overly isolationist.")
		elif choice == 3:
			PLAYER_PARTY.SOCIALIST -= 2.75
			PLAYER_PARTY.LIBERAL -= 2.75
			PLAYER_PARTY.CONSERVATIVE -= 1.0
			PLAYER_PARTY.NATIONALIST += 1.25
			PLAYER_PARTY.COMMUNIST += 0.25
			PLAYER_PARTY.CAPITALIST -= 0.5
			PLAYER_PARTY.move_politics(5.0, social=10)
			text = "You are seen as tyrannical."
			for party in PARTIES:
				if party.social <= -4:
					text += " " + party.leader_full_title + " denounces you."
			print(text)
		
	elif event == "stance_welfare":
		print(COUNTRY + "'s welfare is at a crossroads, and your stance is crucial to attracting voters. Many want it expanded, due to the low quality of healthcare and education services, but capitalists mention that privatizing welfare could help drive growth, and competition could create better services overall. Conservatives want the system to stay as-is.")
		choice = dialogue((
		"No need to rock the boat, we won't privatize or expand our services",
		"We'll increase spending modestly to improve services",
		"A tax increase will be used to improve these services massively",
		"Privatization will create capital and create competition in the process",
		"A less-educated populace is easier to manage, so let's defund",
		))
		COMPLETED_EVENTS[event] = choice
		if choice == 1:
			PLAYER_PARTY.LIBERAL -= 0.5
			PLAYER_PARTY.SOCIALIST -= 2.5
			PLAYER_PARTY.COMMUNIST -= 2.75
			PLAYER_PARTY.CONSERVATIVE += 1.75
			PLAYER_PARTY.CLASS1 -= 0.5
			PLAYER_PARTY.CLASS2 += 0.5
			PLAYER_PARTY.move_politics(0.5, economy=1, social=4)
			print("Communists and socialists are angry, but most others seem to not care much.")
		elif choice == 2:
			PLAYER_PARTY.LIBERAL += 0.75
			PLAYER_PARTY.SOCIALIST += 0.5
			PLAYER_PARTY.COMMUNIST -= 0.5
			PLAYER_PARTY.CONSERVATIVE -= 0.25
			PLAYER_PARTY.CAPITALIST -= 1.0
			PLAYER_PARTY.CLASS1 += 1.5
			PLAYER_PARTY.CLASS2 += 0.5
			PLAYER_PARTY.CLASS3 -= 1.0
			PLAYER_PARTY.move_politics(1.5, economy=-3)
			PLAYER_PARTY.move_politics(0.5, social=-4)
			print("The public is overall happy with your stance, especially lower-class citizens.")
		elif choice == 3:
			PLAYER_PARTY.LIBERAL -= 1.5
			PLAYER_PARTY.SOCIALIST += 1.25
			PLAYER_PARTY.COMMUNIST -= 3.0
			PLAYER_PARTY.CONSERVATIVE -= 2.75
			PLAYER_PARTY.CAPITALIST -= 3.25
			PLAYER_PARTY.CLASS1 += 2.5
			PLAYER_PARTY.CLASS2 -= 0.5
			PLAYER_PARTY.CLASS3 -= 4.0
			PLAYER_PARTY.move_politics(2.5, economy=-7)
			PLAYER_PARTY.move_politics(0.5, social=-4)
			print("Socialists and communists are happy, but middle and upper-class citizens are outraged by the idea of a tax increase.")
		elif choice == 4:
			PLAYER_PARTY.LIBERAL -= 2.0
			PLAYER_PARTY.SOCIALIST -= 3.0
			PLAYER_PARTY.COMMUNIST -= 3.0
			PLAYER_PARTY.CONSERVATIVE -= 1.75
			PLAYER_PARTY.CAPITALIST += 4.0
			PLAYER_PARTY.CLASS1 -= 4.0
			PLAYER_PARTY.CLASS2 -= 2.0
			PLAYER_PARTY.CLASS3 += 3.0
			PLAYER_PARTY.move_politics(3.0, economy=10)
			PLAYER_PARTY.move_politics(1.0, social=3)
			print("Many are outraged, but capitalists are happy. Good thing you still have a whole campaign to get those other voters on your side.")
		elif choice == 5:
			PLAYER_PARTY.LIBERAL -= 4.0
			PLAYER_PARTY.SOCIALIST -= 4.0
			PLAYER_PARTY.COMMUNIST -= 4.0
			PLAYER_PARTY.CONSERVATIVE -= 4.0
			PLAYER_PARTY.CAPITALIST -= 4.0
			PLAYER_PARTY.NATIONALIST += 1.5
			PLAYER_PARTY.CLASS1 -= 5.0
			PLAYER_PARTY.CLASS2 -= 5.0
			PLAYER_PARTY.CLASS3 -= 3.0
			PLAYER_PARTY.move_politics(2.5, economy=4)
			PLAYER_PARTY.move_politics(4.0, social=10)
			print("Everyone hated that. Why would you ever say that?")
			
	elif event == "stance_economy":
		print("You must decide your party's stance on the economy. You can prioritize agricultural growth, industrial growth, or give tax credits to businesses.")
		choice = dialogue((
		"Agriculture will improve living standard and farmer rights",
		"Industry will propel economic growth and create jobs",
		"The world runs on private business, so let's give back",
		))
		COMPLETED_EVENTS[event] = choice
		if choice == 1:
			PLAYER_PARTY.CLASS1 += 3.0
			PLAYER_PARTY.move_politics(1.5, economy=-10)
			print("A new 'Farmers for " + NAME.split()[len(NAME.split())-1] + "' ad aired during a sports game, without your input.")
			PLAYER_PARTY.CHARISMA += 0.75
		elif choice == 2:
			PLAYER_PARTY.CLASS2 += 3.0
			PLAYER_PARTY.move_politics(1.5, economy=-5)
			print("The middle-class rallies behind your promise, with over 20,000 attending.")
		elif choice == 3:
			# by far the most polarizing of the 3 options, making a clear pro-business stance
			PLAYER_PARTY.SOCIALIST -= 2.5
			PLAYER_PARTY.COMMUNIST -= 4.5
			PLAYER_PARTY.CAPITALIST += 3.0
			PLAYER_PARTY.CLASS3 += 3.0
			PLAYER_PARTY.move_politics(2.5, economy=6)
			print("Business leaders praise you. Famous oligarch Leon Tusk promises to offer some funds for your campaign.")

	elif event == "stance_minority":
		print("The minorities in " + COUNTRY + " have often been oppresed and persecuted, and only recently has the situation started to improve. They are still cold towards conservative and authoritarian parties. You can declare a stance, or you can remain neutral.")
		choice = dialogue((
		"(no statement)",
		"We will invest government resources into development in minority areas",
		"We will create universal basic income for minorities",
		"We will improve the legal system to remove bias",
		))
		COMPLETED_EVENTS[event] = choice
		if choice == 1:
			PLAYER_PARTY.LIBERAL -= 0.5
			PLAYER_PARTY.SOCIALIST -= 1.0
			PLAYER_PARTY.CONSERVATIVE += 2.5
			PLAYER_PARTY.NATIONALIST += 0.5
			PLAYER_PARTY.MINORITY -= 2.5
			PLAYER_PARTY.move_politics(0.25, social=10)
		elif choice == 2:
			PLAYER_PARTY.LIBERAL += 1.5
			PLAYER_PARTY.SOCIALIST += 1.0
			PLAYER_PARTY.NATIONALIST -= 2.5
			PLAYER_PARTY.CAPITALIST += 1.5 # "government investment drives capital"
			PLAYER_PARTY.MINORITY += 1.0
			PLAYER_PARTY.move_politics(1.5, social=-6)
			PLAYER_PARTY.move_politics(0.5, economy=-2)
			if COMPLETED_EVENTS["stance_lavitia"] != 3:
				print("Yesterday, there was a new political rally: Minorites for " + NAME + ".")
		elif choice == 3:
			PLAYER_PARTY.LIBERAL -= 0.75
			PLAYER_PARTY.SOCIALIST += 2.5
			PLAYER_PARTY.COMMUNIST += 0.5
			PLAYER_PARTY.CONSERVATIVE -= 1.0
			PLAYER_PARTY.NATIONALIST -= 3.5
			PLAYER_PARTY.CLASS1 += 2.5
			PLAYER_PARTY.MINORITY += 3.0
			PLAYER_PARTY.CAPITALIST -= 2.0 # "government investment drives capital"
			PLAYER_PARTY.move_politics(3.0, social=-10, economy=-10)
			print("Yesterday, there was a new political rally: Minorites for " + NAME + ".")			
		elif choice == 4:
			PLAYER_PARTY.LIBERAL += 2.0
			PLAYER_PARTY.SOCIALIST += 1.0
			PLAYER_PARTY.NATIONALIST -= 2.5
			PLAYER_PARTY.MINORITY += 1.5
			PLAYER_PARTY.move_politics(1.5, social=-10)
			if COMPLETED_EVENTS["stance_lavitia"] != 3:
				print("Yesterday, there was a new political rally: Minorites for " + NAME + ".")
			
		for party in PARTIES:
			if party.social <= -4:
				print(party.name + " made a statement in support of civil rights.")
		
	elif event == "stance_tax":
		print("Now, voters want to know your stance on taxes. Conservatives and capitalists want tax cuts, liberals and nationalists want the status quo, and socialists and communists want a tax increase, specifically for the rich. You don't have to make a stance, but some more radical factions will be concerned. You also don't have to be completely honest.")
		choice = dialogue((
		"(refrain from taking any stance)",
		"Taxes will be lowered",
		"Tax structure will not be changed",
		"Eat the rich, through tax",
		"Taxes shall be increased across the board to fund our government",
		))
		COMPLETED_EVENTS[event] = choice
		if choice == 1:
			PLAYER_PARTY.COMMUNIST -= 1.5
			PLAYER_PARTY.NATIONALIST -= 1.0
			PLAYER_PARTY.CAPITALIST -= 1.0
			PLAYER_PARTY.move_politics(1.0, economy=0)
			print("Nobody pays much attention to your campaign, for better or for worse.")
		elif choice == 2:
			PLAYER_PARTY.COMMUNIST -= 7.5
			PLAYER_PARTY.SOCIALIST -= 2.0
			PLAYER_PARTY.CAPITALIST += 2.5
			PLAYER_PARTY.CONSERVATIVE += 1.5
			PLAYER_PARTY.CLASS1 += 1.0
			PLAYER_PARTY.CLASS2 += 1.0
			PLAYER_PARTY.CLASS3 += 2.5
			PLAYER_PARTY.move_politics(2.0, economy=10)
			print("Your populist message appeals to all demographics, except the economic left.")
		elif choice == 3:
			PLAYER_PARTY.COMMUNIST -= 2.5
			PLAYER_PARTY.SOCIALIST -= 1.0
			PLAYER_PARTY.LIBERAL += 1.5
			PLAYER_PARTY.NATIONALIST += 1.0
			PLAYER_PARTY.CLASS1 -= 0.5
			PLAYER_PARTY.CLASS3 += 0.5
			PLAYER_PARTY.move_politics(1.5, economy=2)
			print("Many seem content. Others wanted change, but the middle and upper-class are glad for the stability.")
		elif choice == 4:
			PLAYER_PARTY.COMMUNIST += 1.0
			PLAYER_PARTY.SOCIALIST += 2.5
			PLAYER_PARTY.LIBERAL += 0.5
			PLAYER_PARTY.NATIONALIST -= 1.0
			PLAYER_PARTY.CONSERVATIVE -= 1.5
			PLAYER_PARTY.CAPITALIST -= 5.5
			PLAYER_PARTY.CLASS1 += 1.5
			PLAYER_PARTY.CLASS3 -= 3.5
			PLAYER_PARTY.move_politics(2.5, economy=-6)
			print("Your anti-rich message appeals to everyone... except the rich, along with capitalists and conservatives. The lower-class approves of your proposal.")
		elif choice == 5:
			PLAYER_PARTY.COMMUNIST += 5.0
			PLAYER_PARTY.SOCIALIST += 2.0
			PLAYER_PARTY.LIBERAL -= 2.0
			PLAYER_PARTY.NATIONALIST += 1.0 # "it is your natural duty to help the state"
			PLAYER_PARTY.CONSERVATIVE -= 3.0
			PLAYER_PARTY.CAPITALIST -= 3.5
			PLAYER_PARTY.CLASS1 -= 1.0
			PLAYER_PARTY.CLASS2 -= 1.5
			PLAYER_PARTY.CLASS3 -= 1.0 # "wealth is relative, so it could be worse"
			PLAYER_PARTY.move_politics(4.5, economy=-10)
			print("Most are unhappy with this, except for socialists and communists. Weirdly, nationalists have also been surprisingly supportive.")
		for party in PARTIES:
				if party.economy <= -4:
					print(party.leader_full_title + " pledges to tax the rich.")
				elif party.economy >= 4 or party.archetype == "Conservative":
					print(party.leader_full_title + " pledges to lower taxes.")

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
		voter = Voter(party.archetype, economy, social)
		VOTERS.append(voter)
		VOTER_ARCHETYPES[party.archetype] += 1 # for info, later
# generate loyalists for a "ghost party"
archetype = random.choice(available_archetypes)
for _ in range(random.randint(25, 100)):
	economy = ARCHETYPES[archetype][0]
	social = ARCHETYPES[archetype][1]
	voter = Voter(archetype, economy, social)
	VOTERS.append(voter)
	VOTER_ARCHETYPES[archetype] += 1
# generate people without a partisan agenda
archetypes = list(ARCHETYPES.keys())
for _ in range(random.randint(350, 500)):
	archetype = random.choice(archetypes)
	economy = ARCHETYPES[archetype][0]
	social = ARCHETYPES[archetype][1]
	voter = Voter(archetype, economy, social)
	VOTERS.append(voter)
	VOTER_ARCHETYPES[archetype] += 1
# extra liberals and conservatives
for _ in range(100):
	archetype = random.choice(("Liberal", "Conservative"))
	economy = ARCHETYPES[archetype][0]
	social = ARCHETYPES[archetype][1]
	voter = Voter(archetype, economy, social)
	VOTERS.append(voter)
	VOTER_ARCHETYPES[archetype] += 1
# finally, true independents
for _ in range(random.randint(75, 150)):
	economy = random.randint(-10, 10)
	social = random.randint(-10, 10)
	voter = Voter("Independent", economy, social, independent=True)
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
party.archetype = party.archetype.strip()
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
for event in events.INTRO_EVENTS:
	EVENT_QUEUE.append(event)
# now, do these events
for event in EVENT_QUEUE:
	do_event(event)
# VP selection
print("Now, you must pick your running mate!")
print("Once elected, this will be your Vice President. This has no bearing on your policies.")
input("$ Press enter to continue: ")
print()
choice = dialogue((
config.VP_NAMES[0] + ", who excels at making candidates likeable",
config.VP_NAMES[1] + ", who is great at fabricating scandals",
config.VP_NAMES[2] + ", who will keep the media on your side",
config.VP_NAMES[3] + ", who gathers lots of funds for your campaign",
))
VP = choice
VP_NAME = config.VP_NAMES[choice-1]
print()
print(VP_NAME + " agrees to run with you.")
input("$ Press enter to continue: ")
# earlygame donations
if VP == 4:
	print(VP_NAME + ": Our financials are very important to this election, which is why I have prepared some PACs to donate:")
else:
	print(VP_NAME + ": We need funding to win. Here is the list of organizations who will support us:")
input("$ Press enter to continue: ")
print()
if PLAYER_PARTY.social >= 5.5:
	print(VP_NAME + ": United " + COUNTRY + " Group has donated ₩20,000,000 in support of our right-wing policies.")
	MONEY += 4
	input("$ Press enter to continue: ")
if PLAYER_PARTY.CONSERVATIVE >= 3:
	print(VP_NAME + ": Old Guard of " + COUNTRY + " pledged to donate ₩25,000,000 because of our conservative stance.")
	MONEY += 5
	input("$ Press enter to continue: ")
if "stance_economy" in COMPLETED_EVENTS:
	if COMPLETED_EVENTS["stance_economy"] == 3:
		print(VP_NAME + ": Leon Tusk donated ₩35,000,000 worth of Newton stock to our campaign, as he promised.")
		MONEY += 7
		PLAYER_PARTY.SCANDAL += 1.0
		input("$ Press enter to continue: ")
if VP == 4:
	print(VP_NAME + ": The " + COUNTRY + " Business Council has voted to donate ₩40,000,000 to " + PLAYER_PARTY.name + ", due to my influence in the group.")
	MONEY += 8
	input("$ Press enter to continue: ")
if PLAYER_PARTY.LIBERAL >= 4 or PLAYER_PARTY.SOCIALIST >= 5:
	print(VP_NAME + ": New Hope for " + COUNTRY + " donated ₩15,000,000 in support of your socially-progressive ideals.")
	MONEY += 3
	input("$ Press enter to continue: ")
if PLAYER_PARTY.CLASS2 >= 4:
	print(VP_NAME + ": We have received ₩25,000,000 cumulatively from voter donations. This is great news for our popularity.")
	MONEY += 5
	input("$ Press enter to continue: ")
if "stance_lavitia" in COMPLETED_EVENTS:
	if COMPLETED_EVENTS["stance_lavitia"] == 3:
		print(VP_NAME + ": Devin Wallace, Chancellor of Lavitia has discreetly given the equivalent of ₩20,000,000 to our campaign, for obvious reasons.")
		MONEY += 4
		input("$ Press enter to continue: ")
		if VP != 3:
			print(VP_NAME + ": Honestly, I'm worried about this. There is no way we can keep a donation this big, especially from such a dictatorial country, from the press.")
			PLAYER_PARTY.SCANDAL += 3.0
		else:
			print(VP_NAME + ": This might be difficult, but I will make sure my media mogul friends never look into this.")
		input("$ Press enter to continue: ")
def formatted_cash():
	# format cash to fit the game style
	return "₩" + str(MONEY*5) + ",000,000"
# print earlygame donations
print()
print(VP_NAME + ": So far, we have earned about " + formatted_cash() + ".")
input("$ Press enter to continue: ")
if 12 > MONEY:
	print(VP_NAME + ": This is bad. We can't rely on media campaigns or bribes to win this election.")
elif 18 > MONEY:
	print(VP_NAME + ": Not great, not terrible.")
	input("$ Press enter to continue: ")
	print(VP_NAME + ": Which leaves room for a miracle.")
else:
	print(VP_NAME + ": ...which is pretty amazing! We have lots to spend.")
input("$ Press enter to continue: ")
print(VP_NAME + ": Any thoughts?")
print()
choice = dialogue((
"Thanks for your help!",
"We need more money to win this election",
"Time to focus on our campaign",
))
if choice == 1:
	if VP == 4:
		print(VP_NAME + ": You're welcome. I'm sure you're already happy you chose me.")
	else:
		print(VP_NAME + ": I had nothing to do with this... I just joined the campaign.")
elif choice == 2:
	if MONEY >= 18:
		print(VP_NAME + ": I'm not sure I follow. We have more than we need already!")
	else:
		print(VP_NAME + ": Agreed.")
elif choice == 3:
	if VP == 1:
		print(VP_NAME + ": That's what I'm here for!")
	else:
		print(VP_NAME + ": Yes, let's.")
input("$ Press enter to continue: ")
print()
# PHASE 1
print("A few weeks later...")
input("$ Press enter to continue: ")
print(VP_NAME + ": The election is in 10 months. Let's call this Phase 1.")
input("$ Press enter to continue: ")
# say the highest chances of winning
highest_archetype = ""
second_place = ""
archetype_max = -100
archetype_opinions = {
"Liberal": PLAYER_PARTY.LIBERAL,
"Nationalist": PLAYER_PARTY.NATIONALIST,
"Conservative": PLAYER_PARTY.CONSERVATIVE,
"Capitalist": PLAYER_PARTY.CAPITALIST,
"Socialist": PLAYER_PARTY.SOCIALIST,
"Communist": PLAYER_PARTY.COMMUNIST,
}
for archetype in list(ARCHETYPES.keys()):
	if archetype_opinions[archetype] >= archetype_max:
		if archetype in available_archetypes:
			second_place = highest_archetype
			highest_archetype = archetype
			archetype_max = archetype_opinions[archetype]
if second_place == "":
	archetype_max = -100
	for archetype in list(ARCHETYPES.keys()):
		if archetype_opinions[archetype] >= archetype_max and archetype != highest_archetype:
			second_place = archetype
if VP != 1:
	print(VP_NAME + ": This may not be my area of expertise, but I would recommend pandering to " + highest_archetype.lower() + "s.")
else:
	print(VP_NAME + ": You would be wise to pander to " + highest_archetype.lower() + "s and " + second_place.lower() + "s. That's my professional opinion.")
input("$ Press enter to continue: ")
print()
# media campaign time
# first, determine other parties' campaign funding:
print(VP_NAME + ": Here's a report on the other parties' media campaigns:")
input("$ Press enter to continue: ")
for party in PARTIES:
	campaign_budget = random.randint(1, 3)
	if party.archetype == "Capitalist":
		campaign_budget = 3
	if campaign_budget == 1:
		print(VP_NAME + ": " + party.name + ", led by " + party.leader + ", is investing in a small campaign.")
		party.CHARISMA += 3.0
	if campaign_budget == 2:
		print(VP_NAME + ": " + party.name + ", led by " + party.leader + ", is investing in a midsize campaign.")
		party.CHARISMA += 5.0
	if campaign_budget == 3:
		print(VP_NAME + ": " + party.name + ", led by " + party.leader + ", is investing in a massive campaign!")
		party.CHARISMA += 7.0
	input("$ Press enter to continue: ")
print(VP_NAME + ": We have our work cut out for us.")
input("$ Press enter to continue: ")
print()
# player media campaign
if 12 > MONEY:
	print(VP_NAME + ": We can start our media campaign, now... though we may have to keep it small.")
else:
	print(VP_NAME + ": Time to get to work on our media campaign! This will heavily affect our public image, so choose carefully.")
input("$ Press enter to continue: ")
if VP != 1: # VP 1 gets a unique, modular media strategy
	print(VP_NAME + ": We can do a small campaign targetting key televisions and radios, or if we have the funds we can do larger, more general campaigns with high-budget editing.")
	input("$ Press enter to continue: ")
	print(VP_NAME + ": What are you leaning towards?")
	available_choices = ["Let's not get involved with these newfangled 'tele-visions'"]
	if MONEY >= 6:
		available_choices.append("Small media campaign, don't go too crazy (₩30,000,000)")
	if MONEY >= 11:
		available_choices.append("Midsized media campaign, let's win this (₩55,000,000)")
	if MONEY >= 18:
		available_choices.append("Huge media campaign, no need for frugality (₩90,000,000)")
	choice = dialogue(available_choices)
	if choice == 1:
		print(VP_NAME + ": They've been around for decades! I'm sure this is the wrong choice...")
		input("$ Press enter to continue: ")
		print(VP_NAME + ": Oh well! If the President says it, so it shall be.")
		PLAYER_PARTY.CHARISMA -= 1.0
	elif choice == 2:
		print(VP_NAME + ": Great! I'll see that this is started right away.")
		MONEY -= 6
		PLAYER_PARTY.CHARISMA += 3.0
	elif choice == 3:
		print(VP_NAME + ": It's great that we can afford this. I'm sure this will greatly help our campaign!")
		MONEY -= 11
		PLAYER_PARTY.CHARISMA += 5.0
	elif choice == 4:
		if VP == 4:
			print(VP_NAME + ": There's always use for frugality... but unspent money is just paper.")
		else:
			print(VP_NAME + ": Well, this certainly worked out well! " + PLAYER_PARTY.motto + "!")
			input("$ Press enter to continue: ")
		PLAYER_PARTY.CHARISMA += 7.0
		MONEY -= 18
	if choice != 1 and VP == 3:
		PLAYER_PARTY.CHARISMA += 1.0
		print(VP_NAME + ": I'll use my contacts to get this through some 'unbiased' papers, as a cherry on top.")
		input("$ Press enter to continue: ")
else: # special media campaign for VP 1
	print(VP_NAME + ": I have some ideas.")
	input("$ Press enter to continue: ")
	if MONEY >= 5: # commercials
		print()
		print(VP_NAME + ": First, our TV campaign. This is a no-brainer.")
		choice = dialogue((
		"The TV arms race is one that we shouldn't fight",
		"Yes, let's start with that (₩25,000,000)",
		))
		if choice == 1:
			print(VP_NAME + ": ...........")
			input("$ Press enter to continue: ")
		elif choice == 2:
			MONEY -= 5
			PLAYER_PARTY.CHARISMA += 3.5
			print()
			print(VP_NAME + ": What should our campaign focus on?")
			choice = dialogue((
			"Maintaining stability and national security",
			"Improving quality of life",
			"Making everyone pay their fair share",
			"Eliminating enemies of the state",
			))
			if choice == 1:
				PLAYER_PARTY.CONSERVATIVE += 2.5
				PLAYER_PARTY.CAPITALIST += 1.0
				PLAYER_PARTY.move_politics(1.5, social=5)
			elif choice == 2:
				PLAYER_PARTY.LIBERAL += 1.5
				PLAYER_PARTY.SOCIALIST += 1.5
				PLAYER_PARTY.move_politics(1.0, social=-10)
			elif choice == 3:
				PLAYER_PARTY.COMMUNIST += 2.0
				PLAYER_PARTY.SOCIALIST += 2.5
				PLAYER_PARTY.CAPITALIST -= 1.5
				PLAYER_PARTY.move_politics(2.5, economy=-10)
			elif choice == 4:
				PLAYER_PARTY.COMMUNIST += 1.5
				PLAYER_PARTY.NATIONALIST += 4.0
				PLAYER_PARTY.LIBERAL -= 3.0
				PLAYER_PARTY.SOCIALIST -= 3.0
				PLAYER_PARTY.CAPITALIST -= 1.0
				PLAYER_PARTY.move_politics(3.0, social=10)
		if MONEY >= 4: # sports
			print()
			print(VP_NAME + ": Now that that's settled, I have a unique opportunity: an ad campaign during the Ultra Cup.")
			choice = dialogue((
			"I hate sports",
			"Great idea! (₩20,000,000)",
			))
			if choice == 1:
				PLAYER_PARTY.CONSERVATIVE += 2.5
				print(VP_NAME + ": Fair enough, " + NAME.split()[0] + ".")
				input("$ Press enter to continue: ")
			elif choice == 2:
				MONEY -= 4
				PLAYER_PARTY.CHARISMA += 3.0
				print(VP_NAME + ": Of course, I'm the one who made it after all.")
				input("$ Press enter to continue: ")
				print()
				print(VP_NAME + ": Now, we only get one commercial. What should it capitalize on: nostalgia or bravado?")
				choice = dialogue((
				"Let's make people nostalgic for the good'oll days",
				"Bravado, of course. We should stand out from the other candidates, especially " + random.choice(PARTIES).leader,
				))
				if choice == 1:
					PLAYER_PARTY.CHARISMA += 1.0
				else:
					PLAYER_PARTY.INDEPENDENT += 3.5
			if MONEY >= 3: # wine
				print()
				print(VP_NAME + ": I have 1 more idea... it's a bit unconventional, and might be a waste of money, but I'll let you be the judge of that.")
				input("$ Press enter to continue: ")
				print(VP_NAME + ": You could buy a vineyard, and sell wine using your name! It will really get vinophiles to respect you.")
				print()
				choice = dialogue((
				"I only drink wine from 18" + str(random.randint(11,99)),
				"I'll drink to that! " + NAME + " Wine, here we come! (₩15,000,000)",
				))
				if choice == 1:
					print(VP_NAME + ": So... no new wine, ever? It was just an idea.")
					input("$ Press enter to continue: ")
				elif choice == 2:
					MONEY -= 3
					PLAYER_PARTY.CHARISMA += 1.0
					PLAYER_PARTY.CLASS1 -= 0.5 # pompous/gaudy
					PLAYER_PARTY.CLASS2 += 1.0
					PLAYER_PARTY.CLASS3 += 2.0
					print(VP_NAME + ": Consider it done.")
					input("$ Press enter to continue: ")
	print(VP_NAME + ": Let's stop it there. We've made some progress.")
	input("$ Press enter to continue: ")
	if PLAYER_PARTY.CHARISMA >= 3.5:
		print(VP_NAME + ": " + NAME + ", a true president of the people!")
		input("$ Press enter to continue: ")



print("That's it for now! This is a work in progress!")
