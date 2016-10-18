import commands
import numerics
import re
import socket
import sys
import json
import hues

def getRequester(usesPrefix, text):
    searchPattern = "(?<=:).+(?=!)" if usesPrefix else ".+(?=!)"
    requestMatches = re.search(searchPattern, text, re.I)
    if requestMatches:
        return str(requestMatches.group())
    return ""

def processServerMessage(irc, host, numeric, user, message):
    hues.log(hues.huestr("Server: " + message).blue.bold.colorized)

    if config["numerics"].get(numeric, None) != None:
        hues.log(hues.huestr("Sent Response for Numeric: " + numeric).magenta.bold.colorized)
        commandMethod = getattr(numerics, config["numerics"][numeric])
        commandMethod(irc, config, host, user, message)

def processChatMessage(irc, sender, command, receiver, message):
    message = message[1:] if message.startswith(":") else message
    requester = getRequester(False, sender) if receiver == nick else receiver
    commandLookup = message.split()[0]

    if config["botcommands"].get(commandLookup, None) != None:
        hues.log(hues.huestr("Sent: " + commandLookup + " RESPONSE to " + requester).magenta.bold.colorized)
        commandMethod = getattr(commands, config["botcommands"][commandLookup])
        if (len(message.split()) == 1):
            commandMethod(irc, config, requester, None)
        else:
            commandMethod(irc, config, requester, message.replace(commandLookup, ""))

def main(argv):
    sentUser = False
    sentNick = False

    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((config["server"]["name"], config["server"]["port"]))
    try:
        while True:
            data = irc.recv(2048)
            if len(data) <= 0:
                continue

            if data.find('PING') != -1:
                irc.send(config["irccommands"]["pong"].format(data.split()[1]))
                hues.log(hues.huestr("Sent: PONG").magenta.bold.colorized)
                continue

            if sentUser == False:
                irc.send(config["irccommands"]["user"].format(nick, nick, nick, realname))
                sentUser = True
                hues.log(hues.huestr("Sent: USER").magenta.bold.colorized)
                continue

            if sentUser and sentNick == False:
                irc.send(config["irccommands"]["nick"].format(nick))
                sentNick = True
                hues.log(hues.huestr("Sent: NICK").magenta.bold.colorized)
                continue

            for lineText in data.split("\r\n"):
                messageMatches = re.search("(:[\\w\\.]+\\s)(\\d{3}\\s|[A-Z]+\\s)([\\w]+\\s)(.+)", lineText)
                if messageMatches:
                    processServerMessage(irc, messageMatches.group(1)[1:-1], messageMatches.group(2)[:-1],
                                         messageMatches.group(3)[:-1], messageMatches.group(4)[1:])

                messageMatches = re.search("(:.+@.+\\s)([A-Z]+\\s)([\\w#]+\\s)(:?.+)", lineText)
                if messageMatches:
                    processChatMessage(irc, messageMatches.group(1)[1:-1], messageMatches.group(2)[:-1],
                                       messageMatches.group(3)[:-1], messageMatches.group(4))

    except KeyboardInterrupt:
        commands.kill_command(irc, config, None, None)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')

    with open('config.json', 'r') as configFile:
        config = json.load(configFile)

    nick = config["nickname"]
    realname = config["realname"]

    main(sys.argv[1:])
