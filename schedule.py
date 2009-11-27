import urllib, urllib2, re, os.path, sqlite3, string
from datetime import datetime
from BeautifulSoup import BeautifulSoup
from Team import Team

tabnewlineregex = re.compile("\t|\n|&nbsp;(-&nbsp;)?", re.U)


class Schedule():
	def __init__(self):
		self.db = fetch_schedule_data()
		self.dbcursor = self.db.cursor()

	def __del__(self):
		self.db.close()
	
	def next_at(self, htm, atm):
		self.dbcursor.execute("SELECT * FROM games WHERE away=? and home=? and date(date_time) > date(?)", (atm.city, htm.city, "now"))
	        data = self.dbcursor.fetchone()
		if data:
			return ["%s@%s scheduled for %s and broadcasted on %s,XM%s" %(data[1], data[2], data[3].strftime("%x %I:%M %p"), data[4], data[5])]
		else:
			return ["No %s@%s games scheduled" %(atm.city, htm.city)]

	def next(self, tm1, tm2):
		self.dbcursor.execute("SELECT * FROM games WHERE ((away=? and home=?) or (away=? and home=?)) and date(date_time) > date(?)", (tm1.city, tm2.city, tm2.city, tm1.city, "now"))
	        data = self.dbcursor.fetchone()
		if data:
			return ["%s@%s scheduled for %s and broadcasted on %s,XM%s" %(data[1], data[2], data[3].strftime("%x %I:%M %p"), data[4], data[5])]
		else:
			return ["No %s/%s games scheduled" %(tm1.city, tm2.city)]

	def today(self):
		output = ["Today's Games:", "-" * 14]
		self.dbcursor.execute("SELECT * FROM games WHERE date(date_time) = date(?)", ("now",))
		data = self.dbcursor.fetchall()
		for game in data:
			output.append("%s@%s at %s broadcasting on %s,XM%s" %(game[1], game[2], game[3].strftime("%I:%M %p"), game[4], game[5]))

		return output

	def date(self, dt):
		return "TODO:"

	def date_range(self, dt1, dt2):
		return "TODO:"


def fetch_schedule_data():
	"""Returns a db object with the schedule data"""

	if os.path.exists('schedule.db'): # we have a db, return the object
		return sqlite3.connect('schedule.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
	else: 
		return create_db()

def create_db():
	"""create the schedule db, populate it, write it, return it"""

	db = sqlite3.connect('schedule.db')
	dbcursor = db.cursor()
	dbcursor.execute('''create table games 
			(id integer primary key, 
			home text, 
			away text, 
			date_time timestamp, 
			network text, 
			xm text)''')

#	for tr in BeautifulSoup(open('scheduletest.html', 'r').read()).find('table').findAll('tr')[1:]:
	for tr in fetch_html_data().find('table').findAll('tr')[1:]:
		dbcursor.execute("INSERT INTO games values (null, ?, ?, ?, ?, ?)", extract_tds(tr.findAll('td')))

	db.commit()
	return db
	
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

	if tds[4].string == None:
		tds[4] = ''
	else:
		tds[4] = tds[4].string

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

	return tds[1], tds[2], dt, tds[4], tds[5]
	


def fetch_html_data():
	curdate = datetime.now()
	url_data = {}
	url = 'http://www.nhl.com/ice/schedulebyseasonprint.htm'
	url_data['season'] = str(curdate.year) + str(curdate.year + 1) #FIXME check for start of season
	url_data['date'] = curdate.strftime("%d/%m/%Y")
	url_data['gameType'] = '2'
	return BeautifulSoup(urllib2.urlopen(url + '?' + urllib.urlencode(url_data)).read())


if __name__ == "__main__":

	sched = Schedule()
#	for blah in sched.dbcursor.execute("select * from games").fetchall():
#		print blah
	away = Team('mon')
	home = Team('tam')
	print sched.today()
#	print sched.next(away, home)

	
