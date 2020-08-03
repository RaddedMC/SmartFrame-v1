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




# -- GENPHOTO --
def genPhoto(xRes, yRes):
	image = Image.new('RGB', (xRes, yRes))

	# Get what data we can find [JSON]
	print("Grabbing card data...")
	cards = GetCardData.getCardData()
	print("Data grabbed. Drawing photo:")

	# Generate 'cards' for each of them, (xRes)x320
	top = 0

	padding = 20 # Easier customization
	textFill = "white" # should probably make dynamic
	numCards = 5
	fontSizeSrc = 30
	fontFile = "/usr/share/fonts/noto/NotoSans-Regular.ttf"
	fontSize1 = 90
	fontSize2 = 50

	for card in cards:
		# Draw background

		draw = ImageDraw.Draw(image)
		draw.rectangle([(0, top),(xRes, top+(yRes/numCards))], fill=card.backgroundColor, outline="white")
		draw.text((padding, top+padding), card.sourceName, fill=textFill, font=ImageFont.truetype(font=fontFile, size=fontSizeSrc))
		draw.text((padding, top+padding+padding/2+fontSizeSrc), card.primaryText, fill = textFill, font=ImageFont.truetype(font=fontFile, size=fontSize1))
		draw.text((padding, top+padding+padding+fontSizeSrc+padding/2+fontSize1), card.secondaryText, fill = textFill, font=ImageFont.truetype(font=fontFile, size=fontSize2))
		top+=yRes/numCards

	# Place small placeholder at the bottom for things that failed, if more than can fit just show number+log, if fits show all

	image.save("SmartFramePhoto.png")
	print("Photo drawn. Saving to SmartFramePhoto.png")


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