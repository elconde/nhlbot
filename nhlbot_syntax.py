from pyparsing import *

team_abbrv = oneOf("bos buf bos buf cgy chi det edm car los mon dal njd nyi nyr phi pit col stl tor van was pho sjs ott tam ana fla atl cbs min nsh") + WordEnd()
team_abbrvs = Group(OneOrMore(team_abbrv)).setResultsName("teams")
division = oneOf("atlantic a pacific p central c northwest nw northeast ne southeast se") + WordEnd()
divisions = Group(OneOrMore(division)).setResultsName("divisions")
conf = oneOf("w west western e east eastern").setResultsName("conf") + WordEnd()
digits = "0123456789"
number = Word(digits)
date = number + Literal("/").suppress() + number + Literal("/").suppress() + number

standings_args = conf ^ divisions ^ team_abbrvs 
standings_command = Literal("standings") + Optional(standings_args)

next_args = team_abbrv.setResultsName("team1") + Or(Literal("@").setResultsName("at") + Literal("/")) + team_abbrv.setResultsName("team2") + WordEnd()
next_command = Literal("next") + next_args

schedule_args = date
schedule_command = Literal("games") + Optional(schedule_args)

exit_command = oneOf("exit quit q leave die") + WordEnd()
help_command = oneOf("? help") + WordEnd()


output_flag = Literal("#") + WordEnd()

command = (standings_command ^ next_command ^ exit_command ^ help_command) + Optional(output_flag).setResultsName("output_flag") + StringEnd()

if __name__ =="__main__":

	data = command.parseString("next tam / nyr #")

	print data


#	except ParseException, err:
#		print err.line
#		print " " * (err.column - 3) + "^"
#		print err

