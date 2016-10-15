import os
import re
import socket
import time
import sys
import json
import urllib2
from urllib import urlopen
from bs4 import BeautifulSoup, Tag
import httplib
import wolframalpha
from googlefinance import getQuotes

user = "virbot "
channel = "#virus"
wukey = "510b7638db220d26"
priv = "PRIVMSG " + channel + " :"

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome"}

ed_url = "http://encyclopediadramatica.se/"

## for urban dict
words = []
urbUrl = 'http://www.urbandictionary.com/define.php?term='
##

connected = False
sentUser = False
sentNick = False

wp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
wp.connect(('us.undernet.org', 6667))
while True:
    data = wp.recv(2048)
    if len(data) > 0:
        print data
    else:
        continue
    time.sleep(1)


    if data.find('PING') != -1:
        wp.send('PONG ' + data.split()[1] + "\r\n")
        print "PING received, PONG sent"
        continue

    if sentUser == False:
        wp.send("User " + user + user + user + ":i'm a virbot\n")
        sentUser = True
        print "SentUser successful"
        continue

    if  sentUser and sentNick == False:
        wp.send("NICK virbot\n")
        sentNick = True
        print "sentNick successful"
        continue

    if sentUser and sentNick and not connected:
        wp.send("JOIN " + channel + "\n")
        connected = True
        print "connected successful"
        continue

    if data.find("!drama") != -1:

        entryMaxSize = 400
        d2 = data.split(' ')
        del d2[0:4]
        print "drama" + d2[0]
        url = ed_url + ''.join(d2)
        print url + "\n"

        reload(sys)
        sys.setdefaultencoding('utf8')


        html = urlopen(url)
        soup = BeautifulSoup(html.read(), 'html.parser')
        drama = soup.find(id="bodyContent")

        entryText = ""
        for element in drama:
            if not isinstance(element, Tag):
                continue

            elementText = element.get_text().replace("\n", "")

            if elementText == u"" or elementText == u" ":
                continue
            if elementText.startswith(u"From Encyclopedia Dramatica"):
                continue
            if elementText.startswith(u"Jump to: navigation, search"):
                continue

            entryText += " " + elementText
            entryLength = len(entryText)
            if entryLength > entryMaxSize:
                entryText = entryText[:-(entryLength-entryMaxSize)]
                break

        wp.send(priv + entryText.strip() + "\n")
        continue

    if data.find("!wolfram") != -1:
        client = wolframalpha.Client("236P2P-X4JWQKUU93")
        reload(sys)
        sys.setdefaultencoding('utf8')
       	try:
		d2 = data.split(' ')
        	del d2[0:4]
        	q = ' '.join(d2).replace('\n','')
		print q
		res = client.query(q)
        	wp.send("PRIVMSG " + channel + " : " + next(res.results).text + "\n")
        	continue
	except:
		""
	continue

    if data.find("!urban") != -1:
        reload(sys)
        sys.setdefaultencoding('utf8')
        d2 = data.split(' ')
        del d2[0:4]
        wordUrl = urbUrl + ''.join(d2).replace('%','')
        print wordUrl + "\n"
        html = urlopen(wordUrl)
        soup = BeautifulSoup(html.read(), 'html.parser')
        meaning = soup.findAll("div",{"class" : "meaning"})
        urbl = meaning[0].get_text().replace("\n", "")
        wp.send("PRIVMSG " + channel + " : " + urbl + "\n")
        continue

    if data.find("!stock") != -1:
        reload(sys)
        sys.setdefaultencoding('utf8')
        d2 = data.split(' ')
        del d2[0:4]
	z = ''.join(d2).replace('\n','')
	print z
	try:
		x = json.dumps(getQuotes(z), indent=2)
		y = x.split()
		z = ''.join(y[5]).replace('\n','').replace('\"','').replace(',','')
		print z
		wp.send(priv + z + "\n")
		continue
	except:
		""
	continue

    if data.find("http://") != -1:
        reload(sys)
        sys.setdefaultencoding('utf8')
        d2 = data.split(' ')
        url = d2[3]
        url = url[1:]
        if "http" in url:
            try:
                html = urllib2.urlopen(url)
            except urllib2.HTTPError as e:
                print "The server couldn't fulfill the request."
                print 'Error code: ', e.code
            except urllib2.URLError as e:
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            else:
                soup = BeautifulSoup(html.read(), 'html.parser')
                try:
                    title = soup.title.string.replace("\n","")
                    print title
                    wp.send(priv + title + "\n")
                except:
                    ""
            continue

    if data.find("!astronomy") != -1:
        reload(sys)
        sys.setdefaultencoding('utf8')
        d2 = data.split(' ')
        zip = d2[4]
        zip.rstrip()
        zip = zip[:-1]
        zip = zip[:-1]
        url = "http://api.wunderground.com/api/" + wukey + "/astronomy/q/CA/" + zip + ".json"
        print url + "\n"
        f = urllib2.urlopen(url)
        json_string = f.read()
        if "error" not in json_string:
            pj = json.loads(json_string)
            sunrise = pj['moon_phase']['sunrise']['hour'] + ":" + pj['moon_phase']['sunrise']['minute']
            sunset = pj['moon_phase']['sunset']['hour'] + ":" + pj['moon_phase']['sunset']['minute']
            illum = pj['moon_phase']['percentIlluminated'] + "%"
            age = pj['moon_phase']['ageOfMoon']
            phase = pj['moon_phase']['phaseofMoon']
            mp = "Sunrise " + sunrise + ", sunset " + sunset + ". Moonphase " + illum + ", age " + age + ", in a " + phase + " phase."

            wp.send(priv + mp + "\n")
            f.close
            continue
        else:
            continue

    if data.find("!weather") != -1:
        reload(sys)
        sys.setdefaultencoding('utf8')
        print data + "\n"
        d2 = data.split(' ')
        zip = d2[4]
        zip.rstrip('\r')
        zip.rstrip('\n')
        zip = zip[:-1]
        zip = zip[:-1]
        zipMatches = re.search(u"[0-9]{5}", zip)
        if zipMatches:
		try:
                	url = "http://api.wunderground.com/api/" + wukey + "/geolookup/conditions/q/PA/" + zip + ".json"
                	print url
                	f = urllib2.urlopen(url)
                	json_string = f.read()
                	if "error" not in json_string:
                    		parsed_json = json.loads(json_string)
                    		city = parsed_json['location']['city']
                    		state = parsed_json['current_observation']['weather']
                    		weather = parsed_json['current_observation']['weather']
                    		temperature_string = parsed_json['current_observation']['temperature_string']
                    		humidity = parsed_json['current_observation']['relative_humidity']
                    		wind_dir = parsed_json['current_observation']['wind_dir']
                    		gust = parsed_json['current_observation']['wind_gust_mph']
                    		wp.send(priv + weather + ", wind from the " + wind_dir + " gusting to " + str(gust) + " mph, " + str(humidity) + " humidity, " + str(temperature_string) + "\n")
                    		f.close
                    		continue
		except:
			""
		continue
    if not connected:
            connected = True
