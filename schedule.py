import Logger,logging
logger=logging.getLogger()

import urllib, urllib2, re, os.path, sqlite3, string
from datetime import datetime
from BeautifulSoup import BeautifulSoup
from Team import Team

tabnewlineregex = re.compile("\t|\n|&nbsp;(-&nbsp;)?", re.U)
finalregex = re.compile('.*FINAL.*span.*\(([0-9]+)\).*span.*\(([0-9]+)\)')

class Schedule():
	def __init__(self):
		self.db = fetch_schedule_data()
		self.dbcursor = self.db.cursor()

	def __del__(self):
		self.db.close()
	
	def next_at(self, htm, atm):
		self.dbcursor.execute("SELECT * FROM games WHERE away=? AND home=? eAND date(date_time) > date(?)", (atm.city, htm.city, "\'now\'"))
	        data = self.dbcursor.fetchone()
		if data:
			return ["%s@%s scheduled for %s and broadcasted on %s" %(data[1], data[2], data[3].strftime("%x %I:%M %p"), data[4])]
		else:
			return ["No %s@%s games scheduled" %(atm.city, htm.city)]

	def next(self, tm1, tm2):
		self.dbcursor.execute("SELECT * FROM games WHERE ((away=? and home=?) OR (away=? AND home=?)) AND date(date_time) > date(?)", (tm1.city, tm2.city, tm2.city, tm1.city, "now"))
	        data = self.dbcursor.fetchone()
		if data:
			return ["%s@%s scheduled for %s and broadcasted on %s" %(data[1], data[2], data[3].strftime("%x %I:%M %p"), data[4])]
		else:
			return ["No %s/%s games scheduled" %(tm1.city, tm2.city)]

	def today(self):
		output = ["Today's games:", "-" * 14]
		self.dbcursor.execute("SELECT * FROM games WHERE date(date_time) = date(?)", ("\'now\'",))
		data = self.dbcursor.fetchall()

		for game in data:
			output.append("%s@%s at %s broadcasting on %s" %(game[1], game[2], game[3].strftime("%d %I:%M %p"), game[4]))


		return output

	def date(self, dt):
		output = ["Games scheduled for %s:" %(dt.strftime("%x")), "-" * 30]
		self.dbcursor.execute("SELECT * FROM games WHERE date(date_time) = date(?)", (dt,))
		data = self.dbcursor.fetchall()
		for game in data:
			output.append("%s@%s at %s broadcasting on %s" %(game[1], game[2], game[3].strftime("%I:%M %p"), game[4]))

		return output

	def date_range(self, dt1, dt2):
		output = ["Games schedule for %s-%s:" %(dt1.strftime("%x"), dt2.strftime("%x")), "-" * 36]
		self.dbcursor.execute("SELECT * FROM games WHERE date(date_time) BETWEEN date(?) AND date(?)", (dt1, dt2))
		data = self.dbcursor.fetchall()
		for game in data:
			output.append("%s@s at %s broadcasting on %s" %(game[1], game[2], game[3].strftime("%I:%M %p"), game[4]))

		return output

def fetch_schedule_data():
	"""Returns a db object with the schedule data"""

	if not os.path.exists('schedule.db'): 
		create_db()

	return sqlite3.connect('schedule.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

def create_db():
	"""create the schedule db, populate it, write it, return it"""
	logger.info('Creating database')
	db = sqlite3.connect('schedule.db')
	dbcursor = db.cursor()
	dbcursor.execute('''create table games 
			(id integer primary key, 
			home text, 
			away text, 
			date_time timestamp,
			result text,
			network text)''')

	for tr in fetch_html_data().find('table').findAll('tr')[1:]:	
		home,away,date_time,network = extract_tds(tr.findAll('td'))
		# The column displays the results for past games and the networks for
		# future games.
		if network.upper().startswith('RESULT'):
			result = network[7:]
			network = ''
		else:
			result = ''
		dbcursor.execute("INSERT INTO games values (null, ?, ?, ?, ?, ?)", (home,away,date_time,result,network))

	db.commit()
	db.close()
	
def extract_tds(tds):
	tds[0] = re.sub("&nbsp;", " ", tds[0].string)

	if tds[1].a == None: # probably olympic team
		tds[1] = tds[1].div.string
	else:
		tds[1] = tds[1].a.string


	if tds[2].a == None: # probably olmpic team
		tds[2] = tds[2].div.string
	else:
		tds[2] = tds[2].a.string

	if tds[3].findNext('div').string == None:
		tds[3] = u'12:00 AM ET'
	else:
		tds[3] = tds[3].findNext('div').string

	contents = str(tds[4].contents)
	match = finalregex.match(contents)
	if not match: tds[4] = tds[4].string
	else:
		tds[4] = 'RESULT %s-%s' % match.groups()
		
	
	
	if tds[5].string == None:
		tds[5] = ''
	else:
		tds[5] = tds[5].string
	
	# clean up data and return

	tds = map(lambda x: re.sub(tabnewlineregex, "", x), tds)
	tds[1] = string.capwords(tds[1], " ")
	tds[2] = string.capwords(tds[2], " ")


	# new york special case need to capitalize the Y
	if "Ny" in tds[1]:
		tds[1] = tds[1].replace("y", "Y")
	if "Ny" in tds[2]:
		tds[2] = tds[2].replace("y", "Y")

	dt = datetime.strptime(tds[0] + " " + tds[3][:-3], "%a %b %d, %Y %I:%M %p")

	return tds[1], tds[2], dt, tds[4] + tds[5]
	


def fetch_html_data():
	return BeautifulSoup(urllib2.urlopen('http://www.nhl.com/ice/schedulebyseasonprint.htm').read())


if __name__ == "__main__":
	os.unlink('schedule.db')
	logger.setLevel(logging.DEBUG)
	sched = Schedule()
	for result in sched.dbcursor.execute('select date_time,home,away,result from games where result != ""').fetchall():
		print result
	#for blah in sched.dbcursor.execute("select * from games").fetchall():
	#	print blah
	njd = Team('njd')
	tam = Team('tam')
	print sched.next(njd, tam)
	#print sched.today()
#	print sched.date(datetime.strptime("11/29/09", "%m/%d/%y"))
