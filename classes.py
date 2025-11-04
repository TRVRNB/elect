import random, math, config

COUNTRY = config.COUNTRY
ARCHETYPES = config.ARCHETYPES
NOUN = config.NOUN
ADJECTIVE = config.ADJECTIVE
MOTTOS = config.MOTTOS

class Party():
	# a political party
	def __init__(self, archetype, name=None, leader=None, motto=None, incumbent=False):
		self.archetype = archetype # define this beforehand
		self.economy = 0
		self.social = 0
		if archetype != "New Party":
			self.economy += ARCHETYPES[archetype][0] + random.randint(-3, 3)
			self.social += ARCHETYPES[archetype][1] + random.randint(-2, 2)
		self.incumbent = incumbent
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
		self.get_default_opinions()

	def generate_name(self):
		# return a name based on the political archetype
		archetype = self.archetype
		return random.choice([
		str(random.choice(ADJECTIVE[archetype]) + " Party of " + COUNTRY),
		str(random.choice(ADJECTIVE[archetype]) + " " + COUNTRY),
		str(random.choice(NOUN[archetype]) + " and " + random.choice(NOUN[archetype]) + " Party"),
		str(random.choice(ADJECTIVE[archetype]) + " " + random.choice(NOUN[archetype]) + " and " + random.choice(NOUN[archetype]) + " Party"),
		str(random.choice(ADJECTIVE[archetype]) + " Party"),
		str(random.choice(NOUN[archetype]) + " Party"),
		str(random.choice(ADJECTIVE[archetype]) + " " + random.choice(NOUN[archetype]) + " and " + random.choice(NOUN[archetype]) + " Party"),
		str(random.choice(ADJECTIVE[archetype]) + " " + random.choice(NOUN[archetype]) + " Party"),
		str(random.choice(ADJECTIVE[archetype]) + " " + random.choice(NOUN[archetype]) + " Party"),
		str(COUNTRY + " " + random.choice(ADJECTIVE[archetype]) + " Party"),
		str(random.choice(ADJECTIVE[archetype]) + " " + random.choice(NOUN[archetype])),
		])
	
	def get_default_opinions(self):
		# these change throughout the game
		if self.archetype == "New Party":
			self.LIBERAL = 0
			self.NATIONALIST = 0
			self.CONSERVATIVE = 0
			self.CAPITALIST = 0
			self.SOCIALIST = 0
			self.COMMUNIST = 0
			self.INDEPENDENT = 5 # independents will always start out liking player parties
			return
		self.LIBERAL = 16.0 - config.TOLERANCE*self.get_political_difference(ARCHETYPES["Liberal"])
		self.NATIONALIST = 10.0 - config.TOLERANCE*self.get_political_difference(ARCHETYPES["Nationalist"])
		self.CONSERVATIVE = 14.0 - config.TOLERANCE*self.get_political_difference(ARCHETYPES["Conservative"])
		self.CAPITALIST = 14.0 - config.TOLERANCE*self.get_political_difference(ARCHETYPES["Capitalist"])
		self.SOCIALIST = 12.0 - config.TOLERANCE*self.get_political_difference(ARCHETYPES["Socialist"])
		self.COMMUNIST = 8.0 - config.TOLERANCE*self.get_political_difference(ARCHETYPES["Communist"])
		self.INDEPENDENT = -config.TOLERANCE*self.get_political_difference((0, 0))
	
	def get_political_difference(self, p):
		# gets the difference between 2 points
		return  math.sqrt((p[0] - self.economy)**2 + (p[1] - self.social)**2)
		
	
	def generate_party_leader(self):
		# generates a name for the party's leader
		first = random.choice(("Marcel", "Frens", "John", "Anita", "Lucian", "Alvin", "Kesaro", "Lileas", "Nia", "Gloria", "George", "Peter", "Monty", "Walter", "Remus", "Victor", "Alma", "Emerich", "Leon", "Patricio", "Serge", "Clark", "Manual", "Kennedy"))
		last = random.choice(("Jabĺonski", "Johnson", "Ricter", "Smolak", "Python", "Hegel", "Kibener", "Smith", "Antony", "Wisci", "Washington", "Starmer", "Monsieur", "Capon", "Rayne", "Macron"))
		if random.randint(1, 7) == 1:
			last = {"Liberal": "Clavin", "Nationalist": "White", "Conservative": "Tory", "Capitalist": "Tusk", "Socialist": "Marx", "Communist": "Saltin"}[self.archetype]
		return first + " " + last
	
	def move_politics(intensity=1.0, economy=None, social=None):
		# move the politics to a certain point
		if economy != none:
			if self.economy > economy + intensity:
				self.economy -= intensity
			elif self.economy < economy - intensity:
				self.economy += intensity
			else:
				self.economy = economy
		if social != none:
			if self.social > social + intensity:
				self.social -= intensity
			elif self.social < social - intensity:
				self.social += intensity
			else:
				self.social = social

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
		self.independent = independent # independents support anti-partisanism
	
