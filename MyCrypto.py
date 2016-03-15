#!/usr/bin/env python			
# -*- coding: utf-8 -*-
		
#########################################################################	
#																		#																
# Created by Luke Turvey 2016											#
# djturvey@hotmail.co.uk												#
# www.mrturvey.co.uk													#
#																		#
#########################################################################


#Imports
import threading
from threading import Thread
import json
from pprint import pprint
import urllib
from slacker import Slacker
from datetime import datetime
import subprocess
import time
import tweepy
import smtplib


#Variables CHANGE ME

# SLACK CONTROLS #
slackAPI = Slacker('') #Your Slack API Key
SlackBotName = "CryptoPimp" #Name of the bot which will be posting to your channel
SlackChannel = "" #Your slack channel ID to post updates to
Percentage = 0.05 #The percent you want to be notifed at for when prices change


#Twitter Controls#
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

#Email Controls#
fromaddr = 'Cryptopimp@coins.com'  
toaddrs  = '@googlemail.com'  
username = '@hotmail.co.uk'  
password = 'MEHHHHHHH'




def setBase():
	try:	
		url = 'http://socket.coincap.io/front'
		search_response = urllib.urlopen(url)
		search_results = search_response.read()
		results = json.loads(search_results)
	
		TopTen = [results[0]['long'],results[1]['long'],results[2]['long'],results[3]['long'],results[4]['long'],results[5]['long'],results[6]['long'],results[7]['long'],results[8]['long'],results[9]['long']]
		one = results[0]['price']
		two = results[1]['price']
		three = results[2]['price']
		four = results[3]['price']
		five = results[4]['price']
		six = results[5]['price']
		seven = results[6]['price']
		eight = results[7]['price']
		nine = results[8]['price']
		ten = results[9]['price']
		TopAmt = [one, two, three, four, five, six, seven, eight, nine, ten]
		return url, TopAmt, TopTen
	except Exception as q:
		with open("/root/logs/MyCryptolog.txt", "a") as myfile:
			myfile.write(str(q))
		print str(q)
		start()


def Tracker(url, TopAmt, TopTen):
	while True:
		try:
			time.sleep(120)
			with open("/root/logs/MyCryptolog.txt", "a") as myfile:
				myfile.write("boop " + str(datetime.now()) + "\n")
			search_response = urllib.urlopen(url)
			search_results = search_response.read()
			results = json.loads(search_results)
			for AllCoins in range(len(TopTen)):
				if results[AllCoins]['long'] != TopTen[AllCoins]:
					TopTen[AllCoins] = results[AllCoins]['long']
					TopAmt[AllCoins] = results[AllCoins]['price']
				else:	
					Percent = float(TopAmt[AllCoins]) * Percentage
					if float(results[AllCoins]['price']) >= float(TopAmt[AllCoins]) + Percent:
						TopAmt[AllCoins] = results[AllCoins]['price']
						SendSlack('UP', TopTen[AllCoins], TopAmt[AllCoins])
						Tweeter('UP', TopTen[AllCoins], TopAmt[AllCoins])
						#Emailings('increased', TopTen[AllCoins], TopAmt[AllCoins])
					elif float(results[AllCoins]['price']) <= float(TopAmt[AllCoins]) - Percent:
						TopAmt[AllCoins] = results[AllCoins]['price']
						SendSlack('Down', TopTen[AllCoins], TopAmt[AllCoins])
						Tweeter('Down', TopTen[AllCoins], TopAmt[AllCoins])
						#Emailings('decreased', TopTen[AllCoins], TopAmt[AllCoins])
					else:
						None
		except Exception as g:
			with open("/root/logs/MyCryptolog.txt", "a") as myfile:
				myfile.write(str(g))
			print str(g)
			start()
				
def SendSlack(UpDown, Name, Price):
	try:
		if UpDown == 'UP':
			Send = 'https://slack.com/api/chat.postMessage?token=xoxp-17876044503-17876317799-25507004853-d476d384b5&channel='+SlackChannel+'&text=ITS%20GONE%20UP!%20The%20current%20price%20of%20'+ Name +'%20is%20$' + str(Price) + '&username='+SlackBotName+'&as_user=False&pretty=1'
			Sender(Send)
		else:
			Send = 'https://slack.com/api/chat.postMessage?token=xoxp-17876044503-17876317799-25507004853-d476d384b5&channel='+SlackChannel+'&text=ITS%20GONE%20DOWN!%20The%20current%20price%20of%20+' + Name +'%20is%20$' + str(Price) + '&username='+SlackBotName+'&as_user=False&pretty=1'
			Sender(Send)	
	except Exception as c:
			with open("/root/logs/MyCryptolog.txt", "a") as myfile:
				myfile.write(str(c))
			print str(c)
			start()
	
def Sender(Send):
	try:
		urllib.urlopen(Send)
	except Exception as e:
		with open("/root/logs/MyCryptolog.txt", "a") as myfile:
			myfile.write(str(e))
		print str(e)
		start()

def Tweeter(UpDown, Name, Price):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	try:
		if UpDown == 'UP':
			api.update_status('#' + str(Name) + ' has increased! The price is now $' + str(Price) + ' #Cryptocurrency')
		else:
			api.update_status('#' + str(Name) + ' has decreased! The price is now $' + str(Price) + ' #Cryptocurrency')
	except Exception as m:
		with open("/root/logs/MyCryptolog.txt", "a") as myfile:
			myfile.write(str(m))
		print str(str(m))
		start()

def Emailings(UPDOWN, TopTen, TopAmt):
	msg = TopTen + ' has ' + UPDOWN + '! The price is now $' + str(TopAmt)
	server = smtplib.SMTP('smtp.live.com', 25)  
	server.ehlo()
	server.starttls()
	server.login(username, password)  
	server.sendmail(fromaddr, toaddrs, msg)  
	server.quit()

def start():
	try:
		with open("/root/logs/MyCryptolog.txt", "a") as myfile:
			myfile.write(str(datetime.now()) + " Program Start" '\n')
		print "Going " + str(time.asctime( time.localtime(time.time())))
		
		First = setBase()
		Tracker(First[0], First[1], First[2])	
	except Exception as h:
		with open("/root/logs/MyCryptolog.txt", "a") as myfile:
			myfile.write(str(h))
		print str(str(h))
		start()
	
if __name__ == '__main__':
	
	start()
	
	'''	
	Thread(target = setBase).start()
	#Thread(target = Tweeter).start()
'''

	
	
