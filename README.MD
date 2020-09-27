**RaddedMC's Project SmartFrame**

- Dependencies:
	- pychromecast for Chromecast integration
	- phue for Hue integration, check out https://github.com/studioimaginaire/phue for setup plus you need a hue-ip-addr file in the SmartFrame folder containing your bridge's IP Address
	- Pillow to draw image
	- **Python 3**
	- spotipy for Spotify integration, you need to get an API client ID and client Secret. Set your redirect URI to http://127.0.0.1:9090 and put your Spotify username, client-id, and client-secret into a file named spotify-user (in that order) in the SmartFrame folder, seperated by line breaks. You'll also need a web browser installed on your system to sign into your account and get an OAuth token. If you're running headless like I am, download a small browser like surf and forward X from your server to your remote access client.
	- wget to download photos, used in spotify integration
	- colorgram to get color from Spotify album art
	- *everything above can be installed with 'pip install \[thing\]'
	
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

Note: This program assumes that you are controlling your photo frame with rasbian and that your username is 'pi'.
	
Feel free to dm me on Insta @RaddedMC or Discord at RaddedMC#4791 for any questions, also check out my video showing off my setup with SmartFrame: https://youtu.be/YDr95xaEsK4
