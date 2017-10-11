import hues

#Channel Topic
def numeric_332(irc, config, host, user, message):
    topic = message[message.find(':') + 1:]
    channel = message.split(':')[0][:-1]
    hues.log(hues.huestr("[TOPIC in #" + channel + "] " + topic).blue.bold.colorized)

#Channel Users
def numeric_353(irc, config, host, user, message):
    names = message[message.find(':') + 1:]
    channel = message.split(':')[0][2:-1]
    hues.log(hues.huestr("[USERS in #" + channel + "] " + names).blue.bold.colorized)

#Message of MOTD
def numeric_372(irc, config, host, user, message):
    hues.log(hues.huestr("[MOTD] " + message).black.colorized)

#Start of MOTD
def numeric_375(irc, config, host, user, message):
    hues.log(hues.huestr("[MOTD] " + message).black.bold.colorized)

#End of MOTD
def numeric_376(irc, config, host, user, message):
    hues.log(hues.huestr("[MOTD] " + message).black.bold.colorized)
