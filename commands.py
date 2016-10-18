import platform
import sys


def host_command(irc, config, requester, message):
    irc.send(config["irccommands"]["privmsg"].format(requester, str(platform.platform())))

def join_command(irc, config, requester, message):
    messageParts = message.split()
    if (len(messageParts) == 1 and messageParts[0].startswith("#")):
        irc.send(config["irccommands"]["join"].format(message))

def kill_command(irc, config, requester, message):
    irc.send(config["irccommands"]["quit"].format(config["strings"]["quitmessage"]))
    print "\n"
    sys.exit()

def part_command(irc, config, requester, message):
    messageParts = message.split()
    if (len(messageParts) == 1 and messageParts[0].startswith("#")):
        irc.send(config["irccommands"]["part"].format(messageParts[0]))