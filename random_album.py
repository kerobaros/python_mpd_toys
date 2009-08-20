#!/usr/bin/python

import random, mpd

def main():
    MPD = mpd.MPDClient()
    MPD.connect("localhost",6600)
    #MPD.iterate = True
    random.seed()
    MPD.stop()
    MPD.clear()
    list = sorted(MPD.list("album"))
    album = random.choice(list)
    tracks = sorted(MPD.find("album", album))
    for track in tracks: MPD.add(track['file'])
    MPD.play()
    print 'Now Playing:', MPD.currentsong()['artist'], '-', MPD.currentsong()['album'], '(%s)' % MPD.currentsong()['date']
    MPD.close()
    MPD.disconnect()
    
if __name__ == '__main__':
    main()
