#!/bin/env python

# Get data from:
	# Calendar
	# Google Keep
	# Last screen of RPI and SolidServ
	# Notifications from RPI and SolidServ

# Throw that into an image
	# User-selectable resolution

# -- IMPORTS --
import sys #Python official, required for arguments
from PIL import Image, ImageDraw, ImageFont

import Card #Card class, required
import GetCardData
import os




# -- SOME GLOBALS --
defX = 760
defY = 1280




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
	print("Usage: SmartFramePhotoGen.py [x-resolution] [y-resolution]\nDefault resolution is " + str(defX) + " x " + str(defY) + ". For help with specific sections, check out the README.MD")
	exit(0)
	#TODO: ADD MORE TO THIS




# -- GENPHOTO --
def genPhoto(xRes = defX, yRes = defY):
	image = Image.new('RGB', (xRes, yRes))

	# Get what data we can find
	print("Grabbing card data...")
	cards = GetCardData.getCardData()
	print("Data recieved. Drawing photo:")


	# Generate 'cards' for each of them, (xRes)x320
	top = 0

	padding = 20 # Easier customization
	textFill = "white" # should probably make dynamic
	cardOutline = "white"
	numCards = 6
	fontSizeSrc = 25
	fontFile = "/usr/share/fonts/noto/NotoSans-Regular.ttf"
	fontSize0 = 140
	fontSize1 = 70
	fontSize2 = 40
	numhuecards = 0
	numicloudcards = 0

	for i in range(0,len(cards)):
		card = cards[i]
		# Draw background

		draw = ImageDraw.Draw(image)

		# Clock
		if card.sourceName == "Current Time":
			draw.text((padding*5, top+padding*3), card.primaryText, fill=textFill, font=ImageFont.truetype(font=fontFile, size=fontSize0))
			draw.text((padding*5, top+padding), card.secondaryText, fill = textFill, font=ImageFont.truetype(font=fontFile, size=fontSize2))
			top+=(yRes/numCards)+padding*2

		# Spotify
		elif card.sourceName[0:7] == "Spotify":
			draw.rectangle([(0, top),(xRes, ((top+(yRes/numCards)/2)-1))], fill=card.backgroundColor, outline=cardOutline)
			draw.text((padding, top+padding/2), card.sourceName[10:], fill=textFill, font=ImageFont.truetype(font=fontFile, size=fontSizeSrc))
			draw.text((padding, top+padding*2), card.primaryText + " - " + card.secondaryText, fill=textFill, font=ImageFont.truetype(font=fontFile, size=fontSize2))
			top+=yRes/(numCards*2)
			
		# Hue
		elif card.sourceName == "Philips Hue":
			draw.rectangle([(padding+numhuecards*(xRes/4), top+(padding/2)-numhuecards*(top+(padding/2)+xRes/8 - top+(padding/2))),(padding/2+numhuecards*(xRes/4)+(xRes/4), top+(padding/2)+xRes/8)], fill=card.backgroundColor, outline=cardOutline)
			draw.text((padding+numhuecards*(xRes/4)+padding/2, (top+(padding/2)+padding/2)), card.secondaryText[0:12], fill=textFill, font=ImageFont.truetype(font=fontFile, size=fontSizeSrc))
			draw.text((padding+numhuecards*(xRes/4)+padding/2, (top+(padding/2)+padding/2)+30), card.primaryText, fill=textFill, font=ImageFont.truetype(font=fontFile, size=fontSize2))
			numhuecards+=1			
			try:
				if not cards[i+1].sourceName == "Philips Hue":
					top+= top+(padding/2)+xRes/8 - top+(padding/2)
			except IndexError: 
				top+= top+(padding/2)+xRes/8 - top+(padding/2)
			
		# iDevice
		elif card.primaryText.endswith("Battery"):
			draw.rectangle([(padding+numicloudcards*(xRes/4), top+(padding/2)),(padding/2+numicloudcards*(xRes/4)+(xRes/4), top+(padding/4)+xRes/4)], fill=card.backgroundColor, outline=cardOutline)
			draw.text((padding+numicloudcards*(xRes/4)+padding/2, (top+(padding/2)+padding/2)+20), card.primaryText[0:3], fill=textFill, font=ImageFont.truetype(font=fontFile, size=fontSize1))
			draw.text((padding+numicloudcards*(xRes/4)+padding/2, (top+(padding/2)+115)), card.primaryText[3:], fill=textFill, font=ImageFont.truetype(font=fontFile, size=fontSizeSrc))
			draw.text((padding+numicloudcards*(xRes/4)+padding/2, (top+(padding/2)+144)), card.secondaryText, fill=textFill, font=ImageFont.truetype(font=fontFile, size=fontSizeSrc))
			draw.text((padding+numicloudcards*(xRes/4)+padding/2, (top+(padding/2))), card.sourceName[0:12], fill=textFill, font=ImageFont.truetype(font=fontFile, size=fontSizeSrc))
			numicloudcards+=1
			try:
				if not cards[i+1].primaryText.endswith("Battery"):
					top+= (padding/2)+xRes/4
			except IndexError: 
				top+= (padding/2)+xRes/4
			
		# Other
		else:
			draw.rectangle([(0, top),(xRes, top+(yRes/numCards))], fill=card.backgroundColor, outline=cardOutline)
			draw.text((padding, top+padding), card.sourceName, fill=textFill, font=ImageFont.truetype(font=fontFile, size=fontSizeSrc))
			draw.text((padding, top+padding+padding/2+fontSizeSrc), card.primaryText, fill = textFill, font=ImageFont.truetype(font=fontFile, size=fontSize1))
			draw.text((padding, top+padding+padding+fontSizeSrc+padding/2+fontSize1), card.secondaryText, fill = textFill, font=ImageFont.truetype(font=fontFile, size=fontSize2))
			top+=yRes/numCards
		
		if not card.imageDir == 'nope':
			try:
				os.remove(card.imageDir)
			except FileNotFoundError:
				print("Unable to delete cached image for " + card.sourceName + "! This could cause issues in the future.")
		print("Finished card " + card.sourceName)

	# Place small placeholder at the bottom for things that failed, if more than can fit just show number+log, if fits show all

	image.save("SmartFramePhoto.jpg")
	print("Photo drawn. Saving to SmartFramePhoto.jpg")


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
		print("Assuming a default resolution of " + str(defX) + "x" + str(defY) + ":")
		genPhoto()

if __name__ == "__main__":
	main()
