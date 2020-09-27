# -- IMPORTS --
import Card #Card class, required

import datetime #Needed for datetime card

import wget #For downloading photos

import requests, json #For weather

import signal #For timeouts
from contextlib import contextmanager
@contextmanager
def timeout(time):
	signal.signal(signal.SIGALRM, raise_timeout)
	signal.alarm(time)
	try:
		yield
	except TimeoutError:
		print("The above operation timed out. Check your SmartFrame device's network or internet connection.")
		pass
	finally:
		signal.signal(signal.SIGALRM, signal.SIG_IGN)

def raise_timeout(signum, frame):
	raise TimeoutError






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
	primaryText = currentTime.strftime("%-I:%M %p")


	print("primary data grabbed successfully! " + primaryText) #NOT USER CHANGEABLE
	print("Getting secondary data from module " + sourceName + "...") #NOT USER CHANGEABLE


	secondaryText = currentTime.strftime("%A %B %-d, %Y")


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




	# SERVER NOTIFICATIONS
	import os #For server notifications
	print("Checking notifications directory...")
	for file in os.listdir(os.getcwd() + "/Notifications/"):
		fileLocation = os.getcwd() + "/Notifications/" + file
		print("Notification from " + file + "!")
		sourceName = file
		print("Getting primary data from module " + sourceName + "...") #NOT USER CHANGEABLE


		lines = [line.rstrip('\n') for line in open(fileLocation, "r").readlines()]
		try:
			if lines[2] != "0" and len(lines) == 3 and isinstance(int(lines[2]), int):
				primaryText = lines[0]
				print("primary data grabbed successfully! " + primaryText) #NOT USER CHANGEABLE
				print("Getting secondary data from module " + sourceName + "...") #NOT USER CHANGEABLE
				secondaryText = lines[1]
				print("secondary data grabbed successfully! " + secondaryText) #NOT USER CHANGEABLE
				print("Getting background color from module " + sourceName + "...") #NOT USER CHANGEABLE
				if lines[2] == "1":
					bgColor = "#440000"
				else:
					bgColor = "#444444"
				print("background color grabbed successfully! " + bgColor) #NOT USER CHANGEABLE
				print(sourceName + " requested to have no photo.") #NOT USER CHANGEABLE
				print("Data for " + sourceName + " grabbed successfully.")
				cards.append(Card.Card(sourceName, primaryText, secondaryText, bgColor, "nope"))
				lines[2] = int(lines[2]) - 1
				file = open(fileLocation, "w")
				file.write(lines[0]+"\n"+lines[1]+"\n"+str(lines[2]))
				file.close()
			else:
				print("Notification has expired or file is invalid. Deleting " + fileLocation + "...")
				os.remove(fileLocation)
		except (IndexError, ValueError) as E:

			print("Notification file " + fileLocation + " is invalid. Deleting file...")
			print(E)
			os.remove(fileLocation)




	# SPOTIFY
	import spotipy
	from spotipy.oauth2 import SpotifyOAuth #For Spotify integration, NEED AN API KEY FOR YOUR ACCOUNT!
	print("Attempting to talk to Spotify...")
	spotify_scope = "user-read-currently-playing"
	do_a_spotify = True
	try:
		userFile = open("spotify-user", "r") #TODO: Should probably have some error checking here
		spotify_user = userFile.readline().rstrip("\n")
		client_id = userFile.readline().rstrip("\n")
		client_secret = userFile.readline().rstrip("\n")
	except FileNotFoundError:	
		print("Spotify username file not found. Spotify support is disabled.")
		print("Create a file named spotify-user within the same directory as this python program containing your Spotify username. This is used to read the name of your currently playing playlist.")
		do_a_spotify = False
	except:
		print("Unknown error getting your spotify information. Read the readme.MD file and make sure you've created your user info file correctly.")

	if do_a_spotify:
		with timeout(30):
			try:
				spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=spotify_scope, redirect_uri="http://127.0.0.1:9090", cache_path=".spotifcache", client_id=client_id, client_secret=client_secret)) #Use an environment varaiable or pass in your keys here, use a web browser to authenticate. If running headless, download a simple browser and forward the X session over SSH.
				# I know this is a stupid way to do things, but for a personal project it worked fine for me.
				current_track = spotify.current_user_playing_track()
				if current_track == False:
					print("Nothing is playing on your Spotify Account.")
					do_a_spotify = False
				if current_track["is_playing"] == False:
					print("Spotify is paused.")
					do_a_spotify = False

			except:
				print("Failed to get data from Spotify!")

				do_a_spotify = False

	if do_a_spotify:
		try:
			current_list = spotify.user_playlist(user=spotify_user, playlist_id=current_track["context"]["uri"], fields="name")
		except TypeError:
			current_list = {'name':'Now Playing'}
		
	if do_a_spotify==True and current_track["is_playing"]==True:
		sourceName = "Spotify - " + current_list["name"]
		print("Getting primary data from module " + sourceName + "...") #NOT USER CHANGEABLE

		is_podcast = False
		try:
			primaryText = current_track["item"]["name"]
		except TypeError:
			primaryText = "Podcast"
			is_podcast = True


		print("primary data grabbed successfully! " + primaryText) #NOT USER CHANGEABLE
		print("Getting secondary data from module " + sourceName + "...") #NOT USER CHANGEABLE

		if not is_podcast:
			secondaryText = current_track["item"]["artists"][0]["name"] + " - " + current_track["item"]["album"]["name"]
		else:
			secondaryText = "Spotify"


		print("secondary data grabbed successfully! " + secondaryText) #NOT USER CHANGEABLE
		print("Getting background color from module " + sourceName + "...") #NOT USER CHANGEABLE


		bgColor = "#004400"


		print("background color grabbed successfully! " + bgColor) #NOT USER CHANGEABLE
		print("Getting photo from module " + sourceName + "...") #NOT USER CHANGEABLE

		if not is_podcast:
			try:
				photo = wget.download(current_track["item"]["album"]["images"][2]["url"])
				import colorgram
				rgb = colorgram.extract(photo, 1)[0].rgb
				from math import ceil
				bgColor = '#%02x%02x%02x' % (ceil(rgb[0]*0.4), ceil(rgb[1]*0.4), ceil(rgb[2]*0.4))
				print("background changed! " + bgColor) #NOT USER CHANGEABLE
			except:
				photo = "nope"
		else:
			photo = "nope"


		if (photo == "nope"):
			print(sourceName + " requested to have no photo.") #NOT USER CHANGEABLE
		else:
			print(sourceName + "'s photo is named " + photo) #NOT USER CHANGEABLE


		print("Data for " + sourceName + " grabbed successfully.")
		cards.append(Card.Card(sourceName, primaryText, secondaryText, bgColor, photo))

		


	# CHROMECASTS
	import pychromecast #Only needed for Chromecasts
	print("Searching for Chromecasts on the network...")
	with timeout(10):
		chromecasts, browser = pychromecast.get_chromecasts()
		for chromecast in chromecasts:
			chromecast.wait()
			print("Discovered Chromecast: " + chromecast.device.friendly_name)
			if not (chromecast.status.display_name == "Backdrop" or chromecast.status.display_name == None or chromecast.status.display_name == "Spotify"):
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
					bgColor = "#440000"
				elif secondaryText == "Bluetooth Audio":
					bgColor = "#000044"
				else:
					bgColor = "#444444"


				print("background color grabbed successfully! " + bgColor) #NOT USER CHANGEABLE
				print("Getting photo from module " + sourceName + "...") #NOT USER CHANGEABLE


				#imageUrl = chromecast.device.icon_url #TODO: Wait for pillow to support downloadable photos or figure it out yourself
				#photo = wget.download(imageUrl)
				photo = "nope"


				if (photo == "nope"):
					print(sourceName + " requested to have no photo.") #NOT USER CHANGEABLE
				else:
					print(sourceName + "'s photo is named " + photo) #NOT USER CHANGEABLE


				print("Data for " + sourceName + " grabbed successfully.")
				cards.append(Card.Card(sourceName, primaryText, secondaryText, bgColor, photo))




	# HUE

	import phue #Only needed for Hue
	ipfailed = False
	try:
		ipFile = open("hue-ip-addr", "r") #TODO: Should probably have some error checking here
		ip = ipFile.read()
	except FileNotFoundError:	
		print("IP file not found. Philips Hue support is disabled.")
		print("Create a file named hue-ip-addr within the same directory as this python program containing the IP of your Philips Hue Bridge to begin connection.")
		ipfailed = True

	if not ipfailed:
		with timeout(10):
			try:
				print("Searching for a Philips Hue bridge at " + ip + "...")
				b = phue.Bridge(ip)
				groups = b.groups
				for group in groups:
					lightdown = False
					for light in group.lights:
							if not light.reachable:
								lightdown = True
								break

					if not group.name.startswith("hgrp-"):
						if lightdown:
							print("Discovered offline light group: " + group.name)
							sourceName = "Philips Hue"
							print("Getting primary data from module " + sourceName + "...") #NOT USER CHANGEABLE
							primaryText = "OFFLINE"
							bgColor = "#440000"
							print("primary data grabbed successfully! " + primaryText) #NOT USER CHANGEABLE
							print("Getting secondary data from module " + sourceName + "...") #NOT USER CHANGEABLE
							secondaryText = group.name + " Lights"
							print("secondary data grabbed successfully! " + secondaryText) #NOT USER CHANGEABLE
							print("Getting background color from module " + sourceName + "...") #NOT USER CHANGEABLE


							print("background color grabbed successfully! " + bgColor) #NOT USER CHANGEABLE
							print("Getting photo from module " + sourceName + "...") #NOT USER CHANGEABLE


							photo = "nope"
							if (photo == "nope"):
								print(sourceName + " requested to have no photo.") #NOT USER CHANGEABLE
							else:
								print(sourceName + "'s photo is named " + photo) #NOT USER CHANGEABLE

							print("Data for " + sourceName + " grabbed successfully.")
							cards.append(Card.Card(sourceName, primaryText, secondaryText, bgColor, photo))
						elif group.on:
							print("Discovered powered light group: " + group.name)
							sourceName = "Philips Hue"
							print("Getting primary data from module " + sourceName + "...") #NOT USER CHANGEABLE

							primaryText = "ON " + str(round(group.brightness/2.55)) + "%"
							bgColor = "#" + 2*(hex(round((group.brightness*0.2666666))).replace("0x","")) + "00"


							print("primary data grabbed successfully! " + primaryText) #NOT USER CHANGEABLE
							print("Getting secondary data from module " + sourceName + "...") #NOT USER CHANGEABLE


							secondaryText = group.name + " Lights"


							print("secondary data grabbed successfully! " + secondaryText) #NOT USER CHANGEABLE
							print("Getting background color from module " + sourceName + "...") #NOT USER CHANGEABLE


							print("background color grabbed successfully! " + bgColor) #NOT USER CHANGEABLE
							print("Getting photo from module " + sourceName + "...") #NOT USER CHANGEABLE


							photo = "nope"

							if (photo == "nope"):
								print(sourceName + " requested to have no photo.") #NOT USER CHANGEABLE
							else:
								print(sourceName + "'s photo is named " + photo) #NOT USER CHANGEABLE

							print("Data for " + sourceName + " grabbed successfully.")
							cards.append(Card.Card(sourceName, primaryText, secondaryText, bgColor, photo))
			except phue.PhueRegistrationException:
				print("Error with Philips hue:") #TODO: Color errors
				print("You need to run the phue.py setup program and press the button on your Philips Hue bridge to link your device to your Bridge.")
				print("More instructons are on github.com/RaddedMC/SmartFrame/blob/master/README.MD")
			except:
				print("Unknown error with Philips Hue. check the traceback above for details.")




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
	print("Data ready.")
	return cards
