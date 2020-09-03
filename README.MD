**RaddedMC's Project SmartFrame**

- Dependencies:
	- pychromecast for Chromecast integration
	- phue for Hue integration
	- Pillow to draw image
	- **Python 3**
	
- Setup:
	- Create your own bash script to run in the background on whatever device you want to drive your photo frame, or use mine (FrameScript.sh, run as root with BASH) and make the necessary modifications
	- To put a notification, create a file using any program under the Notifications/ directory with 3 lines of text:
		- Filename is top 'source name' line
		- First line is large text, recommend 20 characters max
		- Second line is secondary text, recommend 40 characters max
		- Third line is number of updates to keep the notification for
		- If the file is invalid or the notification is expired, the program will continue and delete the file.
		- I used this notification system to integrate my random message board (https://forms.gle/cARq91Krjp5nDgNG8) and storage usage from my server. I recommend using SCP to get a remote computer to add a notification file 
		- See sample notification file for more details
		
- File deets:
	- Card.py: The class that stores the data to be converted to a photo
	- GetCardData.py: The function that grabs the data from the internet, separated to keep the image generation code which won't be modified much and the data pulling code which will probably vary from user to user in two different places. Feel free to modify this function to fit your needs, just keep in mind that only 6 cards will show up by default.
	- SmartFramePhotoGen.py: The main file for this project, which also contains the image generation code. Feel free to modify this to fit your needs, it also takes two arguments for a custom x and y resolution if you want. My S-frame is around 600x1280 (vertical), so that's the default.
	
Feel free to dm me on Insta @RaddedMC or Discord at RaddedMC#4791 for any questions, also check out my video showing off my setup with SmartFrame: https://youtu.be/YDr95xaEsK4
