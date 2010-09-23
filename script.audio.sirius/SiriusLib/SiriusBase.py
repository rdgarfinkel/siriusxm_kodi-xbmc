# SiriusBase - A library containing generic Sirius access code.

# http://www.sacknet.org/sirius/

# Version 1.2

# Mike Rosack - 09/30/2006

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

import ClientCookie
import urllib
import urllib2
import md5
import os


CACHE_DIR = os.getcwd() + "\\cache"

class SiriusInterface:
	def __init__(self, username, password):
		self.username = username
		self.password = md5.new(password).hexdigest()
		self.categoryName = ''
		self.genreName = ''
		self.channelData = ''
		self.txdata = None
		self.txheaders = {'User-Agent':'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.7.8) Gecko/20050511 Firefox/1.0.4'}


	def getCategoryList(self):
		url = 'http://www.sirius.com/sirius/mediaplayer/player/common/lineup/category.jsp?category=&genre=&channel='
		req = urllib2.Request(url, self.txdata, self.txheaders)
		catPage = ClientCookie.urlopen(req).read()
		categories = []
		while catPage.count("myPlayer.Category"):
			catPos = catPage.find('myPlayer.Category(\'') + 19
			category = catPage[catPos :]
			category = category[:category.find('\'')]
			if (category != ''):
				categories.append(category)
			catPage = catPage[catPos + len(category) :]
		return categories


	def setCategory(self, categoryName):
		self.categoryName = categoryName
		self.genreName = ''
		self.channelData = ''


	def getGenreList(self):
		if self.categoryName == '':
			return

		url = 'http://www.sirius.com/sirius/mediaplayer/player/common/lineup/genre.jsp?category=' + self.categoryName
		req = urllib2.Request(url, self.txdata, self.txheaders)
		genrePage = ClientCookie.urlopen(req).read()
		genres = []
		while genrePage.count("myPlayer.Genre"):
			genrePos = genrePage.find('myPlayer.Genre(\'' + self.categoryName + '\', \'') + 20 + len(self.categoryName)
			genre = genrePage[genrePos :]
			genre = genre[:genre.find('\'')]
			if (genre != ''):
				genres.append(genre)
			genrePage = genrePage[genrePos + len(genre) :]
		return genres

	
	def setGenre(self, genreName):
		self.genreName = genreName
		self.channelData = ''


	def getChannelList(self):
		if (self.categoryName == '') or (self.genreName == ''):
			return

		url = 'http://www.sirius.com/sirius/mediaplayer/player/common/lineup/channel.jsp?category=' + self.categoryName + '&genre=' + self.genreName
		req = urllib2.Request(url, self.txdata, self.txheaders)
		channelPage = ClientCookie.urlopen(req).read()
		channels = []
		channelPage = channelPage[channelPage.find('onLoad=') + 50:]
		while channelPage.count("myPlayer.Channel"):
			channelTarget = 'myPlayer.Channel(\'' + self.categoryName + '\', \'' + self.genreName + '\', \''
			channelPos = channelPage.find(channelTarget) + len(channelTarget)
			channel = channelPage[channelPos :]
			channel = channel[:channel.find('\'')]
			channelPage = channelPage[channelPos + len(channel) :]

			if (channel != ''):
				tokenPos = channelPage.find('\', \'') + 4
				token = channelPage[tokenPos :]
				token = token[:token.find('\')"')]
				channelPage = channelPage[len(token) + tokenPos + 3:]

				numberPos = channelPage.find('class="channel">') + 16
				number = channelPage[numberPos :]
				number = number[:number.find('</a>')]
				channelPage = channelPage[len(number) + numberPos + 4:]
				number = number[: number.find('|')]
				number = number.strip()

				textPos = channelPage.find('class="text">') + 13
				text = channelPage[textPos :]
				text = text[:text.find('</a>')]
				channelPage = channelPage[len(text) + textPos + 4:]

				descPos = channelPage.find('class="desc">') + 13
				desc = channelPage[descPos :]
				desc = desc[:desc.find('</a>')]
				channelPage = channelPage[len(desc) + descPos + 4:]
		
				channelInfo = {'channel':channel,
								'token':token,
								'number':number,
								'text':text,
								'desc':desc}

				channels.append(channelInfo)
			
		return channels
	

	def setChannel(self, channelData):
		self.channelData = channelData


	def getChannel(self):
		return self.channelData


	def getChannelURL(self):
		url = 'http://www.sirius.com/sirius/servlet/MediaPlayer?activity=selectStream&stream='
		url = url + self.channelData['channel']
		url = url + '&token=' + self.channelData['token']
		req = urllib2.Request(url, self.txdata, self.txheaders)
		channelPage = ClientCookie.urlopen(req).read()

		urlPos = channelPage.find('PARAM NAME="FileName" VALUE="')
		if urlPos == -1:
			return -1

		url = channelPage[urlPos + 29 :]
		url = url[:url.find('"')]

		req = urllib2.Request(url, self.txdata, self.txheaders)
		asx = ClientCookie.urlopen(req).read()

		mmsPos = asx.find('<ref href="mms')
		if mmsPos != -1:
			mms = asx[mmsPos + 11 :]
			mms = mms[:mms.find('"/>')]
			return mms
		else:
			return url


	def findToken(self, stringData):
		#print "findToken:"
		target = '<input type="hidden" name="token" value="'
		position = stringData.find(target)
		token = stringData[position + len(target) :]
		token = token[:token.find('">')]
		#print token
		return token

	def findCaptchaID(self, stringData):
		print "findCaptchaID token:"
		target = '<input type="hidden" name="captchaID" value="'
		position = stringData.find(target)
		token = stringData[position + len(target) :]
		token = token[:token.find('">')]
		print token
		return token
	
	def findCaptchaImage(self, stringData):
		#print "findCaptchaImage token:"
		target = '<img src="/mp/captcha/image/'
		position = stringData.find(target)
		token = stringData[position + len(target) :]
		token = token[:token.find('" width="')]
		#print token
		return token
	
	def getCaptchaCode(self, stringData):
		print "getCaptchaCode token:"
		target = '<img src="/mp/captcha/image/img_'
		position = stringData.find(target)
		token = stringData[position + len(target) :]
		token = token[:token.find('.jpg')]
		print token
		#return token
		imgID = token
		# Thanks to Tanner Jepson for these codes!
		
		captchaCodes = ["wrQ2","LtFK","2bxh","Mf6D","fEXY","Wc46","fYP7","X6aw","nQQd","rt3k","kQhf","f2WG","aTLX","Qnaf","cA2T","cY36","xddQ","yaYf","4P67","7ekW","yZLN","RhLd","4eAC","bHKA","t4kW","AZQE","RWhN","7rPD","fYWP","7HCb","aR3L","TDkT","kf4Y","yfFZ","eyDh","yWnK","NFWm","2n4d","634t","YnAH","MHPQ","N26M","Ra4C","dR4e","P6CZ","cnaW","W6wm","Wm3y","mrdG","3KhR","p6fY","AGen","ctDC","HDZY","WNKM","K72H","k627","PMW2","mEew","y3YA","r67T","nDpE","Q7MQ","kLW2","pyDR","AQkH","wdfW","eWQh","ttEP","tn6r","P6yx","nRKW","eXEb","ywNZ","MHZt","f7mc","RyMY","MTPC","rc3k","Xebn","ffGH","6Y2D","mbKX","6nCH","tHyG","RtAE","hWE2","3F6D","dQpC","HACn","Ampy","mLEr","Mdt2","QGbL","PDQp","EEyC","MfmL","PQ3f","HPPc","pTXc"]
		#captchaCodes = ["vRLCHr","Rk9f3b","tN2R1A","R3iwj5","jBjsvj","v3jvKg","IImNmx","cahMYf","Vw3rxG","R7KPgK","RUyTUS","cef11w","NAQbyX","q6EYAH","tReWYs","fimQlm","U6qsi6","m5Wkwh","FpVR2T","CuAF1k","sgnUw7","4N1RPP","ech2am","CtbsNQ","kXrPES","1AgXSR","5DHYSR","e3ru7T","c1yjHE","FR1ltI","Xtn36U","DHEWnx","8KePqv","1TKVVk","BIY138","RA6c83","SaluKT","T89gGV","gUPVqL","J4F3gi","BbQnjy","qLrRgi","c3eSfa","yAhdN5","3YW4WC","mPvBah","UZnHN4","x24GCx","GLdYdn","DsUIMk","7GCaEc","1WXPNr","SRpRsG","vSlae4","r95Vhm","1tGuk7","wnZyD4","c8lj6k","sdQ3X4","5FNMsi","Up7Rni","csjyJa","9Uq5rm","p9kbvj","Cy1iip","mc7y2c","SE3rqi","YmJ3Tv","Qr32YN","13rcdJ","xn33VA","tjxuf4","3hLBuU","3fntSq","rMYmpH","yvKfyR","bkxHDW","EtUSs3","3gA7wG","Yn3uUL","hcw9cg","aLI1R7","wmkRRP","Rm3C3i","CgS98N","xaF7cd","ATxch8","8I1rDk","C8896y","SiNusq","AQZ3kR","ARFUSP","hDgs72","Lxbg1X","4716A3","gCkAqa","wRDWeN","h64fGf","Cr2VPm","66SiiF"]

		print "captchaCodes"
		print captchaCodes[ int( imgID ) - 1 ]

		self.base_path = os.getcwd().replace(';','')

		#find XBMC script location, and the "cache" folder underneath it; create it if it doesn't exist
		dir = os.path.join(self.base_path, 'cache')
		if not os.path.exists(dir):
			os.mkdir(dir)

		#find the "captcha.txt" file to create the file storing the username/password
		path = os.path.join(dir, 'captcha.txt')

		##if the file doesn't exist, create it. most likely this will be a new installation
		if not os.path.isfile(path):
			try:
				f = open(path, 'w')
				f.write(captchaCodes[ int( imgID ) - 1 ])
				f.close()
			except IOError:
				pass

		return captchaCodes[ int( imgID ) - 1 ]

	def testSongInfo(self, channelNumber):
		self.channelData = { 'number' : channelNumber }
		print self.getSongInfo()

	# Get what's playing info from DogStar Radio
	def getSongInfo(self):
		dogstarUrl = "http://www.dogstarradio.com/channelrss/" + str(self.channelData['number']) + ".txt"
		tracker=urllib.urlopen(dogstarUrl).read();
		songInfo = {'artist':'',
					'title':''}
		lines=tracker.split("\n")
		songInfo['artist']=lines[3]
		songInfo['title']=lines[4]
		
		return songInfo
