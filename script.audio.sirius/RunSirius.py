# RunSirius - This is a python script to access sirius' online streams.
# Make sure to set your username and password!

# Originally from http://www.sacknet.org/sirius/ (Mike Rosack - 09/30/2006) 1.2

# Version 1.3 9/4/2008

# 

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

import xbmc, xbmcgui
import threading
import time
import urllib
import os
from os import path
from SiriusLib import * 
import sys
import traceback

# SET ME!  SET ME!  SET ME!
USERNAME = ""
PASSWORD = ""

#globSir = SiriusSubscriber.SiriusInterface(USERNAME, PASSWORD)
# If you want to use a guest account...
globSir = SiriusGuest.SiriusInterface(USERNAME, PASSWORD)

DIR = os.getcwd()
CACHE_DIR = DIR + "\\cache"
ACTION_PREVIOUS_MENU = 10
CURRENT_VERSION = "1.3"


class MenuWindow(xbmcgui.Window):
        def __init__(self):
                self.screenX = self.getWidth()
                self.screenY = self.getHeight()
                fontSize = "font12"
                if self.screenX > 750:
                        fontSize = "font13"
                self.list = xbmcgui.ControlList(int(self.screenX * .2),
                                                                                int(self.screenY * .2),
                                                                                int(self.screenX * .6),
                                                                                int(self.screenY * .6),
                                                                                fontSize)
                self.addControl(self.list)

                #self.captchaButton = xbmcgui.ControlButton(50, 200, 80, 30, 'Captcha')
                #self.addControl(self.captchaButton)

                #self.list.controlLeft(self.captchaButton)

                self.setFocus(self.list)
        
        def setSirius(self, sir):
                self.sir = sir
                self.populateCats()
                
        def onAction(self, action):
                if action == ACTION_PREVIOUS_MENU:
                        self.close()
        
        def onControl(self, control):
                #if control == self.captchaButton:
                #        popup = LoginWindow()
                #        popup.setSirius(self.sir)
                #        popup.doModal()
                #        del popup

                if control == self.list:
                        if self.curMode == "cats":
                                self.sir.setCategory(self.list.getSelectedItem().getLabel())
                                self.populateGenres()
                        elif self.curMode == "genres":
                                if self.list.getSelectedPosition() == 0:
                                        self.populateCats()
                                else:
                                        self.sir.setGenre(self.list.getSelectedItem().getLabel())
                                        self.populateChannels()
                        elif self.curMode == "channels":
                                if self.list.getSelectedPosition() == 0:
                                        self.populateGenres()
                                else:
                                        self.sir.setChannel(self.channels[self.list.getSelectedPosition() - 1])
                                        self.curMode = "playing"
                                        self.list.reset()
                                        self.list.addItem("Loading - Please Wait...")
                                        sirURL = self.sir.getChannelURL()
                                        if sirURL == -1:
                                                dialog = xbmcgui.Dialog()
                                                dialog.ok("Login Error", "Couldn't login to Sirius.  Please check your username / password.")
                                        else:
                                                try:
##                                      You can set this path below to whatever matches your location
                                                        text_file = open(DIR + "\\sirius.strm", "w")
                                                        text_file.write (sirURL)
                                                        text_file.close()
                                                        sirPlay = DIR + '\\sirius.strm'
                                                        xbmc.PlayList(0).load(sirPlay)
                                                        xbmc.Player().play()
                                                        
                                                        if xbmc.Player().isPlaying():
                                                                popup = PlayingStream()
                                                                popup.setSirius(self.sir)
                                                                popup.doModal()
                                                                del popup
                                                        xbmc.Player().stop()
                                                except:
                                                        print formatExceptionInfo()
                                                        dialog = xbmcgui.Dialog()
                                                        dialog.ok(sirPlay, 
                                                                        "Apparently XBMC has problems playing this type of URL.  Hopefully this will work in the future. :(")
                                        self.populateChannels()
                        
        

        def populateCats(self):
                self.curMode = "cats"
                self.list.reset()
                cats = self.sir.getCategoryList()
                for i in range(0, len(cats)):
                        self.list.addItem(cats[i])


        def populateGenres(self):
                self.curMode = "genres"
                self.list.reset()
                self.list.addItem(".. Back to Categories")
                genres = self.sir.getGenreList()
                for i in range(0, len(genres)):
                        self.list.addItem(genres[i])


        def populateChannels(self):
                self.curMode = "channels"
                self.list.reset()
                self.list.addItem(".. Back to Genres")
                self.channels = self.sir.getChannelList()
                for i in range(0, len(self.channels)):
                        self.list.addItem(self.channels[i]['number'] + ' - ' + self.channels[i]['text'] + ': ' + self.channels[i]['desc'])


