from enum import Enum


class VirBotLogType(Enum):
    ERROR = 1
    GENERIC = 2
    GENERICBOLD = 3
    CHANNEL = 4
    NOTICE = 5
    RECEIVED = 6
    SENT = 7
    SERVER = 8