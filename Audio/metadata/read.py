# Dependencies
import mutagen.flac as mflac
import mutagen.id3 as mid3

class Read_Metadata():

    def __init__(self, a_file):

        self.audio_file = a_file

    def create_tag_dict(self, audio_object, a_dict):

        metadata_dict = {}
        song = audio_object

        for tag in a_dict:
            try:
                metadata_dict[tag] = song[a_dict[tag]][0]
            except KeyError:
                metadata_dict[tag] = ''
                print("WARNING: The %s tag is missing" % a_dict[tag])

        return metadata_dict

    def flac_tag(self):

        song = mflac.FLAC(self.audio_file)

        info_dict = {
            'album': 'ALBUM',
            'album_artist': 'ALBUMARTIST',
            'artist': 'ARTIST',
            'date': 'DATE',
            'label': 'LABEL',
            'genre': 'GENRE',
            'title': 'TITLE',
            'track_number': 'TRACKNUMBER',
            'total_tracks': 'TOTALTRACKS',
            'disc_number': 'DISCNUMBER',
            'total_discs': 'TOTALDISCS'
        }

        metadata_dictionary = self.create_tag_dict(song, info_dict)

        return metadata_dictionary

    def id3_tag(self):

        song = mid3.ID3(self.audio_file)

        info_dict = {
            'album': 'TALB',
            'album_artist': 'TPE1',
            'artist': 'TPE2',
            'date': 'TDRL',
            'label': 'TPUB',
            'genre': 'TCON',
            'title': 'TIT2'
        }

        metadata_dictionary = self.create_tag_dict(song, info_dict)

        disc_tag = song['TPOS'][0]
        track_tag = song['TRCK'][0]

        if '/' in disc_tag:
            disc_number, total_discs = track_tag.split()

            metadata_dict['track_number'] = disc_number
            metadata_dict['total_tracks'] = total_discs

        else:
            print("WARNING: The TPOS total tag is missing")
            metadata_dict['track_number'] = disc_tag
            metadata_dict['total_tracks'] = ''

        if '/' in track_tag:
            track_number, total_tracks = track_tag.split()

            metadata_dict['track_number'] = track_number
            metadata_dict['total_tracks'] = total_tracks

        else:
            print("WARNING: The TRCK total tag is missing")
            metadata_dict['track_number'] = track_tag
            metadata_dict['total_tracks'] = ''
