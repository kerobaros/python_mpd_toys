#!/bin/env python

import random
import subprocess

from mpd import MPDClient

ROFI = "rofi"


def rofi(list, prompt):
    cred_list = "\n".join(list)
    rofi_command_line = [ROFI, "-dmenu", "-width", "50", "-lines", "40", "-p",
                         prompt]
    with subprocess.Popen(rofi_command_line, stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE, universal_newlines=True)\
            as proc:
        out = proc.communicate(input=cred_list)[0]
    return out


def get_tracks_from_album(MPD, artist, album, debug=False):
    tracks = sorted(MPD.list("filename", "artist", artist, "album", album))
    return tracks


def queue_tracks(MPD, tracks, debug=False):
    for track in tracks:
        MPD.add(track)


def choose_album(MPD, artist='', year='', debug=False):
    if artist != '':
        list = sorted(MPD.list("album", "artist", artist))
    elif year != '':
        list = sorted(MPD.list("album", "date", year))
    else:
        list = sorted(MPD.list("album"))
    if len(list) > 0:
        # if debug: print list
        album = random.choice(list)
        return album
    else:
        print('No albums matching search!')


def queue_album(MPD, artist='', album='', debug=False):
    tracks = get_tracks_from_album(MPD, artist, album, debug)
    queue_tracks(MPD, tracks, debug)


def press_play(MPD, debug=False):
    MPD.play()
    print('Now Playing:', MPD.currentsong()['artist'], '-',
          MPD.currentsong()['album'],
          '(%s)' % MPD.currentsong()['date'])


def connect():
    MPD = MPDClient()
    MPD.connect("localhost", 6600)
    return MPD


def disconnect(MPD):
    MPD.close()
    MPD.disconnect()


def menu(input_list, prompt="Choose an action: "):
    menu_list = []
    i = 1
    for item in input_list:
        menu_list.append("%02d - %s - %s" % (i, item[0], item[1]))
        i += 1
    menu_list.append("11 - More albums...")
    menu_choice = rofi(menu_list, prompt).strip()
    return menu_list.index(menu_choice)


def get_album_artist(MPD, album):
    album_info = MPD.find("album", album)
    for track_info in album_info:
        artist = track_info['artist']
    if type(artist) is list:
        return artist[0]
    else:
        return artist


def main_menu(MPD):
    i = 0
    albums = []
    while i < 10:
        current_album = choose_album(MPD)
        current_artist = get_album_artist(MPD, current_album)
        albums.append([current_artist, current_album])
        i += 1
    choice = menu(albums, prompt="Choose an album: ")
    if choice < 10:
        decision = albums[choice]
    else:
        decision = False
    return decision


def main():
    mpd = connect()
    mpd.stop()
    mpd.clear()
    random.seed()
    choice = False
    while choice is False:
        choice = main_menu(mpd)
    queue_album(mpd, artist=choice[0], album=choice[1])
    press_play(mpd)
    disconnect(mpd)


if __name__ == "__main__":
    main()
