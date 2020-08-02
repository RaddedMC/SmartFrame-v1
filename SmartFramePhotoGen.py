#!/bin/env python

# Get data from:
	# Spotify
	# Google Cast
	# Smart devices
		# preferably IFTTT
	# Calendar
	# Google Keep
	# Last screen of RPI and SolidServ
	# Notifications from RPI and SolidServ

# Throw that into an image
	# User-selectable resolution

# -- IMPORTS --
import sys
from PIL import Image, ImageDraw, ImageFont
import datetime
import Card
import pychromecast


# -- BASIC FUNCTIONS --
def throwErr(msg, code = 5):
	print("Error: " + msg)
	print("SmartFramePhotoGen -h for help.")
	exit(code)

def isThisANumber(isit):
	if isinstance(isit, (int, float, complex)) and not isinstance(isit, bool):
		return True
	else:
		return False

def getHelp():
	print("You've called the help function. Unfortunately, there's nothing here right now.")
	exit(0)
	#TODO: ADD MORE TO THIS


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




	# CHROMECASTS

	print("Searching for Chromecasts on the network...")
	chromecasts, browser = pychromecast.get_chromecasts()
	for chromecast in chromecasts:
		chromecast.wait()
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


			photo = "nope"


			if (photo == "nope"):
				print(sourceName + " requested to have no photo.") #NOT USER CHANGEABLE
			else:
				print(sourceName + "'s photo is named " + photo) #NOT USER CHANGEABLE


			print("Data for " + sourceName + " grabbed successfully.")
			cards.append(Card.Card(sourceName, primaryText, secondaryText, bgColor, photo))



	# HUE



	#data grabbing code ends here
	return cards


# -- GENPHOTO --
def genPhoto(xRes, yRes):
	image = Image.new('RGB', (xRes, yRes))

	# Get what data we can find [JSON]
	print("Grabbing card data...")
	cards = getCardData()

	# Generate 'cards' for each of them, (xRes)x320
	top = 0

	padding = 20 # Easier customization
	textFill = "white" # should probably make dynamic
	numCards = 5
	fontSizeSrc = 30
	fontFile = "/usr/share/fonts/noto/NotoSans-Regular.ttf"
	fontSize1 = 100
	fontSize2 = 50

	for card in cards:
		# Draw background

		draw = ImageDraw.Draw(image)
		draw.rectangle([(0, top),(xRes, top+(yRes/numCards))], fill=card.backgroundColor, outline="white")
		draw.text((padding, top+padding), card.sourceName, fill=textFill, font=ImageFont.truetype(font=fontFile, size=fontSizeSrc))
		draw.text((padding, top+padding+padding/2+fontSizeSrc), card.primaryText, fill = textFill, font=ImageFont.truetype(font=fontFile, size=fontSize1))
		draw.text((padding, top+padding+padding/2+fontSizeSrc+padding/2+fontSize1), card.secondaryText, fill = textFill, font=ImageFont.truetype(font=fontFile, size=fontSize2))
		top+=yRes/numCards

	# Place small placeholder at the bottom for things that failed, if more than can fit just show number+log, if fits show all

	image.save("SmartFramePhoto.png")


# -- MAIN --
def main():
	argc = len(sys.argv)

	if argc > 1:
		if sys.argv[1] == "-h" or sys.argv[1] == "--help":
			getHelp()
		if argc > 2:
			try:
				xRes = int(sys.argv[1])
				yRes = int(sys.argv[2])
			except ValueError:
				throwErr("given argument is not a number!")
			print("Resolution set: " + str(xRes) + "x" + str(yRes))
			genPhoto(xRes, yRes)
		else:
			throwErr("Unrecognized argument.")

	else:
		print("Assuming a default resolution of 720x1280:")
		genPhoto(720, 1280)

if __name__ == "__main__":
	main()