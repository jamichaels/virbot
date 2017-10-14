import re
import socket
import sys
import json
import utility

from commands import VirBotCommands
from logtype import VirBotLogType
from numerics import VirBotNumerics


def main(argv):
    sentUser = False
    sentNick = False

    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((config["server"]["name"], config["server"]["port"]))

    botCommands = VirBotCommands(irc, config)
    botNumerics = VirBotNumerics(irc, config)

    try:
        while True:
            data = irc.recv(2048)
            if len(data) <= 0:
                continue

            if config["debugmode"]:
                print data

            if data.startswith('ERROR') == True:
                #TODO: Add proper error output and reconnection if configured
                utility.consoleMessage(VirBotLogType.ERROR, data)
                sys.exit()

            if data.find('PING') != -1 and data.find(u"\u0001PING") == -1:
                irc.send(config["irccommands"]["pong"].format(data.split()[1]))
                utility.consoleMessage(VirBotLogType.SENT, "PONG to SERVER" + " (" + data.split()[1][1:] + ")")
                continue

            if data.find(u"\u0001PING") != -1:
                requester = utility.getRequester(True, data)
                if requester != None:
                    pingindex = data.index(u"\u0001PING")
                    pingreply = data[pingindex:]
                    pingreply = pingreply.replace("\r\n", "")
                    irc.send(u"NOTICE " + requester + u" :" + pingreply + u"\u0001\n")
                    utility.consoleMessage(VirBotLogType.SENT, "PONG to " + requester + " (" + pingreply[6:] + ")")
                    continue

            if sentUser == False:
                irc.send(config["irccommands"]["user"].format(nick, nick, nick, realname))
                sentUser = True
                utility.consoleMessage(VirBotLogType.SENT, "USER")
                continue

            if sentUser and sentNick == False:
                irc.send(config["irccommands"]["nick"].format(nick))
                sentNick = True
                utility.consoleMessage(VirBotLogType.SENT, "NICK" + " (" + nick + ")")
                continue

            for lineText in data.split("\r\n"):
                messageMatches = re.search("(:[\\w\\.]+\\s)(\\d{3}\\s|[A-Z]+\\s)([\\w]+\\s)(.+)", lineText)
                if messageMatches:
                    host = messageMatches.group(1)[1:-1]
                    numeric = messageMatches.group(2)[:-1]
                    user = messageMatches.group(3)[:-1]
                    message = messageMatches.group(4)[1:]
                    botNumerics.process_botnumeric(host, numeric, user, message)
                    continue

                messageMatches = re.search("(:.+@.+\\s)([A-Z]+\\s)([\\w#]+\\s)(:?.+)", lineText)
                if messageMatches:
                    sender = messageMatches.group(1)[1:-1]
                    command = messageMatches.group(2)[:-1]
                    receiver = messageMatches.group(3)[:-1]
                    message = messageMatches.group(4)
                    message = message[1:] if message.startswith(":") else message
                    requester = utility.getRequester(False, sender) if receiver == nick else receiver
                    commandLookup = message.split()[0]
                    botCommands.process_botcommand(sender, requester, commandLookup, message)
                    continue

    except KeyboardInterrupt:
        botCommands.kill_command(None, None)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')

    with open('config.json', 'r') as configFile:
        config = json.load(configFile)

    nick = config["nickname"]
    realname = config["realname"]

    main(sys.argv[1:])
