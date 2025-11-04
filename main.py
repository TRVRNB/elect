import random

COUNTRY = "Wrathia"

ARCHETYPES = { # actual parties will vary
"Liberal": (2, -6), # centrist/freedom/justice
"Nationalist": (3, 9), # right-wing/populist/reactionary/racist
"Conservative": (0, 4), # centrist/traditionalist
"Capitalist": (6, 0), # pro-west/socially neutral
"Socialist": (-4, -6), # liberal/planned economy
"Communist": (-8, 5), # pro-east/illiberal
}

ADJECTIVE = { # adjectives for random party names
"Liberal": ("Free", "Social", "Democratic", "Liberal", "Civil", "Green"),
"Nationalist": ("United", "Unified", "National", "Strong", "Racist"), 
"Conservative": ("United", "Old", "Traditional", "Moderate"), 
"Capitalist": ("Capitalist", "Western", "Wealthy", "Open", "Economic"),
"Socialist": ("Social", "Socialist", "Social", "Civil", "Blue", "Woke"),
"Communist": ("People's", "Worker's", "Communist", "Comrade", "Red"),
}

NOUN = { # mouns for random party names
"Liberal": ("Freedom", "Liberty", "Justice", "Equality", "Reform", "Democracy", "Rights"),
"Nationalist": ("Restoration", "Front", "Strength", "Unity", "Nationalism", "Nationality"),
"Conservative": ("Guard", "Continuity", "Engine", "World", "Land", "Constitution", COUNTRY),
"Capitalist": ("Trade", "West", "Liberal", "Cash", "Money", "Bank", "Economy", "Privatization"),
"Socialist": ("Equity", "Labor", "Welfare", "Life", "Health", "Education", "Ideal"),
"Communist": ("Revolution", "Communism", "Tax", "Standard", "State", "Nationalization"),
}

MOTTOS = { # party mottos, these do not have ending punctuation so they can be spoken in different contexts
"Liberal": ("Freedom, liberty, equality for all", "Life, liberty, pursuit of happiness", "Democracy, above all", "Civil rights and liberty for all", "Peace and harmony"),
"Nationalist": ("Above all, one", "One people, one nation, one identity", "We are our country, our country is us", "National pride, above all", "A strong, just nation"),
"Conservative": ("The past brings stability", "Stability is progress", "Constitution, above all", "Rational change", "Stand on our own"),
"Capitalist": ("The west is peace", "Wealth is happiness", "Poverty is chaos", "Supply and demand", "Regulation fails", "Liberty, above all"),
"Socialist": ("Equity and welfare for all", "Democracy, welfare, peace", "Voice of the unheard", "Equity, above all", "Rights beyond paper"),
"Communist": ("Death to the west", "The east will bring life", "Communism will bury you", "Revolution is inevitable", "We are the will of the people", "Statism, above all"),
}

PARTIES = []

class Party():
	# a political party
	def __init__(self, archetype, name=None, leader=None, motto=None):
		self.archetype = archetype # define this beforehand
		self.economy = ARCHETYPES[archetype][0] + random.randint(-3, 3)
		self.social = ARCHETYPES[archetype][1] + random.randint(-2, 2)
		# get motto
		self.motto = motto
		if motto == None:
			self.motto = random.choice(MOTTOS[archetype])
		# get name
		self.name = name
		if name == None:
			self.name = self.generate_name()
		# now, get initials
		self.initials = ""
		names = self.name.split()
		for name in names:
			if name[0] == name[0].upper():
				self.initials += name[0]
		# now, generate a party leader (running for president)
		self.leader = leader
		if leader == None:
			self.leader = self.generate_party_leader()	
		# effects that change over the span of the game
		self.charisma = 0
		self.scandal = 0

	def generate_name(self):
		# return a name based on the political archetype
		archetype = self.archetype
		return random.choice([
		str(random.choice(ADJECTIVE[archetype]) + " Party of " + COUNTRY),
		str(random.choice(NOUN[archetype]) + " and " + random.choice(NOUN[archetype]) + " Party"),
		str(random.choice(NOUN[archetype]) + " " + random.choice(NOUN[archetype]) + " Party"),
		str(random.choice(ADJECTIVE[archetype]) + " Party"),
		str(random.choice(ADJECTIVE[archetype]) + " " + random.choice(NOUN[archetype]) + " and " + random.choice(NOUN[archetype]) + " Party"),
		str(random.choice(ADJECTIVE[archetype]) + " " + random.choice(NOUN[archetype]) + " Party"),
		str(random.choice(ADJECTIVE[archetype]) + " " + random.choice(NOUN[archetype]) + " Party"),
		str(COUNTRY + " " + random.choice(ADJECTIVE[archetype]) + " Party"),
		str(random.choice(ADJECTIVE[archetype]) + " " + random.choice(NOUN[archetype])),
		])
		
	def generate_party_leader(self):
		# generates a name for the party's leader
		first = random.choice(("Marcel", "Frens", "John", "Anita", "Lucian", "Alvin", "Kesaro", "Lileas", "Nia", "Gloria", "George", "Peter", "Monty", "Walter", "Remus", "Victor", "Alma", "Emerich", "Leon", "Patricio", "Serge", "Clark", "Manual", "Kennedy"))
		last = random.choice(("Jabĺonski", "Johnson", "Ricter", "Smolak", "Python", "Hegel", "Kibener", "Smith", "Antony", "Wisci", "Washington", "Starmer", "Monsieur", "Capon", "Rayne", "Macron"))
		if random.randint(1, 7) == 1:
			last = {"Liberal": "Clavin", "Nationalist": "White", "Conservative": "Tory", "Capitalist": "Tusk", "Socialist": "Marx", "Communist": "Saltin"}[self.archetype]
		return first + " " + last
	

class Voter():
	# a voter who looks through the list of parties
	def __init__(self, economy=0, social=0, turnout=0.5, independent=False):
		self.economy = economy # negative: socialism, positive: capitalism
		self.economy += random.randint(-4, 4)
		self.social = social # negative: liberal, positive: conservative
		self.social += random.randint(-3, 3)
		self.social_class = random.randint(1, 3) # poor is more likely to vote for socialist, rich is more likely to vote for capitalist
		self.minority = random.randint(1, 6) == 1 # less likely to vote for nationalist policies
		self.turnout = turnout + random.uniform(-0.5, 0.5) # total chance to vote, they will always vote if it is above 1.0
		self.independent = independent # independents support anti-partisan policies

intro = "Welcome to " + COUNTRY + "! This is the 19" + str(38 + 4 * random.randint(1, 6)) + " General Election, and you are running for president. You will create and name a new party, determine its stance on several divisive political topics, and create a campaign!"
# there will also be a political debate and a speech that heavily affect the charisma modifier
# plus, chances to fabricate scandals, and a few scandals of your own to deal with
print(intro)
input("$ Press enter to continue: ")
print()

# create parties
available_archetypes = list(ARCHETYPES.keys())
print("Here are this election's leading parties:")
for _ in range(random.randint(2, 4)):
	print("—")
	archetype = random.choice(available_archetypes)
	party = Party(archetype)
	available_archetypes.remove(archetype)
	PARTIES.append(party)
	print(party.name + " (" + party.initials + ")")
	print("Leader: " + party.leader + ", Policies: " + party.archetype)
	print(party.motto + ".")
print("—")
input("$ Press enter to continue: ")
print()

# voter demographics
input("$ Now, for the voter demographics:")
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
# now, create a new party
