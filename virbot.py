import os
import re
import socket
import time
import sys
import json

with open('config.json', 'r') as configFile:
    config = json.load(configFile)
    serverConfig = config["server"]
    ircComands = config["irccommands"]

user = config["nickname"]
channel = config["channel"]
realname = config["realname"]

connected = False
sentUser = False
sentNick = False

wp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
wp.connect((serverConfig["name"], serverConfig["port"]))
while True:
    data = wp.recv(2048)
    if len(data) > 0:
        print data
    else:
        continue
    time.sleep(1)

    if data.find('PING') != -1:
        wp.send(ircComands["pong"].format(data.split()[1]))
        print "PING received, PONG sent"
        continue

    if sentUser == False:
        wp.send(ircComands["user"].format(user, user, user, realname))
        sentUser = True
        print "SentUser successful"
        continue

    if sentUser and sentNick == False:
        wp.send(ircComands["nick"].format(user))
        sentNick = True
        print "sentNick successful"
        continue

    if sentUser and sentNick and not connected:
        wp.send(ircComands["join"].format(channel))
        connected = True
        print "connected successful"
        continue

    if not connected:
        connected = True
