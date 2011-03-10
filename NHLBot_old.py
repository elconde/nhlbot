from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr
from nhlbot_syntax import *
from handle_commands import handle_commands
import sys, re

nhlbotregex = re.compile("^nhlbot (?P<command>.*$)")

class NHLBot(SingleServerIRCBot):
	def __init__(self, server, port, channel):
		nick = "NHLbot"
		SingleServerIRCBot.__init__(self, [(server, port)], nick, nick)
		self.channel = "#" + channel


	def on_nicknameinuse(self, c, e):
		c.nick(c.get_nickname() + "_")

	def on_welcome(self, c, e):
		c.join(self.channel)

	def on_join(self, c, e):
		c.notice(self.channel, "nhlbot is running and waiting for commands")

	def on_privmsg(self, c, e):
		self.do_command(e, e.arguments()[0])

	def on_pubmsg(self, c, e):
		args = e.arguments()[0]
		nick = nm_to_n(e.source())
		match = nhlbotregex.match(args)
		if match:
			try:
				self.send_it(e, match.groupdict()['command'])
			except ParseException, err:
				c.notice(nick, "Sorry, I didn't understand: %s" %err.line)
				c.notice(nick, "                           " + " " * int(err.column) + "^")
				c.notice(nick, err)


		return

	def send_it(self, e, cmd):
		recvr = nm_to_n(e.source())
		c = self.connection

		cmd_data = process_command(command.parseString(cmd))

		if cmd_data[-1] == output_flag
			recvr = self.channel

		if cmd_data[0] == exit_command:
			self.disconnect("NHLbot is shutting down")
			sys.exit()
		for line in cmd_data[0]
			c.privmsg(recvr, line)	
		
		return

