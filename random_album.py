#!/usr/bin/python

import random, mpd
from optparse import OptionParser

def queue_album(artist = '', year = '', debug = False):

    MPD = mpd.MPDClient()
    MPD.connect("localhost",6600)
    if debug == None: 
        MPD.stop()
        MPD.clear()
    if artist != '': list = sorted(MPD.list("album", "artist", artist))
    elif year != '': list = sorted(MPD.list("album", "date", year))
    else: list = sorted(MPD.list("album"))
    if len(list) > 0:
        if debug: print list
        album = random.choice(list)
        if debug: print album
        tracks = sorted(MPD.find("album", album))
        if debug == None:
            for track in tracks: MPD.add(track['file'])
            MPD.play()
            print 'Now Playing:', MPD.currentsong()['artist'], '-', MPD.currentsong()['album'], '(%s)' % MPD.currentsong()['date']
        MPD.close()
        MPD.disconnect()
    else: print 'No albums matching search!'

def main():
    random.seed()
    parser = OptionParser()
    parser.add_option("-a", "--artist", type = "string", dest = "artist", help = "Specifies an artist to limit album choices from; needs to be a quoted string")
    parser.add_option("-y", "--year", type = "string", dest = "year", help = "Specifies a year to limit album choices")
    parser.add_option("-d", "--debug", action = "store_true", dest = "debug", help = "Outputs debug text and prevents modifying MPD server")
    (options, args) = parser.parse_args()

    #if options.debug == None
    
    if options.artist: queue_album(artist = options.artist, debug = options.debug)
    elif options.year: queue_album(year = options.year, debug = options.debug)
    else: queue_album(debug = options.debug)
        
if __name__ == '__main__':
    main()
