""" This script looks at the tags of your MP3 files, and then standardizes them
to the ID3 2.4 standard.
"""

possible_id3_tags = {
    'date': ['TDRL', 'TDRC', 'TXXX=Year']
}
