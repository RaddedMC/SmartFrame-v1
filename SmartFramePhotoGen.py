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

def throwErr(msg, code):
	print("Error: " + msg)
	exit(code)

def throwErr(msg):
	throwErr(msg, 5)	

# -- MAIN --
def main():
	# Help, Resolution
	argc = len(sys.argv)
	if argc > 1:
		if sys.argv[1] == "-h" or sys.argv[1] == "--help":
			print("HELP!")
			exit()
		if argc > 2:
			print("Resolution set: " + sys.argv[1] + "x" + sys.argv[2])
		else:
			throwErr("Unrecognized argument.")
	else:
		print("Assuming a default resolution of 1280x800:")

if __name__ == "__main__":
	main()