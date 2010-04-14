#!/usr/bin/env python
# -*- coding: utf-8 -*-

# change following line from True to False to prevent autoskipping one-starred songs
skip_on_one = True

import mpd, os, sys

method = ''
if len(sys.argv) > 1: method = sys.argv[1]

ratings = {}
ratingsfilename = os.path.expanduser("~/.mpd/ratings.db")
ratingsfile = open(ratingsfilename)

for line in ratingsfile.readlines():
    if line != '': 
        linefile, linerating = line.rstrip('\n').split(':')
        ratings[linefile] = linerating

ratingsfile.close()

client = mpd.MPDClient()
try: client.connect("localhost", 6600)
except socket.error:
    print 'Couldn\'t connect to MPD!'
    sys.exit(1)

song = client.currentsong()
    
songfilename = song['file']


if method != '':
    if method == '1':
        ratings[songfilename] = 1
        if skip_on_one: client.next()
    if method == '2': ratings[songfilename] = 2
    if method == '3': ratings[songfilename] = 3
    if method == '4': ratings[songfilename] = 4
    if method == '5': ratings[songfilename] = 5
    if method == '-':
        print '*' * int(ratings.get(songfilename, 0))
        sys.exit(0)

print ratings.get(songfilename, 0)

ratingsfile = open(ratingsfilename, 'w')
for rating in ratings.items():
    ratingsfile.write(rating[0] + ':' + str(rating[1]) + '\n')

ratingsfile.close()
