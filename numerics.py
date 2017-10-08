import hues

def numeric_376(irc, config, host, user, message):
    hues.log(hues.huestr("Sent: JOIN").magenta.bold.colorized)
    irc.send(config["irccommands"]["join"].format(config["channel"]))
