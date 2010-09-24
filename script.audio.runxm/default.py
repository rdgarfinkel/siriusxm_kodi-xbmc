# RunXM - This is a python script to access xm online streams.

RunXMDate="04/09/2010"
version="0.19"

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import xbmc
import xbmcgui
import threading
import time
import urllib
import re
import os
from XmLib import * 
import sys
import traceback

ACTION_PREVIOUS_MENU = 10

class MainClass(xbmcgui.Window):
	def __init__(self):
		screenX = self.getWidth()
		screenY = self.getHeight()
		#print "screen width"
		#print screenX
		#print "screen height"
		#print screenY
		fontSize = "font12"
		if screenX > 750:
			userbuttonheight = 30
			userbuttonlength = 140
			userbuttonfromtop = 200
		else:
			userbuttonheight = 20
			userbuttonlength = 100
			userbuttonfromtop = 100

		self.base_path = os.getcwd().replace(';','')

		#find XBMC script location, and the "data" folder underneath it; create it if it doesn't exist
		dir = os.path.join(self.base_path, 'data')
		if not os.path.exists(dir):
			os.mkdir(dir)

		#find the "login.txt" file to create the file storing the username/password
		path = os.path.join(dir, 'login.txt')

		##if the file doesn't exist, create it. most likely this will be a new installation
		if not os.path.isfile(path):
			dialog = xbmcgui.Dialog()
			dialog.ok("Login Required", "A valid username and password are required.\nPlease enter your XM Radio Username and Password\nin the following prompts, then restart RunXM.")

			username = xbmc.Keyboard("Username","XM Radio Online Username")
			username.doModal()
			if (username.isConfirmed()):
				userwrite = username.getText() + "|"
				print userwrite

			password = xbmc.Keyboard("Password","XM Radio Online Password")
			password.doModal()
			if (password.isConfirmed()):
				passwrite = password.getText() + "|"
				print passwrite

			history_list = userwrite + passwrite

			try:
				f = open(path, 'w')
				f.write(history_list)
				f.close()
			except IOError:
				pass

			print "file contents"
			print file(path).read()

			dialog = xbmcgui.Dialog()
			dialog.ok("Changes Saved!", "Username and Password Saved.\nTo change your username and password later,\ngo to the Change Login button on the left.\nPlease restart RunXM to begin listening.")
			self.text = xbmcgui.ControlLabel(int(screenX * .3),
											int(screenY * .2),
											int(screenX * .6),
											int(screenY * .75),
											fontSize,
											'0xFFFFFF00')
			self.addControl(self.text)
			self.close()


		else:
			path = os.path.join(dir, 'login.txt')
			f=open(path, 'r')
			LOGIN=f.readline()
			splitlogin=str(LOGIN)
			USERNAME,PASSWORD,EOL = splitlogin.split('|')
			f.close()
			#print "username: " + USERNAME
			#print "password: " + PASSWORD

			#self.addControl(xbmcgui.ControlImage(0,0,screenX,screenY,os.path.abspath(self.base_path + "\\images\\background.png")))
			self.lastAlbum = ''


			self.list = xbmcgui.ControlList(int(screenX * .3),
											int(screenY * .2),
											int(screenX * .6),
											int(screenY * .75),
											fontSize)
			self.addControl(self.list)

			self.userButton = xbmcgui.ControlButton(50, userbuttonfromtop, userbuttonlength, userbuttonheight, 'Change Login')
			self.addControl(self.userButton)

			self.about = xbmcgui.ControlButton(50, (userbuttonfromtop+35), userbuttonlength, userbuttonheight, 'About')
			self.addControl(self.about)

			self.userButton.controlRight(self.list)
			self.userButton.controlDown(self.about)

			self.about.controlRight(self.list)
			self.about.controlUp(self.userButton)

			self.list.controlLeft(self.userButton)

			self.xm = XmSubscriber.XmInterface(USERNAME, PASSWORD)
			self.populateCats()
			self.setFocus(self.list)
		
	def onAction(self, action):
		if action.getButtonCode() == 275:
			self.close()
	
	def onControl(self, control):
		if control == self.about:
			dialog = xbmcgui.Dialog()
			#text = "RunXM Version" + str(version) + "\nXM Channel Listings Updated" + str(XmBase.XmBaseDate)
			dialog.ok("About RunXM " + str(version), "RunXM Compile Date: " + str(RunXMDate) + "\nSirius/XM Channels Updated: " + str(XmBase.XmBaseDate))
					
		if control == self.userButton:
			self.base_path = os.getcwd().replace(';','')
			dir = os.path.join(self.base_path, 'data')
			path = os.path.join(dir, 'login.txt')

			f=open(path, 'r')
			LOGIN=f.readline()
			splitlogin=str(LOGIN)
			USERNAME,PASSWORD,EOL = splitlogin.split('|')
			f.close()

			dialog = xbmcgui.Dialog()
			dialog.ok("Editing XM Radio Login", "Changing current username and password.\nPlease edit your XM Radio Username and Password\nin the following prompts, then restart RunXM.")

			username = xbmc.Keyboard(USERNAME,"XM Radio Online Username")
			username.doModal()
			if (username.isConfirmed()):
				userwrite = username.getText() + "|"

			password = xbmc.Keyboard(PASSWORD,"XM Radio Online Password")
			password.doModal()
			if (password.isConfirmed()):
				passwrite = password.getText() + "|"

			history_list = userwrite + passwrite

			dir = os.path.join(self.base_path, 'data')
			if not os.path.exists(dir):
				os.mkdir(dir)
			path = os.path.join(dir, 'login.txt')

			f = open(path, 'w')
			f.write(history_list)
			f.close()

			print "file contents"
			print file(path).read()

			dialog = xbmcgui.Dialog()
			dialog.ok("Changes Saved!", "Username and Password Saved.\nPlease restart RunXM, then enjoy listening!")

		if control == self.list:
			if self.curMode == "cats":
				self.xm.setCategory(self.list.getSelectedItem().getLabel())
				self.populateGenres()
			elif self.curMode == "genres":
				if self.list.getSelectedPosition() == 0:
					self.populateCats()
				else:
					self.xm.setGenre(self.list.getSelectedItem().getLabel())
					self.populateChannels()
			elif self.curMode == "channels":
				if self.list.getSelectedPosition() == 0:
					self.populateGenres()
				else:
					self.xm.setChannel(self.channels[self.list.getSelectedPosition() - 1])
					self.curMode = "playing"
					self.list.reset()
					self.list.addItem("Loading - Please Wait...")
					xmURL = self.xm.getChannelURL()
					if xmURL == -1:
						dialog = xbmcgui.Dialog()
						dialog.ok("Login Error", "Error logging in to XM.\nPlease double check your username and password.")
					else:
						try:
							xbmc.Player().play(xmURL)
							if xbmc.Player().isPlaying():
								popup = PlayingStream()
								popup.setXm(self.xm)
								popup.doModal()
								del popup
							xbmc.Player().stop()
						except:
							print formatExceptionInfo()
							dialog = xbmcgui.Dialog()
							dialog.ok("Media Error", 
									"Apparently XBMC had a problem opening this item.\nPlease try again or try another channel.")
					self.populateChannels()
			
	

	def populateCats(self):
		self.curMode = "cats"
		self.list.reset()
		cats = self.xm.getCategoryList()
		for i in range(0, len(cats)):
			self.list.addItem(cats[i])


	def populateGenres(self):
		self.curMode = "genres"
		self.list.reset()
		self.list.addItem(".. Back to Categories")
		genres = self.xm.getGenreList()
		for i in range(0, len(genres)):
			self.list.addItem(genres[i])


	def populateChannels(self):
		self.curMode = "channels"
		self.list.reset()
		self.list.addItem(".. Back to Genres")
		self.channels = self.xm.getChannelList()
		for i in range(0, len(self.channels)):
			self.list.addItem(self.channels[i]['number'] + ' - ' + self.channels[i]['text'] + ': ' + self.channels[i]['desc'])


