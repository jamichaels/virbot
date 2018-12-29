# coding=utf-8
import platform
import sys
import urllib

import utility
from logtype import VirBotLogType


class VirBotCommands:
    def __init__(self, irc, config):
        self.irc = irc
        self.config = config

    def process_botcommand(self, sender, requester, command, message):
        if self.config["botcommands"].get(command, None) != None:
            utility.consoleMessage(VirBotLogType.RECEIVED, command + " command FROM " + requester + " (" + sender + ")")
            commandMethod = getattr(self, self.config["botcommands"][command])
            if (len(message.split()) == 1):
                commandMethod(requester, None)
            else:
                commandMethod(requester, message.replace(command, ""))

    """
    Bot Commands
    """

    def send_formatted_command(self, command, *args):
        self.irc.send(self.config["irccommands"][command].format(*args))

    def host_command(self, requester, message):
        self.send_formatted_command("privmsg", requester, str(platform.platform()))

    def join_command(self, requester, message):
        messageParts = message.split()
        if (len(messageParts) == 1 and messageParts[0].startswith("#")):
            self.send_formatted_command("join", message)

    def kill_command(self, requester, message):
        self.send_formatted_command("quit", self.config["strings"]["quitmessage"])
        print "\n"
        sys.exit()

    def lmgtfy_command(self, requester, message):
        self.send_formatted_command("privmsg", requester, "http://lmgtfy.com/?q=" + urllib.quote(message[1:]))

    def part_command(self, requester, message):
        messageParts = message.split()
        if (len(messageParts) == 1 and messageParts[0].startswith("#")):
            self.send_formatted_command("part", messageParts[0])
            
    def op_command(self, requester, message):
        messageParts = message.split()
        if (messageParts[0].startswith("#"))
            self.send_formatted_command("op", messageParts[0], requester)