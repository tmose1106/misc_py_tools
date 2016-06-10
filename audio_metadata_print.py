import sys
import mutagen.id3 as mid3

song = mid3.ID3(sys.argv[1])
output = song.pprint()
print(output)
