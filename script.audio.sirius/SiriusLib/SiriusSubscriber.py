# SiriusSubscriber - A library to navigate the sirius subscriber area and
# retrieve Windows Media (mms) URLS

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

import SiriusBase
import ClientCookie
import urllib
import urllib2
import md5

class SiriusInterface(SiriusBase.SiriusInterface):

	def DoLogin(self):
		#url = 'http://www.sirius.com/player/channel/xenaforward.action'
		url = 'http://www.sirius.com/player/home/siriushome.action'
		req = urllib2.Request(url, self.txdata, self.txheaders)
		loginData = ClientCookie.urlopen(req).read()
		self.token = self.findToken(loginData)
		self.captchaID = self.findCaptchaID(loginData)
		self.captchaImage = self.findCaptchaImage(loginData)
		self.captchaAnswer = self.getCaptchaCode(loginData)
		params = urllib.urlencode({'activity':'login',
									'type':'subscriber',
									'password':self.password,
									'loginForm':'subscriber',
									'stream':'undefined',
									'token':self.token,
									'username':self.username,
									'captchaID':self.captchaID,
									'captcha_response':self.captchaAnswer})

	def FinishLogin(self):
		url = 'http://www.sirius.com/sirius/servlet/MediaPlayerLogin/subscriber'
		req = urllib2.Request(url, self.txdata, self.txheaders)
		if(ClientCookie.urlopen(req, params).read().find('redirect to player') != -1):
			return True
		else:
			return False
