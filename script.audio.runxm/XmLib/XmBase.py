# XmBase - A library containing generic Xm access code.

XmBaseDate="12/15/2009"

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
import random
import re


class XmInterface:
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.categoryName = ''
		self.genreName = ''
		self.channelData = ''
		self.prevAlbum = ''
		self.txdata = None
		self.padCount = 1000
		self.txheaders = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)'}


	def getCategoryList(self):
		#Hard Coding Categories for now.
		
		categories = ['Music', 'Other']
		
		return categories


	def setCategory(self, categoryName):
		self.categoryName = categoryName
		self.genreName = ''
		self.channelData = ''


	def getGenreList(self):
		if self.categoryName == '':
			return

	        if self.categoryName == 'Music':
	        	genres = ['Decades', 'Country', 'Hits', 'Christian', 'Rock', 'Urban', 'Jazz & Blues', 'Dance', 'World', 'Classical', 'Kids', 'Artist Radio']
		if self.categoryName == 'Other':
			genres = ['News', 'Comedy', 'Talk', 'Sports', 'Best of Sirius']
		return genres

	
	def setGenre(self, genreName):
		self.genreName = genreName
		self.channelData = ''


	def getChannelList(self):
		if (self.categoryName == '') or (self.genreName == ''):
			return

		if self.genreName == 'Artist Radio':
			channels = [
					{'number':'13', 'text':'Willie\'s Place', 'desc':'Traditional Country'},
					{'number':'18', 'text':'Elvis Radio', 'desc':'Elvis Presley 24/7'},
					#{'number':'19', 'text':'No Shoes Radio', 'desc':'Kenny Chesney\'s No Shoes Radio'},
				   	#{'number':'39', 'text':'Led Zeppelin Radio', 'desc':'Led Zeppelin 24/7'},
				   	#{'number':'53', 'text':'AC/DC Radio', 'desc':'AC/DC 24/7'},
				   	{'number':'55', 'text':'Radio Margaritaville', 'desc':'Jimmy Buffett\'s Radio Station'},
				   	{'number':'57', 'text':'Grateful Dead Radio', 'desc':'Grateful Dead 24/7'},
				   	{'number':'58', 'text':'E Street Radio', 'desc':'Bruce Springsteen 24/7'},
				   	{'number':'66', 'text':'Shade 45 (XL)', 'desc':'Uncut And Uncensored Hip-Hop By Eminem'},
					{'number':'73', 'text':'Siriusly Sinatra', 'desc':'American Standards'},
					{'number':'74', 'text':'B.B. King\'s Bluesville', 'desc':'Blues'},
					{'number':'148', 'text':'Blue Collar Radio', 'desc':'All American Comedy'},
					{'number':'149', 'text':'The Foxxhole', 'desc':'Comedy, Music, And More Presented By Jamie Foxx'}
				   ]
			return channels

		if self.genreName == 'Decades':
			channels = [
					{'number':'4', 'text':'\'40s on 4', 'desc':'Big Bands And Hits Of The \'40s'},  
				   	{'number':'5', 'text':'\'50s on 5', 'desc':'Early Rock And Roll'},
				   	{'number':'6', 'text':'\'60s on 6', 'desc':'The Authentic \'60s Sound'},
				   	{'number':'7', 'text':'\'70s on 7', 'desc':'Best Of The \'70s'},
				   	{'number':'8', 'text':'\'80s on 8', 'desc':'The Awesome \'80s'},
				   	{'number':'9', 'text':'\'90s on 9', 'desc':'Nineties Hits'}
				   ]
			return channels
			
		if self.genreName == 'Country':
			channels = [
					{'number':'10', 'text':'The Roadhouse', 'desc':'Classic Country'},
					{'number':'12', 'text':'Outlaw Country', 'desc':'Progressive Country'},
					{'number':'13', 'text':'Willie\'s Place', 'desc':'Traditional Country'},
					{'number':'14', 'text':'Bluegrass Junction', 'desc':'From Bluegrass to Newgrass'},
					{'number':'15', 'text':'The Village', 'desc':'A Celebration Of Folk Music'},
					{'number':'16', 'text':'The Highway', 'desc':'Top Country Hits'},
					{'number':'17', 'text':'Prime Country', 'desc':'Superstar Hits Of \'80s And \'90s'}
					#{'number':'19', 'text':'No Shoes Radio', 'desc':'Kenny Chesney\'s No Shoes Radio'}
				   ]
			return channels
			
		if self.genreName == 'Hits':
			channels = [
					{'number':'2', 'text':'Sirius XM Hits', 'desc':'Top 40 Hits'},
					{'number':'18', 'text':'Elvis Radio', 'desc':'Elvis Presley 24/7'},
					{'number':'20', 'text':'20 on 20', 'desc':'Interactive Top 20 Countdown'},
				   	{'number':'23', 'text':'Sirius XM Love', 'desc':'All Love Songs 24/7'},
				   	{'number':'25', 'text':'The Blend', 'desc':'Adult Hits Of The Past And Today'},
				   	{'number':'26', 'text':'The Pulse', 'desc':'Modern Hits Of The \'90s And Now'},
				   	{'number':'27', 'text':'The Bridge', 'desc':'Classic Hits'},
				   	{'number':'28', 'text':'Escape', 'desc':'Popular Melodies Of The Last 60 Years'},
				   	{'number':'29', 'text':'BBC Radio One', 'desc':'New British Music'},
				   	{'number':'30', 'text':'Pop2K', 'desc':'Today\'s Hit Music'},
				   	#{'number':'31', 'text':'U-Pop', 'desc':'International Hits'},
				   	{'number':'75', 'text':'On Broadway', 'desc':'Broadway And Showtunes'}
				   	]
			return channels
			
		if self.genreName == 'Christian':
			channels = [
				   	#{'number':'31', 'text':'The Torch', 'desc':'Christian Music that Rocks'},
				   	{'number':'32', 'text':'The Message', 'desc':'Christian Pop & Rock'},
				   	{'number':'33', 'text':'Praise', 'desc':'Glorious Gospel'},
				   	{'number':'34', 'text':'enLighten', 'desc':'Southern Gospel'},
				   	{'number':'117', 'text':'The Catholic Channel', 'desc':'Modern Talk On Catholicism'}
				   ]
			return channels

		if self.genreName == 'Rock':
			channels = [
				   	#{'number':'39', 'text':'Led Zeppelin Radio', 'desc':'Led Zeppelin 24/7'},
				   	{'number':'40', 'text':'Deep Tracks', 'desc':'Deep Album Cuts'},
				   	{'number':'41', 'text':'Hair Nation', 'desc':'\'80s Hair Bands'},
				   	{'number':'42', 'text':'Liquid Metal (XL)', 'desc':'Industrial Strength Metal'},
				   	{'number':'43', 'text':'Sirius XMU', 'desc':'New Music And Now'},
				   	{'number':'44', 'text':'1st Wave', 'desc':'Classic Alternative'},
				   	{'number':'45', 'text':'The Spectrum', 'desc':'Adult Album Rock'},
				   	{'number':'46', 'text':'Classic Vinyl', 'desc':'Classic Album Cuts'},
				   	{'number':'47', 'text':'ALT Nation', 'desc':'Alternative Hits'},
				   	{'number':'48', 'text':'Octane', 'desc':'Hard Alternative'},
				   	{'number':'49', 'text':'Classic Rewind', 'desc':'Later Classic Rock'},
				   	{'number':'50', 'text':'The Loft', 'desc':'Acoustic Rock'},
				   	{'number':'51', 'text':'The Coffeehouse', 'desc':'Progressive Rock & Fusion'},
				   	{'number':'52', 'text':'Faction (XL)', 'desc':'Emerging Artists'},
				   	{'number':'53', 'text':'Boneyard', 'desc':'Hard and Heavy Classic Rock'},
				   	{'number':'54', 'text':'Lithium', 'desc':'Classic Alternative Hits'},
				   	{'number':'55', 'text':'Radio Margaritaville', 'desc':'Jimmy Buffett\'s Radio Station'},
				   	{'number':'56', 'text':'Jam On', 'desc':'Jam Bands'},
				   	{'number':'57', 'text':'Grateful Dead Radio', 'desc':'Grateful Dead 24/7'},
				   	{'number':'58', 'text':'E Street Radio', 'desc':'Bruce Springsteen 24/7'},
				   	{'number':'59', 'text':'Underground Garage', 'desc':'Garage Rock'}
				   ]
			return channels
			
		if self.genreName == 'Urban':
			channels = [
				   	{'number':'60', 'text':'Soul Town', 'desc':'Classic Soul'},
				   	#{'number':'61', 'text':'The Flow', 'desc':'Neo Soul'},
				   	{'number':'62', 'text':'Heart & Soul', 'desc':'Adult R&B Hits'},
				   	{'number':'64', 'text':'The Groove', 'desc':'Old School R&B'},
				   	{'number':'65', 'text':'Backspin (XL)', 'desc':'Old Skool Rap'},
				   	{'number':'66', 'text':'Shade 45 (XL)', 'desc':'Uncut And Uncensored Hip-Hop'},
				   	{'number':'67', 'text':'Hip-Hop Nation (XL)', 'desc':'Hip-Hop'},
				   	{'number':'68', 'text':'The Heat', 'desc':'Rythmic Hits'}
				   ]
			return channels
		
		if self.genreName == 'Jazz & Blues':
			channels = [
				   	{'number':'28', 'text':'Escape', 'desc':'Popular Melodies Of The Last 60 Years'},
					{'number':'70', 'text':'Real Jazz', 'desc':'Traditional Jazz'},
					{'number':'71', 'text':'Watercolors', 'desc':'Contemporary/Smooth Jazz'},
					{'number':'72', 'text':'Spa', 'desc':'Contemporary Eclectic Music'},
					{'number':'73', 'text':'Siriusly Sinatra', 'desc':'American Standards'},
					{'number':'74', 'text':'B.B. King\'s Bluesville', 'desc':'Blues'},
					{'number':'75', 'text':'On Broadway', 'desc':'Broadway & Showtunes'},
				   	{'number':'76', 'text':'Cinemagic', 'desc':'Movie Soundtracks'}
				   ]
			return channels

		if self.genreName == 'Classical':
			channels = [
					{'number':'77', 'text':'Sirius XM Pops', 'desc':'Classical\'s Greatest Hits'},
					{'number':'78', 'text':'Symphony Hall', 'desc':'Greatest Music Of The Last 1,000 Years'},
					{'number':'79', 'text':'Met Opera Radio', 'desc':'Magic Of The Human Voice'}
				   ]
			return channels
			
		if self.genreName == 'Dance':
			channels = [
				   	{'number':'80', 'text':'Area', 'desc':'Underground Dance'},
				   	{'number':'81', 'text':'BPM', 'desc':'Dance Hits'},
				   	{'number':'82', 'text':'The Strobe', 'desc':'Disco Music'},
				   	{'number':'84', 'text':'Sirius XM Chill', 'desc':'Chill Music'}
				   ]
			return channels
			
		if self.genreName == 'World':
			channels = [
					{'number':'85', 'text':'Caliente', 'desc':'A Tropical Paradise (Spanish)'},
					{'number':'86', 'text':'The Joint', 'desc':'Reggae'},
					{'number':'87', 'text':'The Verge', 'desc':'New And Emerging Artists'},
					{'number':'88', 'text':'Air Musique', 'desc':'New And Emerging Music (French)'},
					{'number':'89', 'text':'Sur La Route', 'desc':'Pop Hits (French)'},
					#{'number':'90', 'text':'World Zone', 'desc':'World Music'},
					{'number':'91', 'text':'Viva', 'desc':'Latin Pop'}
					#{'number':'98', 'text':'Ngoma', 'desc':'The Sound Of Africa'}
				   ]
			return channels
			
		if self.genreName == 'Kids':
			channels = [
					{'number':'115', 'text':'Radio Disney', 'desc':'Radio Disney'},
					{'number':'116', 'text':'Kids Place Live', 'desc':'All Fun for Kids'}
				   ]
			return channels
			
		if self.genreName == 'News':
			channels = [
					{'number':'122', 'text':'CNN', 'desc':'CNN News'},
					{'number':'130', 'text':'POTUS', 'desc':'Unfiltered Political Talk'},
					{'number':'131', 'text':'BBC', 'desc':'BBC World News'},
					{'number':'132', 'text':'C-SPAN', 'desc':'C-SPAN Radio'},
					{'number':'133', 'text':'XM Public Radio', 'desc':'XM Public Radio'},
					{'number':'134', 'text':'NPR Now', 'desc':'NPR News And Conversation'},
					{'number':'135', 'text':'World Radio', 'desc':'News Around The World'},
					#{'number':'137', 'text':'The Agenda', 'desc':'GBLT Community News, Talk, And Entertainment'},
					{'number':'168', 'text':'Fox News Talk', 'desc':'Fox News Talk'}
				   ]
			return channels
			
		if self.genreName == 'Sports':
			channels = [
					{'number':'124', 'text':'Sirius NFL Radio', 'desc':'Sports'},
					{'number':'140', 'text':'ESPN Radio', 'desc':'Sports'},
					#{'number':'141', 'text':'ESPNEWS', 'desc':'The Definitive 24-hour Sports News Network'},
					#{'number':'142', 'text':'FOX Sports Radio', 'desc':'Sports Talk'},
					#{'number':'143', 'text':'Sporting News Radio', 'desc':'Sports'},
					{'number':'144', 'text':'Mad Dog Radio', 'desc':'Sports Talk'},
					#{'number':'145', 'text':'IndyCar Series Racing', 'desc':'IndyCar Series Racing'},
					{'number':'146', 'text':'PGA TOUR Network', 'desc':'Golf Talk'},
					#{'number':'147', 'text':'XM Deportivo', 'desc':'Spanish Sports Talk'},
					{'number':'175', 'text':'MLB Home Plate', 'desc':'Baseball News And Talk'},
					{'number':'204', 'text':'NHL Home Ice', 'desc':'NHL Talk And Play-By-Play'}
				   ]
			return channels
			
		if self.genreName == 'Comedy':
			channels = [
					#{'number':'148', 'text':'Blue Collar Radio (XL)', 'desc':'All American Comedy'},
					{'number':'149', 'text':'The Foxxhole (XL)', 'desc':'Comedy, Music, And More Presented By Jamie Foxx'},
					{'number':'150', 'text':'Raw Dog Comedy (XL)', 'desc':'Everything Funny'},
					{'number':'151', 'text':'Laugh USA (XL)', 'desc':'Family Laughs And Fun'},
					#{'number':'154', 'text':'National Lampoon Comedy Radio', 'desc':'Comedy'}
					{'number':'202', 'text':'The Virus (XL)', 'desc':'Outrageous Talk Radio'}
				   ]
			return channels
			
		if self.genreName == 'Talk':
			channels = [
				   	{'number':'117', 'text':'The Catholic Channel', 'desc':'Modern Talk On Catholicism'},
				   	{'number':'119', 'text':'Doctor Radio', 'desc':'NYU Langone Medical Center'},
				   	{'number':'122', 'text':'CNN', 'desc':'CNN News'},
				   	{'number':'130', 'text':'POTUS', 'desc':'Political Talk'},
				   	{'number':'131', 'text':'BBC World Service', 'desc':'BBC World Service'},
				   	{'number':'132', 'text':'C-SPAN', 'desc':'C-SPAN Radio'},
				   	{'number':'133', 'text':'XM Public Radio', 'desc':'Public Radio'},
				   	{'number':'134', 'text':'NPR Now', 'desc':'NPR News and Conversation'},
				   	{'number':'135', 'text':'World Radio Network', 'desc':'News From Around the World'},
				   	#{'number':'137', 'text':'The Agenda', 'desc':'GBLT News, Talk, Entertainment'},
				   	{'number':'139', 'text':'Sirius XM Stars Too (XL)', 'desc':'Talk Radio for Guys'},
					{'number':'155', 'text':'Sirius XM Stars (XL)', 'desc':'Celebrity Hosts And Lifestyle Programming'},
					{'number':'156', 'text':'Oprah Radio', 'desc':'Oprah & Friends'},
					{'number':'157', 'text':'Martha Stewart Living Radio', 'desc':'How To For Living'},
					{'number':'162', 'text':'Cosmo Radio (XL)', 'desc':'Fun, Fearless, Female'},
				   	{'number':'168', 'text':'Fow News Talk', 'desc':'Fox News Talk'},
				   	{'number':'169', 'text':'The Power', 'desc':'African American Talk'}
					#{'number':'256', 'text':'Oprah\'s Soul Series', 'desc':'Oprah\'s Soul Series'}
				   ]
			return channels

		if self.genreName == 'Best of Sirius':
			channels = [
				   	{'number':'99', 'text':'Playboy Radio (XL)', 'desc':'Smart & Sexy Adult Radio'},
				   	{'number':'100', 'text':'Howard 100 (XL)', 'desc':'Outrageous Personalities, Uncensored Radio'},
				   	{'number':'101', 'text':'Howard 101 (XL)', 'desc':'Outrageous Personalities, Uncensored Radio'},
				   	{'number':'124', 'text':'Sirius NFL Radio', 'desc':'24/7 NFL Talk'},
				   	{'number':'157', 'text':'Martha Stewart Living', 'desc':'How To For Living'}
				   ]
			return channels


	def setChannel(self, channelData):
		self.channelData = channelData


	def getChannel(self):
		return self.channelData


	def getChannelURL(self):
		url = 'http://www.xmradio.com/player/listen/play.action?channelKey='
		url = url + self.channelData['number']
		req = urllib2.Request(url)
		channelPage = ClientCookie.urlopen(req).read()

		urlPos = channelPage.find('SRC="')
		if urlPos == -1:
			self.doLogin()
			channelPage = ClientCookie.urlopen(req).read()
			urlPos = channelPage.find('SRC="')
			if urlPos == -1:
				return -1

		url = channelPage[urlPos + 5 :]
		url = url[:url.find('"')]

		url = url.replace("&amp;", "&")

		#print url

		req = urllib2.Request(url, self.txdata, self.txheaders)
		asx = ClientCookie.urlopen(req).read()
		#print asx

		mmsPos = asx.find('Ref1=http://')
		if mmsPos != -1:
			mmstemp = asx[mmsPos + 12 :]
			mmstemp = mmstemp[:mmstemp.find('.asf')]
			mms = "mms://" + mmstemp + ".asf"
			#print mms
			return mms
		else:
			return url

		#return url
	
	def getSongInfo(self):
		self.padCount = self.padCount + 1
		#http://www.xmradio.com/padData/pad_data_servlet.jsp?all_channels=true
		trackerurl = 'http://www.xmradio.com/padData/pad_data_servlet.jsp?channel='
		trackerurl = trackerurl + str(self.channelData['number'])+ '&rnd=' + str(self.padCount)
		trackerreq = urllib2.Request(trackerurl, self.txdata, self.txheaders)
		
		albumName = ''
		tracker = ClientCookie.urlopen(trackerreq).read()
		tracker2 = tracker
		tracker3 = tracker
		target = '<artist>'
		target2 = '<songtitle>'
		target3 = '<album>'
		songInfo = {'artist':'Error',
					'title':'Problem Retrieving Data!', 'album':'Album information not available', 'albumURL': ''}

		if tracker.find(target) != -1:
			tracker = tracker[tracker.find(target) + len(target) :]
			songInfo['artist'] = tracker[: tracker.find('</artist>')]
			songInfo['artist'] = songInfo['artist'].replace("&#39;", "'")
			songInfo['artist'] = songInfo['artist'].replace("&#38;", "&")
			songInfo['artist'] = songInfo['artist'].replace("&amp;", "&")
			tracker2 = tracker2[tracker2.find(target2) + len(target2) :]
			songInfo['title'] = tracker2[: tracker2.find('</songtitle>')]
			songInfo['title'] = songInfo['title'].replace("&#39;", "'")
			songInfo['title'] = songInfo['title'].replace("&#38;", "&")
			songInfo['title'] = songInfo['title'].replace("&amp;", "&")
			tracker3 = tracker3[tracker3.find(target3) + len(target3) :]
			albumName = tracker3[: tracker3.find('</album>')]
			albumName = str(albumName)
			albumName = re.sub('&#39;', '\'', albumName)
			albumName = re.sub('&#38;', '&', albumName)
			albumName = re.sub('&amp;', '&', albumName)
			songInfo['album'] =albumName
			
			if albumName != self.prevAlbum:
				if (albumName.strip() == 'CD Single') or (albumName.strip() == 'COMP Promo Only'):
					albumParam = songInfo['title']
				else:
					albumParam = albumName
				#params = urllib.urlencode({'imgsize':'m','artist': songInfo['artist'],'album': songInfo['album']})
				#f = urllib.urlopen("http://www.slothradio.com/covers/?adv=1&" + params)
				#ImageHTML = f.read()
				#target = 'div class="album0"><img src="'
				#if ImageHTML.find(target) != -1:
				#	ImageHTML = ImageHTML[ImageHTML.find(target) + len(target) :]
				#	songInfo['albumURL'] = ImageHTML[: ImageHTML.find('"')]
			self.prevAlbum = albumName

		return songInfo
