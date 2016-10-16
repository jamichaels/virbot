import platform
import hues


def host_command(irc, ircCommands, requester, message):
    hues.log(hues.huestr("Sent: !host RESPONSE to " + requester).magenta.bold.colorized)
    irc.send(ircCommands["privmsg"].format(requester, str(platform.platform())))