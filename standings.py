import urllib, urllib2, html5lib, re
from BeautifulSoup import BeautifulSoup
from Team import Team

tabnewlineregex = re.compile("\t|\n|&nbsp;-&nbsp;", re.U)

def standings(cmd):
	stand = get_league_standings()
	output = []

	if cmd.divisions:
		divs = get_division_standings(stand, cmd.divisions.asList())
		for div in divs:
			for team in div:
				output.append("{name: <25} {gp: >2} {win: >2}".format(name=team.name,  gp=team.get_stat('gp'), win=team.get_stat('go')))
	if cmd.teams:
		for team in get_team_standings(stand, cmd.teams.asList()):
			output.append("{name: <30} ".format(name=team.name)a)

	return output


#outputlines.append("{blnk: <2} {blnk: <25} {div: <3} {gp: >2} {win: >2} {loss: >2} {ot: >2} {pts: >3} {gf: >3} {ga: >3} {home: >8} {away: >8} {l10: >6} {streak: >7}".format(blnk="", div=div, gp=gp, win=win, loss=loss, ot=ot, pts=ot, gf=gf, ga=ga, home=home, away=away, l10=l10, streak=streak))

def format_stats(statdict):
	return "{gp: >2} {win: >2} {loss: >2} {ot: >2} {pts: >3} {gf: >3} {ga: >3} {home: >8} {away: >8} {l10: >6} {streak: >3}".format(
			gp=team.get_stat('gp'),
			win=team.get_stat('win'),
			loss=team.get_stat('loss'),
			ot=team.get_stat('ot'),
			pts=team.get_stat('pts'),
			gf=team.get_stat('gf'),
			ga=team.get_stat('ga'),
			home=team.get_stat('home'),
			away=team.get_stat('away'),
			l10=team.get_stat('l10'),
			streak=team.get_stat('streak'))
def stats_header():
	return "{gp: >2} {win: >2} {loss: >2} {ot: >2} {pts: >3} {gf: >3} {ga: >3} {home: >8} {away: >8} {l10: >6} {streak: >3}".format(
			gp='GP', win='WIN', loss='LOSS', ot='OT', pts='PTS', gf='GF', ga='GA', home='HOME', away='AWAY', l10='L10', streak='STREAK')
	


def get_league_standings():
	"""Returns the standings and stats for the league"""

	standings = [{} for x in range(30)]

	for tr in fetch_standings_data().find('table').findAll('tr'):
		# extract and sanitize the data
		place, team, div, gp, win, loss, ot, pts, gf, ga, home, away, l10, streak = map(extract_and_sanatize, tr.findAll('td'))

		if place != "None": # we aren't the header
			standings[int(place) - 1] = Team(team, {'div' : div, 'gp' : gp, 'win' : win, 'loss': loss, 'ot' : ot, 'pts' : pts, 'gf' : gf, 'ga' : ga, 'home' : home, 'away' : away, 'l10' : l10, 'streak' : streak})

	return standings

def get_division_standings(standings, divs):

	divslist = []
	for div in divs:
		teamlist = []
		for team in standings:
			if team.get_stat('div') == div:
				teamlist.append(team)
		divslist.append(teamlist)
		
	return divslist


def get_team_standings(standings, teams):
	teamlist = []
	for team in standings:
		if team.abbrv in teams:
			teamlist.append(team)

	return teamlist

def fetch_standings_data(type='LEA'):
	url_data = {}
	url = 'http://www.nhl.com/ice/standingsprint.htm'
	url_data['season'] = '20092010'
	url_data['type'] = type

	return BeautifulSoup(urllib2.urlopen(url + '?' + urllib.urlencode(url_data)).read())


def extract_and_sanatize(d):
	clinch = d.find(id="clincher")
	if clinch:
		return  str(re.sub(tabnewlineregex, "", unicode(clinch.string).encode("utf-8"))[1:])
	else:
		return unicode(d.string).encode('utf-8')


if __name__ == "__main__":

	print get_team_standings(get_league_standings(), ['cgy'])

#	test.division("divisions")