class LoginWindow(xbmcgui.Window):
        def __init__(self):
                self.screenX = self.getWidth()
                self.screenY = self.getHeight()
                self.capAns = ""
                fontSize = "font12"
                if self.screenX > 750:
                        fontSize = "font13"

                self.CaptchaDesc = xbmcgui.ControlLabel(int(self.screenX * .2),
                                                                                                int(self.screenY * .15),
                                                                                                int(self.screenX * .5),
                                                                                                100, "", fontSize, "0xFFFFFFFF")
                self.CaptchaDesc.setLabel("Enter the text as shown below:")


		self.base_path = os.getcwd().replace(';','')
		dir = os.path.join(self.base_path, 'cache')
		path = os.path.join(dir, 'captcha.txt')
		print "accessing " + path
		f = open(path,'r')
		f.seek(0)
		f.read()
		str = f.read()
		f.close()
		print str

                self.Captcha = xbmcgui.ControlLabel(int(self.screenX * .2),
                                                                                                int(self.screenY * .25),
                                                                                                int(self.screenX * .5),
                                                                                                100, "", "font45", "0xFFFFFFFF")
                self.Captcha.setLabel("Test")

                self.CaptchaAnswer = xbmcgui.ControlLabel(int(self.screenX * .2),
                                                                                                int(self.screenY * .4),
                                                                                                int(self.screenX * .6),
                                                                                                100, "", fontSize, "0xFFFFFFFF")
                self.CaptchaAnswer.setLabel("Your entry:")

                self.button0 = xbmcgui.ControlButton(int(self.screenX * .2),
                                                                                        int(self.screenY * .8),
                                                                                        200, 30, "Enter Text")
                self.button1 = xbmcgui.ControlButton(int(self.screenX * .5),
                                                                                        int(self.screenY * .8),
                                                                                        200, 30, "Login")
                
                self.addControl(self.CaptchaDesc)
                self.addControl(self.CaptchaAnswer)
                self.addControl(self.Captcha)
                self.addControl(self.button0)
                self.addControl(self.button1)
                self.button0.controlRight(self.button1)
                self.button1.controlLeft(self.button0)
                self.setFocus(self.button0)
        
        def onAction(self,action):
                if(action == ACTION_PREVIOUS_MENU):
                        self.close()
        
        def onControl(self,control):
                if(control == self.button0):
                        keyboard = xbmc.Keyboard()
                        keyboard.doModal()
                        self.CaptchaAnswer.setLabel("Your entry: " + keyboard.getText())
                        self.capAns = keyboard.getText()
                elif(control == self.button1):
                        try:
                                if(self.capAns == ""):
                                        dialog = xbmcgui.Dialog()
                                        dialog.ok("Enter Captcha Text", "Please enter the Captcha text before logging in.");
                                elif(not self.sir.FinishLogin(self.capAns)):
                                        dialog = xbmcgui.Dialog()
                                        dialog.ok("Login Failed", 
                                                "Either your username/password or your Captcha answer was incorrect.")
                                        self.close()
                                else:
                                        mydisplay = MenuWindow()
                                        mydisplay.setSirius(self.sir)
                                        mydisplay.doModal()
                                        del mydisplay
                                        self.close()
                        except:
                                print formatExceptionInfo()
                        
        
        def setSirius(self,sir):
                self.sir = sir
                destFile = os.path.abspath(CACHE_DIR + "\\captcha.jpg")
                self.CaptchaImage = xbmcgui.ControlImage(int(self.screenX * .7),
                                                                                                int(self.screenY * .15),
                                                                                                184, 65, destFile) 
                self.addControl(self.CaptchaImage)

                return True;
        

