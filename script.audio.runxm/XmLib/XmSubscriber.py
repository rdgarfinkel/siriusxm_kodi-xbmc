# XmSubscriber - A library to navigate xm and retrieve
# Windows Media (mms) URLS

# Version 0.1

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

import XmBase
import ClientCookie
import urllib
import urllib2
import md5

class XmInterface(XmBase.XmInterface):

	def doLogin(self):
		
		params = urllib.urlencode({'userName':self.username,'password':self.password,'playerToLaunch':'xm','encryptPassword':'true'})
		#print params
		url = 'http://www.xmradio.com/player/login/xmlogin.action'
		req = urllib2.Request(url, self.txdata, self.txheaders)
		ClientCookie.urlopen(req, params).read()
		#print ClientCookie.urlopen(req, params).read()
