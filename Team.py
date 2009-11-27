abbrv_lookup = {
	'bos' : ['Boston', 'Bruins'],
	'buf' : ['Buffalo', ' Sabres'],
	'cgy' : ['Calgary', 'Flames'],
	'chi' : ['Chicago', 'Blackhawks'],
	'det' : ['Detroits', 'Red Wings'],
	'edm' : ['Edmonton', 'Oilers'],
	'car' : ['Carolina', 'Hurricanes'],
	'los' : ['Los Angeles', 'Kings'],
	'mon' : ['Montreal', 'Canadiens'],
#	'mon' : [u'Montr\xc3\xa9al', 'Canadiens'],
	'dal' : ['Dallas', 'Stars'],
	'njd' : ['New Jersey', 'Devils'],
	'nyr' : ['NY Rangers', 'Rangers'],
	'nyi' : ['NY Islanders', 'Islanders'],
	'phi' : ['Philadelphia', 'Flyers'],
	'pit' : ['Pittsburgh', 'Penguins'],
	'col' : ['Colorado', 'Avalanche'],
	'stl' : ['St Loius', 'Blues'],
	'tor' : ['Toronto', 'Maple Leafs'],
	'van' : ['Vancouver', 'Canucks'],
	'was' : ['Washington', 'Capitals'],
	'pho' : ['Phoenix', 'Coyotes '],
	'sjs' : ['San Jose', 'Sharks'],
	'ott' : ['Ottawa', 'Senators'],
	'tam' : ['Tampa Bay', 'Lightning'],
	'ana' : ['Anaheim', 'Ducks'],
	'fla' : ['Florida', 'Panthers'],
	'atl' : ['Atlanta', 'Thrashers'],
	'cbs' : ['Columbus', 'Blue Jackets'],
	'min' : ['Minnesota', 'Wild'],
	'nsh' : ['Nashville', 'Predators']}


class Team:
	def __init__(self, team_abbrv):
		self.city = abbrv_lookup[team_abbrv][0]
		self.name = abbrv_lookup[team_abbrv][1]
		self.abbrv = team_abbrv

	def __repr__(self):
		return self.name
