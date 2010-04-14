#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mpd, scrobble, random

from optparse import OptionParser

def main():

    parser = OptionParser()
    parser.add_option("-a", "--artist", type = "string", dest = "artist", help = "Specifies an artist to start building playlist from; needs to be a quoted string")
    parser.add_option("-l", "--limit", type = "int", dest = "limit", help = "Specifies length of playlist; defaults to 50")
    parser.add_option("-d", "--debug", action = "store_true", dest = "debug", help = "Outputs debug text and prevents modifying MPD server")
    (options, args) = parser.parse_args()
    
    random.seed()
    
    MPD = mpd.MPDClient()
    MPD.connect('localhost', 6600)
    
    if options.artist == '' or options.artist == None: artist = scrobble.Artist(MPD.currentsong()['artist'])
    else: artist = scrobble.Artist(options.artist)
    if options.limit == None: limit = 50
    else: limit = options.limit
    if options.debug == None: debug = False
    else: debug = True
    
    #if debug: print MPD.currentsong()
    #if debug: print artist
    
    #if debug: print artist
    #if debug: print artist.similar
    
    #if artist == '': print 'Couldn\'t find artist on last.fm!'
    #similar_artists = get_artist_list(artist)
    
    similar_artists = [artist.name]
    missing_artists = []
    for option in artist.similar:
        if MPD.search('artist', option.name) != []: similar_artists.append(option.name)
        else: missing_artists.append(option.name)
        
    #print similar_artists
    
    #print MPD.playlistinfo()
    
    if debug: limit = len(MPD.playlist()) + 1
    
    while len(MPD.playlist()) < limit:
        for option in similar_artists:
            #print option
            choice = random.choice(MPD.search('artist', option))['file']
            extant = False
            for song in MPD.playlistinfo():
                if song['file'] == choice: 
                    if debug: print '%s is already on playlist!' % choice
                    extant = True
            if extant == False:
                if debug == False: MPD.add(choice)
                if debug: print 'would add %s!' % choice
    
    #print sorted(MPD.playlist())
    
    #print missing_artists
    
if __name__ == '__main__': main()
