#!/bin/env python

# Get data from:
	# Spotify
	# Google Cast
	# Smart devices
		# preferably IFTTT
	# Calendar
	# Time
	# Date
	# Google Keep
	# Last screen of RPI and SolidServ
	# Notifications from RPI and SolidServ

# Throw that into an image
	# User-selectable resolution

# -- IMPORTS --
import sys
from PIL import Image


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
	# Data code here...
	image.save("SmartFrame.png")


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
		print("Assuming a default resolution of 1280x800:")
		genPhoto(1280, 800)

if __name__ == "__main__":
	main()