import re
import hues

from logtype import VirBotLogType


def getRequester(usesPrefix, text):
    searchPattern = "(?<=:).+(?=!)" if usesPrefix else ".+(?=!)"
    requestMatches = re.search(searchPattern, text, re.I)
    if requestMatches:
        return str(requestMatches.group())
    return ""

def consoleMessage(logtype, message):
    if logtype is VirBotLogType.ERROR:
        hues.log(hues.huestr("[ERROR] " + message).magenta.bold.colorized)
    elif logtype is VirBotLogType.GENERIC:
        hues.log(hues.huestr(message).black.colorized)
    elif logtype is VirBotLogType.GENERICBOLD:
        hues.log(hues.huestr(message).black.bold.colorized)
    elif logtype is VirBotLogType.CHANNEL:
        hues.log(hues.huestr(message).blue.bold.colorized)
    elif logtype is VirBotLogType.NOTICE:
        hues.log(hues.huestr("[NOTICE] " + message).blue.bold.colorized)
    elif logtype is VirBotLogType.RECEIVED:
        hues.log(hues.huestr("[RECEIVED] " + message).green.colorized)
    elif logtype is VirBotLogType.SENT:
        hues.log(hues.huestr("[SENT] " + message).magenta.bold.colorized)
    elif logtype is VirBotLogType.SERVER:
        hues.log(hues.huestr("[SERVER] " + message).cyan.bold.colorized)