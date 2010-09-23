from SiriusLib import *

sir = SiriusSubscriber.SiriusInterface( '', '' )
print sir.testSongInfo( raw_input( 'Channel Number: ' ) )