class PlayingStream(xbmcgui.Window):
	def __init__(self):
		screenX = self.getWidth()
		screenY = self.getHeight()
		self.base_path = os.getcwd().replace(';','')

		#self.addControl(xbmcgui.ControlImage(0,0,screenX,screenY,os.path.abspath(self.base_path + "\\images\\background.png")))
		fontSize = "font12"
		self.StationLabel = xbmcgui.ControlLabel(int(screenX * .3),
												int(screenY * .2),
												int(screenX * .5),
												120, "", fontSize, "0xFFFFFFFF")
		self.ArtistLabel = xbmcgui.ControlLabel(int(screenX * .3),
												int((screenY * .2) * 1.25),
												int(screenX * .75),
												100, "", "font13", "0xFFFFFFFF")
		self.SongLabel = xbmcgui.ControlLabel(int(screenX * .3),
												int((screenY * .2) * 1.5),
												int(screenX * .75),
												100, "", "font13", "0xFFFFFFFF")
		self.AlbumLabel = xbmcgui.ControlLabel(int(screenX * .3),
											int((screenY * .2) * 1.75),
											int(screenX * .75),
											100, "", "font13", "0xFFFFFFFF")
		self.addControl(self.StationLabel)
		self.addControl(self.ArtistLabel)
		self.addControl(self.SongLabel)
		self.addControl(self.AlbumLabel)
		self.stopCount = 0

	
	def setXm(self, xm):
		screenX = self.getWidth()
		screenY = self.getHeight()
		self.base_path = os.getcwd().replace(';','')

		self.xm = xm
		self.channel = self.xm.getChannel()
		## check to see if a channel image is present, if not use generic "XM Radio" image
		destFile = self.base_path + "\\images\\" + str(self.channel['number']) + ".jpg"
		if os.path.isfile(destFile):
			pass
		else:
			destFile = self.base_path + "\\images\\xmradio.gif"
		#print destFile

		if screenX > 1050:
			channelimageX = screenX*.8
			channelimageY = screenY*.1
			albumimageX = screenX*.05
			albumimageY = screenY*.6
			albumimagesizeX = 250
			albumimagesizeY = 250
		elif screenX > 750:
			channelimageX = screenX*.8
			channelimageY = screenY*.1
			albumimageX = screenX*.05
			albumimageY = screenY*.6
			albumimagesizeX = 200
			albumimagesizeY = 200
		else:
			channelimageX = screenX*.7
			channelimageY = screenY*.08
			albumimageX = screenX*.05
			albumimageY = screenY*.6
			albumimagesizeX = 150
			albumimagesizeY = 150

		self.StationImage = xbmcgui.ControlImage(int(channelimageX), int(channelimageY), 138, 50, destFile) 
		self.addControl(self.StationImage)

		#put up an empty image first
		#albumFile = os.path.abspath(self.base_path + "\\images\\album.jpg")
		#self.AlbumImage = xbmcgui.ControlImage(int(albumimageX), int(albumimageY), albumimagesizeX, albumimagesizeY, albumFile) 
		#self.addControl(self.AlbumImage)				       

		#print "image size X"
		#print albumimagesizeX
		#print "image size Y"
		#print albumimagesizeY
		self.StationLabel.setLabel("XM Radio Online, " + str(self.channel['text']))

		#self.BiographyTEXT = xbmcgui.ControlTextBox((int(screenX * .3)),(int((screenY * .2) * 2.25)),int(screenY),(int(screenX * .3)),"font12")
		#self.addControl(self.BiographyTEXT)

		self.ut = UpdateTime(25, self)
		self.ut.start()

	
	def onAction(self, action):
		if (action == ACTION_PREVIOUS_MENU) and (self.stopCount == 0):
			self.stopCount = 1
			self.ut.stopThread()
			self.StationLabel.setLabel("")
			self.ArtistLabel.setLabel("Please wait briefly while the cached audio plays")
			self.SongLabel.setLabel("itself out, and things are cleaned up.")
			self.AlbumLabel.setLabel("")
			#self.BiographyTEXT.setText("")
			self.ut.join()
			self.close()


	def updateSong(self):
		songData = self.xm.getSongInfo()
		screenX = self.getWidth()
		screenY = self.getHeight()
		self.base_path = os.getcwd().replace(';','')

		if screenX > 1050:
			albumimageX = screenX*.05
			albumimageY = screenY*.6
			albumimagesizeX = 250
			albumimagesizeY = 250
		elif screenX > 750: 
			albumimageX = screenX*.05
			albumimageY = screenY*.6
			albumimagesizeX = 200
			albumimagesizeY = 200
		else:
			albumimageX = screenX*.05
			albumimageY = screenY*.6
			albumimagesizeX = 150
			albumimagesizeY = 150

		self.ArtistLabel.setLabel("Artist: " + songData['artist'])
		self.SongLabel.setLabel("Song: " + songData['title'])
		self.AlbumLabel.setLabel("Album: " + songData['album'])
		#if (songData['albumURL'] != ""):
		#	#albumcover.jpg is the image downloaded
		#	destFile = os.path.abspath(self.base_path + "\\images\\albumcover.jpg")
		#	try:
		#		pass
		#		#urllib.urlretrieve(songData['albumURL'], destFile)
		#	except:
		#		print formatExceptionInfo()
		#		#dialog = xbmcgui.Dialog()
		#		#dialog.ok("Error Downloading Album Image", 
		#		#			"Could not download Album Image")
		#else:
		#	if songData['albumURL'] == '':
		#		#album.jpg is a blank image
		#		destFile = os.path.abspath(self.base_path + "\\images\\album.jpg")

		#self.AlbumImage = xbmcgui.ControlImage(int(albumimageX), int(albumimageY), albumimagesizeX, albumimagesizeY, destFile)
		#self.addControl(self.AlbumImage)
		self.lastAlbum = songData['album']

		#biography = "Sorry, the biography of this artist cannot be displayed. This may happen if the artist listing displays multiple artists, or there is no biography listed on Yahoo! Music."

		#self.base_path = os.getcwd().replace(';','')

		##find XBMC script location, and the "data" folder underneath it; create it if it doesn't exist
		#dir = os.path.join(self.base_path, 'data')
		#if not os.path.exists(dir):
		#	os.mkdir(dir)

		##find the "bio.txt" file to create the file storing the biography
		#path = os.path.join(dir, 'bio.txt')

		##if the file doesn't exist, create it
		#if not os.path.isfile(path):
		#	f=open(path, 'w')
		#	f.write("Artist|Bio|")
		#	f.close()
		#f=open(path, 'r')
		#TEMP=f.readline()
		#BIOTEMP=str(TEMP)
		#ARTISTNAME,BIO = BIOTEMP.split('|')
		#f.close()

		## this is the code to show the artist biography... it looks funky here, i know

		## the following line prevents the text box from overwriting itself when an update comes around
		## it checks to see if the current artist is the same as before, if it is not it will run

		## **this works 99.9% of the time; if the last artist in a stream is the first artist in another, there won't be a biography displayed**

		#if (songData['artist'] != ARTISTNAME):
		##	create the search parameters of Yahoo! Music
		#	search = urllib.urlencode({'m':'all','p':songData['artist']})

		##	what is the URL of the search engine? (this seems to only work with engines that pass information through the web address, fyi)
		#	artistURL = urllib.urlopen("http://search.music.yahoo.com/search/?" + search)
		#	print "http://search.music.yahoo.com/search/?" + search

		##	we need to open the results from above
		#	SearchHTML = artistURL.read()

		##	now, look for this "target" text in the page, which will give you the artist ID number Yahoo! Music uses
		#	target = '<a href="http://music.yahoo.com/ar-'

		##	if the "target" is found continue on...
		#	if SearchHTML.find(target) != -1:
		#		SearchHTML = SearchHTML[SearchHTML.find(target) + len(target) :]

		##		now strip all of the page to only the text above and below, then assign it to 'data'

		#		data = SearchHTML[: SearchHTML.find('---')]
		#		print data

		##		now, take the stripped 'data,' go to the biography page, then strip out the pages' biography into 'BioHTML'
		#		if (data):
		#			artistBIO = urllib.urlopen("http://music.yahoo.com/ar-" + data + "-bio--")
		#			print "http://music.yahoo.com/ar-" + data + "-bio--"
		#			BioHTML = artistBIO.read()

		##			yahoo music uses "<td>" throughout the whole page, and these "targets" always look for the first occurance
		##			for this usage, the first one isn't what is needed, it's actually the fifth or sixth
		##			so, again, find the target below, then strip it into 'rawHTML'
		#			target = '<div class="ymusic-text-article bio-body">'
		#			if BioHTML.find(target) != -1:
		#				BioHTML = BioHTML[BioHTML.find(target) + len(target) :]
		#				rawHTML = BioHTML[: BioHTML.find('</div>')]
		#				print rawHTML

		#				target = '       '
		#				if rawHTML.find(target) != -1:
		#					biography = rawHTML[rawHTML.find(target) + len(target) :]
		#					biography = str(biography)
		#					biography = re.sub('<P>', '\n ', biography)
		#					biography = re.sub('</P>', ' ', biography)
		#					biography = re.sub('<p>', '\n', biography)
		#					biography = re.sub('</p>', ' ', biography)
		#					biography = re.sub('<B>', '\n ', biography)
		#					biography = re.sub('</B>', ' ', biography)
		#					biography = re.sub('<b>', '\n', biography)
		#					biography = re.sub('</b>', ' ', biography)
		#					biography = re.sub('<I>', '\n ', biography)
		#					biography = re.sub('</I>', ' ', biography)
		#					biography = re.sub('<i>', '\n', biography)
		#					biography = re.sub('</i>', ' ', biography)
		#					biography = re.sub('<BR>', '\n\n', biography)
		#					biography = re.sub('<br>', '\n\n', biography)
		#					biography = re.sub('<a.*?>', '', biography)
		#					biography = re.sub('</a>', '', biography)
		#					print biography

		##					  this takes the artist and biography and stores it under the 'data' folder as 'bio.txt'
		##					  this lets you read thru the biography without interruption once an artist/song update occurs every 25 seconds
		#					self.base_path = os.getcwd().replace(';','')
		#					dir = os.path.join(self.base_path, 'data')
		#					path = os.path.join(dir, 'bio.txt')
		#					WRITEBIO = open(path, 'w')
		#					WRITEBIO.write(songData['artist'] + '|' + biography)
		#					WRITEBIO.close()

		#	self.BiographyTEXT.setText(biography)
		##	set biography to what was just downloaded
		#	self.setFocus(self.BiographyTEXT)
			

class UpdateTime(threading.Thread):
	def __init__(self, seconds, object):
		self.runTime = seconds
		self.object = object
		self.go = 1
		threading.Thread.__init__(self)

	def run(self):
		while self.go == 1:
			try:
				self.object.updateSong()
			except:
				print formatExceptionInfo()
			time.sleep(self.runTime)
	
	def stopThread(self):
		self.go = 2;


def formatExceptionInfo(maxTBlevel = 5):
	cla, exc, trbk = sys.exc_info()
	excName = cla.__name__
	try:
		excArgs = exc.__dict__["args"]
	except KeyError:
		excArgs = "<no args>"
	excTb = traceback.format_tb(trbk, maxTBlevel)
	return (excName, excArgs, excTb)

	
mydisplay = MainClass()
mydisplay.doModal()
del mydisplay