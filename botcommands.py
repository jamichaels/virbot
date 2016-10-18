import platform


def host_command(irc, ircCommands, requester, message):
    irc.send(ircCommands["privmsg"].format(requester, str(platform.platform())))