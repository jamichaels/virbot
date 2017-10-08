import hues

#Message of MOTD
def numeric_372(irc, config, host, user, message):
    hues.log(hues.huestr("[MOTD] " + message).black.colorized)

#Start of MOTD
def numeric_375(irc, config, host, user, message):
    hues.log(hues.huestr("[MOTD] " + message).black.bold.colorized)

#End of MOTD
def numeric_376(irc, config, host, user, message):
    hues.log(hues.huestr("[MOTD] " + message).black.bold.colorized)