class PlayingStream(xbmcgui.Window):
        def __init__(self):
                self.screenX = self.getWidth()
                self.screenY = self.getHeight()
                fontSize = "font12"
                if self.screenX > 750:
                        fontSize = "font13"
                self.StationLabel = xbmcgui.ControlLabel(int(self.screenX * .1),
                                                                                                int(self.screenY * .15),
                                                                                                int(self.screenX * .5),
                                                                                                100, "", fontSize, "0xFFFFFFFF")
                self.ArtistLabel = xbmcgui.ControlLabel(int(self.screenX * .1),
                                                                                                int((self.screenY * .15) * 2),
                                                                                                int(self.screenX * .8),
                                                                                                100, "", fontSize, "0xFFFFFFFF")
                self.SongLabel = xbmcgui.ControlLabel(int(self.screenX * .1),
                                                                                                int((self.screenY * .15) * 3),
                                                                                                int(self.screenX * .8),
                                                                                                100, "", fontSize, "0xFFFFFFFF")
                self.IOSLabel = xbmcgui.ControlLabel(int(self.screenX * .1),
                                                                                        int((self.screenY * .15) * 5),
                                                                                        int(self.screenX * .8),
                                                                                        100, "", "font12", "0xFFFFFFFF")
                self.addControl(self.StationLabel)
                self.addControl(self.ArtistLabel)
                self.addControl(self.SongLabel)
                self.addControl(self.IOSLabel)
                self.IOSLabel.setLabel("Current Song Listing provided by DogstarRadio.com.")
                self.stopCount = 0

        
        def setSirius(self, sir):
                self.sir = sir
                self.channel = self.sir.getChannel()
                #logoURL = "http://www.siriusbackstage.com/blobimg.php?Stream=" + str(self.channel['number'])
                #destFile = path.abspath(CACHE_DIR + "\\" + str(self.channel['number']) + ".gif")
                #if (not path.exists(destFile)):
                #        loc = urllib.URLopener()
                #        try:
                #                loc.retrieve(logoURL, destFile)
                #        except:
                #                print formatExceptionInfo()
                #        loc.close()
                #picSize = 150
                #if self.screenX > 750:
                #        picSize = 300
                #self.StationImage = xbmcgui.ControlImage(int(self.screenX * .7),
                #                                                                                int(self.screenY * .15),
                #                                                                                picSize, picSize, destFile) 
                #self.addControl(self.StationImage)
                self.StationLabel.setLabel("You're listening to: " + str(self.channel['number']) + " - " + self.channel['text'])
                self.ut = UpdateTime(15, self)
                self.ut.start()
        
        
        def onAction(self, action):
                if (action == ACTION_PREVIOUS_MENU) and (self.stopCount == 0):
                        self.stopCount = 1
                        self.ut.stopThread()
                        self.StationLabel.setLabel("Cleaning up... please wait...")
                        self.ArtistLabel.setLabel("")
                        self.SongLabel.setLabel("")
                        self.ut.join()
                        self.close()


        def updateSong(self):
                songData = self.sir.getSongInfo()
                if( songData[ 'artist' ] != '' ):
                        self.ArtistLabel.setLabel(songData['artist'])
                if( songData[ 'title' ] != '' ):
                        self.SongLabel.setLabel(songData['title'])


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


dialog = xbmcgui.Dialog()
if USERNAME == '':
        dialog.ok("Set your Sirius Username / Password!", 
                "You must set your Sirius username / password in RunSirius.py before using this script!")
else:
##        currentversion = urllib.urlopen( "http://www.sacknet.org/sirius/currentversion" ).read().strip()
##        if( currentversion != CURRENT_VERSION ):
##                dialog.ok( "New version available!", "A new version of XBMCsirius is available!\n" +
##                        "This probably fixes some bugs, so you\n" +
##                        "might want to download it.  Go to\n" +
##                        "sacknet.org/sirius for more information." )
        
        if(not globSir.DoLogin()):
                dialog = xbmcgui.Dialog()
                dialog.ok("Enter Captcha Codes", 
                        "Enter the Captcha Code in the following screen\nto log in.")
                window = LoginWindow()
                window.doModal()
                del window
                mydisplay = MenuWindow()
                mydisplay.setSirius(globSir)
                mydisplay.doModal()
                del mydisplay

        else:
                mydisplay = MenuWindow()
                mydisplay.setSirius(globSir)
                mydisplay.doModal()
                del mydisplay

        # Captcha data now hard coded - leaving this here in case I need to re-enable it
        #window = LoginWindow()
        #if( not window.setSirius(globSir) ):
        #       dialog.ok("Error downloading Captcha Image",
        #               "Please press the white button after the script exits\nfor debugging information." )
        #else:
        #       window.doModal()
        #       del window
