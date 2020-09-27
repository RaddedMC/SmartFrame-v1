# -- IMPORTS --
import Card #Card class, required

import datetime #Needed for datetime card





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


	print("Data ready.")
	return cards
