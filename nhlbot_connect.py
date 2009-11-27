#! /usr/bin/env python

import irclib
import sys
import NHLBot



if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage: nhlbot <server[:port]> <channel>"
		sys.exit(1)

	firstarg = sys.argv[1].split(":", 1)
	server = firstarg[0]
	if len(firstarg) == 2:
		try:
			port = int(firstarg[1])
		except ValueError:
			print "Error: Bad Port."
			sys.exit(1)
	else:
		port = 6667

	channel = sys.argv[2]

	nhlbot = NHLBot.NHLBot(server, port, channel)
	nhlbot.start()

