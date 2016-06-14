import os
import sys
import mutagen.flac as mflac
import mutagen.id3 as mid3

input_song = sys.argv[1]
proc_song = ()
title, extension = os.path.splitext(input_song)
true_extension = extension.lower()

if true_extension == '.mp3':
    proc_song = mid3.ID3(input_song)
elif true_extension == '.flac':
    proc_song = mflac.FLAC(input_song)
else:
    print("Extension not supported")
    sys.exit(1)

output = proc_song.pprint()

print(output)
