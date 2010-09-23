from SiriusLib import *

username = raw_input( 'Email / Username: ' )
password = raw_input( 'Password: ' )
sir = SiriusSubscriber.SiriusInterface( username, password )
#sir = SiriusGuest.SiriusInterface( username, password )
print sir.DoLogin()

cats = sir.getCategoryList()
for i in range( 0, len( cats ) ):
	print "[" + `i` + "]: " + cats[i]
sir.setCategory( cats[ int( raw_input( 'Select Category: ' ) ) ] )

gens = sir.getGenreList()
for i in range( 0, len( gens ) ):
	print "[" + `i` + "]: " + gens[i]
sir.setGenre( gens[ int( raw_input( 'Select Genre: ' ) ) ] )

chans = sir.getChannelList()
for i in range( 0, len( chans ) ):
	print "[" + `i` + "]: " + chans[i]['text']
sir.setChannel( chans[ int( raw_input( 'Select Channel: ' ) ) ] )

print sir.getChannelURL()
print sir.getSongInfo()
print sir.getChannel()
