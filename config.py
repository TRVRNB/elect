# config file for elect
COUNTRY = "Wrathia" # name of the country
PARTY_COUNT = 3 # how many parties there should be, excluding the player
TOLERANCE = 2.5 # how much opinion should be lost per point on the political compass apart

VP_NAMES = ("Lucian Populise", "Chloe Kandaggier", "Patricia Raymonds", "Saul Greene") # they always go in this order

ARCHETYPES = { # actual parties will vary
"Liberal": (2, -6), # centrist/freedom/justice
"Nationalist": (3, 9), # right-wing/populist/reactionary/racist
"Conservative": (0, 4), # centrist/traditionalist
"Capitalist": (6, 0), # pro-west/socially neutral
"Socialist": (-4, -6), # liberal/planned economy
"Communist": (-9, 4), # pro-east/illiberal
}

ADJECTIVE = { # adjectives for random party names
"Liberal": ("Free", "Social", "Democratic", "Liberal", "Civil", "Green", "Personal"),
"Nationalist": ("United", "Liberated", "National", "Strong", "Racist"), 
"Conservative": ("United", "Old", "Traditional", "Moderate", "Geriatric", "Conventional"), 
"Capitalist": ("Capitalist", "Western", "Wealthy", "Open", "Economic", "Oligarchic"),
"Socialist": ("Social", "Socialist", "Social", "Civil", "Blue", "Woke", "Idealist"),
"Communist": ("People's", "Worker's", "Communist", "Tankie", "Red"),
}

NOUN = { # nouns for random party names
"Liberal": ("Freedom", "Liberty", "Justice", "Equality", "Reform", "Democracy", "Rights", "Soy"),
"Nationalist": ("Restoration", "Front", "Strength", "Unity", "Nationalism", "Nationality", "Power", "Strength"),
"Conservative": ("Guard", "Continuity", "Engine", "World", "Land", "Constitution", COUNTRY),
"Capitalist": ("Trade", "West", "Liberal", "Cash", "Money", "Bank", "Economy", "Privatization"),
"Socialist": ("Equity", "Labor", "Welfare", "Life", "Health", "Education", "Ideal", "Socialism"),
"Communist": ("Revolution", "Communism", "Tax", "Standards", "State", "Nationalization", "Comrade", "Menace", "Scare"),
}

MOTTOS = { # party mottos, these do not have ending punctuation so they can be spoken in different contexts
"Liberal": ("Freedom, liberty, equality for all", "Life, liberty, pursuit of happiness", "Democracy, above all", "Civil rights and liberty for all", "Peace and harmony", "We choose our own path"),
"Nationalist": ("Above all, one", "One people, one nation, one identity", "We are our country, our country are we", "National pride, above all", "A strong, just nation", "United we stand, divided we fall"),
"Conservative": ("The past brings stability", "Stability is progress", "Constitution, above all", "Rational change", "Stand on our own as we always have", "Our land, your land, " + COUNTRY, "The way of old is the way of gold"),
"Capitalist": ("The West is peace", "Freedom through wealth", "Failed regulation is poverty", "Supply and demand", "Liberty, above all", "Markets create wealth"),
"Socialist": ("Equity and welfare for all", "Democracy, welfare, peace", "Voice of the unheard", "Equity, above all", "Rights beyond paper", "Down with oppression"),
"Communist": ("Death to the West", "The East will bring life", "Communism will bury you", "Revolution is inevitable", "We are the will of the people", "Statism, above all", "Morning shall come"),
}
