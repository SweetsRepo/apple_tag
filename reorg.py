import os
import re
import shutil

import taglib

SRCDIR = "./Music/"
DESTDIR = "./Sorted/"

ILLEGAL = [':','*','"','<','>','|','?','/','\\']

for root, _, fnames in os.walk(SRCDIR):
    for fname in fnames:
        try:
            song_fname = os.path.join(root, fname)
            song_ext = os.path.splitext(song_fname)[-1]
            song = taglib.File(song_fname)
            artist = song.tags["ARTIST"][0].strip()
            album = song.tags["ALBUM"][0].strip()
            title = song.tags["TITLE"][0].strip()
            track_number = song.tags["TRACKNUMBER"][0].strip().split("/")[0]

            # Remove Windows Restricted Characters from Directory and Filename
            for c in ILLEGAL:
                artist = artist.replace(c,"")
                album = album.replace(c,"")
                title = title.replace(c,"")
            song_dest_dir = os.path.join(DESTDIR, artist, album)
            song_dest_name = os.path.join(
                song_dest_dir,
                f"{track_number}. {title}"
            )
            if not os.path.exists(song_dest_dir):
                os.makedirs(song_dest_dir)
            shutil.copy2(
                song_fname,
                song_dest_name+song_ext
            )
        except (OSError, KeyError) as e:
            print(os.path.join(root, fname))
