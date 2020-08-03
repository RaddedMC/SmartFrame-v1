# -- IMPORTS --
import Card #Card class, required

import datetime #Needed for datetime card

import pychromecast #Only needed for Chromecasts
#import wget #TODO: Download photos

from phue import Bridge #Only needed for Hue

import requests, json #For weather



# -- GETCARDDATA --
def getCardData():
	# Each piece of data should have 5 keypairs:
		# source-name
		# primary-text
		# secondary-text
		# bg-color
		# photo (either a directory or 'nope')

	cards = []
	#data grabbing code starts here
	#TODO: Make this dynamic based on some kind of config file




	# TIME
	sourceName = "Current Time"
	print("Getting primary data from module " + sourceName + "...") #NOT USER CHANGEABLE


	currentTime = datetime.datetime.now()
	if currentTime.hour > 12:
		primaryText = str(currentTime.hour-12) + ":" + str(currentTime.minute) + " PM"
	else:
		primaryText = str(currentTime.hour) + ":" + str(currentTime.minute) + " AM"


	print("primary data grabbed successfully! " + primaryText) #NOT USER CHANGEABLE
	print("Getting secondary data from module " + sourceName + "...") #NOT USER CHANGEABLE


	secondaryText = str(currentTime.month) + "-" + str(currentTime.day) + "-" + str(currentTime.year)


	print("secondary data grabbed successfully! " + secondaryText) #NOT USER CHANGEABLE
	print("Getting background color from module " + sourceName + "...") #NOT USER CHANGEABLE


	bgColor = "#000000"


	print("background color grabbed successfully! " + bgColor) #NOT USER CHANGEABLE
	print("Getting photo from module " + sourceName + "...") #NOT USER CHANGEABLE


	photo = "nope"


	if (photo == "nope"):
		print(sourceName + " requested to have no photo.") #NOT USER CHANGEABLE
	else:
		print(sourceName + "'s photo is named " + photo) #NOT USER CHANGEABLE


	print("Data for " + sourceName + " grabbed successfully.")
	cards.append(Card.Card(sourceName, primaryText, secondaryText, bgColor, photo))





	# TIME
	sourceName = "Current Time"
	print("Getting primary data from module " + sourceName + "...") #NOT USER CHANGEABLE

	minute = str(currentTime.minute)
	if (len(minute) == 1):
		minute = "0" + minute

	currentTime = datetime.datetime.now()
	if currentTime.hour > 12:
		primaryText = str(currentTime.hour-12) + ":" + minute + " PM"
	else:
		primaryText = str(currentTime.hour) + ":" + minute + " AM"


	print("primary data grabbed successfully! " + primaryText) #NOT USER CHANGEABLE
	print("Getting secondary data from module " + sourceName + "...") #NOT USER CHANGEABLE


	secondaryText = str(currentTime.month) + "-" + str(currentTime.day) + "-" + str(currentTime.year)


	print("secondary data grabbed successfully! " + secondaryText) #NOT USER CHANGEABLE
	print("Getting background color from module " + sourceName + "...") #NOT USER CHANGEABLE


	bgColor = "#000000"


	print("background color grabbed successfully! " + bgColor) #NOT USER CHANGEABLE
	print("Getting photo from module " + sourceName + "...") #NOT USER CHANGEABLE


	photo = "nope"


	if (photo == "nope"):
		print(sourceName + " requested to have no photo.") #NOT USER CHANGEABLE
	else:
		print(sourceName + "'s photo is named " + photo) #NOT USER CHANGEABLE




	# CHROMECASTS

	print("Searching for Chromecasts on the network...")
	chromecasts, browser = pychromecast.get_chromecasts()
	for chromecast in chromecasts:
		chromecast.wait()
		print("Discovered Chromecast: " + chromecast.device.friendly_name)
		if not (chromecast.status.display_name == "Backdrop" or chromecast.status.display_name == None):
			sourceName = chromecast.device.friendly_name
			print("Getting primary data from module " + sourceName + "...") #NOT USER CHANGEABLE

			primaryText = chromecast.status.status_text
			primaryText = primaryText.replace("Casting: ", "")


			print("primary data grabbed successfully! " + primaryText) #NOT USER CHANGEABLE
			print("Getting secondary data from module " + sourceName + "...") #NOT USER CHANGEABLE


			secondaryText = str(chromecast.status.display_name)


			print("secondary data grabbed successfully! " + secondaryText) #NOT USER CHANGEABLE
			print("Getting background color from module " + sourceName + "...") #NOT USER CHANGEABLE


			if secondaryText == "YouTube" or secondaryText == "Netflix":
				bgColor = "#330000"
			elif secondaryText == "Spotify":
				bgColor = "#003300"
			else:
				bgColor = "#333333"


			print("background color grabbed successfully! " + bgColor) #NOT USER CHANGEABLE
			print("Getting photo from module " + sourceName + "...") #NOT USER CHANGEABLE


			#imageUrl = chromecast.device.icon_url #TODO: Wait for pillow to support downloadable photos or figure it out yourself
			#photo = wget.download(imageUrl)


			if (photo == "nope"):
				print(sourceName + " requested to have no photo.") #NOT USER CHANGEABLE
			else:
				print(sourceName + "'s photo is named " + photo) #NOT USER CHANGEABLE


			print("Data for " + sourceName + " grabbed successfully.")
			cards.append(Card.Card(sourceName, primaryText, secondaryText, bgColor, photo))




	# HUE
	ipfailed = False
	try:
		ipFile = open("hue-ip-addr", "r") #TODO: Should probably have some error checking here
		ip = ipFile.read()
	except FileNotFoundError:	
		print("IP file not found. Philips Hue support is disabled.")
		print("Create a file named hue-ip-addr within the same directory as this python program containing the IP of your Philips Hue Bridge to begin connection.")
		ipfailed = True

	if not ipfailed:
		try:
			print("Searching for a Philips Hue bridge at " + ip + "...")
			b = Bridge(ip)
			groups = b.groups
			for group in groups:
				if group.on and not group.name.startswith("hgrp-"):
					print("Discovered powered light group: " + group.name)
					sourceName = "Philips Hue"
					print("Getting primary data from module " + sourceName + "...") #NOT USER CHANGEABLE


					primaryText = "Lights are ON!"


					print("primary data grabbed successfully! " + primaryText) #NOT USER CHANGEABLE
					print("Getting secondary data from module " + sourceName + "...") #NOT USER CHANGEABLE


					secondaryText = group.name + " Lights"


					print("secondary data grabbed successfully! " + secondaryText) #NOT USER CHANGEABLE
					print("Getting background color from module " + sourceName + "...") #NOT USER CHANGEABLE


					bgColor = "#333300"


					print("background color grabbed successfully! " + bgColor) #NOT USER CHANGEABLE
					print("Getting photo from module " + sourceName + "...") #NOT USER CHANGEABLE


					photo = "nope"


					if (photo == "nope"):
						print(sourceName + " requested to have no photo.") #NOT USER CHANGEABLE
					else:
						print(sourceName + "'s photo is named " + photo) #NOT USER CHANGEABLE

					print("Data for " + sourceName + " grabbed successfully.")
					cards.append(Card.Card(sourceName, primaryText, secondaryText, bgColor, photo))
		except:
			print("Error with Philips hue:") #TODO: Color errors
			print("You need to run the phue.py setup program and press the button on your Philips Hue bridge to link your device to your Bridge.")
			print("More instructons are on github.com/RaddedMC/SmartFrame/blob/master/README.MD")




	# TEMPLATE

	#sourceName = "Current Time"
	#print("Getting primary data from module " + sourceName + "...") #NOT USER CHANGEABLE


	#primaryText = 


	#print("primary data grabbed successfully! " + primaryText) #NOT USER CHANGEABLE
	#print("Getting secondary data from module " + sourceName + "...") #NOT USER CHANGEABLE


	#secondaryText = 


	#print("secondary data grabbed successfully! " + secondaryText) #NOT USER CHANGEABLE
	#print("Getting background color from module " + sourceName + "...") #NOT USER CHANGEABLE


	#bgColor = "#000000"


	#print("background color grabbed successfully! " + bgColor) #NOT USER CHANGEABLE
	#print("Getting photo from module " + sourceName + "...") #NOT USER CHANGEABLE


	#photo = "nope"


	#if (photo == "nope"):
	#	print(sourceName + " requested to have no photo.") #NOT USER CHANGEABLE
	#else:
	#	print(sourceName + "'s photo is named " + photo) #NOT USER CHANGEABLE


	#print("Data for " + sourceName + " grabbed successfully.")
	#cards.append(Card.Card(sourceName, primaryText, secondaryText, bgColor, photo))




	#data grabbing code ends here
	return cards