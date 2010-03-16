#! /usr/bin/env python

import sys
from optparse import OptionParser
from schedule import Schedule
from datetime import date, datetime

def schedule(option, opt_str, value, parser):
	sched = Schedule()
	schedate = datetime.strptime(value, '%m/%d/%Y')

	print "Games scheduled for %s:" %schedate.strftime("%m/%d/%Y")
	for match in sched.date(schedate):
		print match.without_date()

def today(option, opt_str, value, parser):
	sched = Schedule()
	print "Games scheduled for %s:" %date.today().strftime("%m/%d/%Y")
	for match in sched.date(date.today()):
		print match.without_date()



if __name__ == "__main__":
	nhlparse = OptionParser(usage = "usage: %prog [command] [arg]")
	nhlparse.add_option(
			"-s", "--schedule",
			help = "takes a date of the form m/d/y.  defaults to current",
			action = "callback",
			type = "string",
			callback = schedule)
	nhlparse.add_option(
			"-t", "--today",
			help = "todays scheduled games",
			action = "callback",
			type = "string",
			nargs = 0,
			callback = today)
	nhlparse.add_option(
			"-n", "--next",
			help = "takes two teams of the form abrv@abrv or abrv/arbv")


	(options, args) = nhlparse.parse_args()

