import botcommands
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
    if numeric.find("255") != -1:
        hues.log(hues.huestr("Sent: JOIN").magenta.bold.colorized)
        irc.send("JOIN " + channel + "\n")

def processChatMessage(irc, sender, command, receiver, message):
    message = message[1:] if message.startswith(":") else message
    requester = getRequester(False, sender) if receiver == nick else receiver
    isFromChannel = requester.startswith("#")

    if botCommands.get(message.split()[0], None) != None:
        commandMethod = getattr(botcommands, botCommands[message.split()[0]])
        commandMethod(irc, ircComands, requester, message)

def main(argv):
    sentUser = False
    sentNick = False

    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((serverConfig["name"], serverConfig["port"]))
    try:
        while True:
            data = irc.recv(2048)
            if len(data) > 0:
                hues.log(hues.huestr("Server: " + data).blue.bold.colorized)
            else:
                continue

            if data.find('PING') != -1:
                irc.send(ircComands["pong"].format(data.split()[1]))
                hues.log(hues.huestr("Sent: PONG").magenta.bold.colorized)
                continue

            if sentUser == False:
                irc.send(ircComands["user"].format(nick, nick, nick, realname))
                sentUser = True
                hues.log(hues.huestr("Sent: USER").magenta.bold.colorized)
                continue

            if sentUser and sentNick == False:
                irc.send(ircComands["nick"].format(nick))
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
        irc.send(ircComands["quit"].format(strings["quitmessage"]))
        print "\n"
        sys.exit()

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')

    with open('config.json', 'r') as configFile:
        config = json.load(configFile)
        serverConfig = config["server"]
        botCommands = config["botcommands"]
        ircComands = config["irccommands"]
        strings = config["strings"]

    nick = config["nickname"]
    channel = config["channel"]
    realname = config["realname"]

    main(sys.argv[1:])
