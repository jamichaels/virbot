import datetime

import utility
from logtype import VirBotLogType

class VirBotNumerics:
    def __init__(self, irc, config):
        self.irc = irc
        self.config = config

    def process_botnumeric(self, host, numeric, user, message):
        if self.config["numerics"].get(numeric, None) != None:
            commandMethod = getattr(self, self.config["numerics"][numeric])
            commandMethod(host, user, message)
        elif numeric == "NOTICE":
            utility.consoleMessage(VirBotLogType.NOTICE, message)
        else:
            utility.consoleMessage(VirBotLogType.SERVER, message)

    """
    Bot Numerics
    """

    #Channel Topic
    def numeric_332(self, host, user, message):
        topic = message[message.find(':') + 1:]
        channel = message.split(':')[0][:-1]
        utility.consoleMessage(VirBotLogType.CHANNEL, "[TOPIC in #" + channel + "] " + topic)

    #Channel Topic Set By
    def numeric_333(self, host, user, message):
        topicinfo = message.split(' ')
        channel = topicinfo[0]
        setby = topicinfo[1]
        seton = datetime.datetime.fromtimestamp(int(float(topicinfo[2]))).strftime('%c')
        seton.replace("  ", " ")
        utility.consoleMessage(VirBotLogType.CHANNEL, "[TOPIC in #" + channel + "] Set By " + setby + " @ " + seton)

    #Channel Users
    def numeric_353(self, host, user, message):
        names = message[message.find(':') + 1:]
        channel = message.split(':')[0][2:-1]
        utility.consoleMessage(VirBotLogType.CHANNEL, "[USERS in #" + channel + "] " + names)

    #Message of MOTD
    def numeric_372(self, host, user, message):
        utility.consoleMessage(VirBotLogType.GENERIC, "[MOTD] " + message)

    #Start of MOTD
    def numeric_375(self, host, user, message):
        utility.consoleMessage(VirBotLogType.GENERICBOLD, "[MOTD] " + message)

    #End of MOTD
    def numeric_376(self, host, user, message):
        utility.consoleMessage(VirBotLogType.GENERICBOLD, "[MOTD] " + message)
