# Standard
import os
# Dependencies
import mutagen
import mutagen.flac as mflac
import mutagen.id3 as mid3

class Metadata_Paste():
    
    """ This class is used to 'paste' or apply metadata taken from a clean 
    dictionary into a new file
    """

    def __init__(self, metadata_dictionary, a_file, number):

        """ This function accepts a metadata dictionary, then splits a file
        through its name to find a format, and finally creates a mutagen
        object based on it's file extension.
        """

        self.info_dict = metadata_dictionary
        
        title, extension = os.path.splitext(a_file)

        if extension in '.flac':
            self.song = mflac.FLAC(a_file)
        elif extension in '.mp3':
            self.song = mflac.ID3(a_file)
        else:
            print("%s format not permitted" % extension)

        self.track_number = number

    def flac_paste(self):

        """ This function takes a metadata dictionary and uses Mutagen to
        apply it to a FLAC file.
        """

        info_dict = self.info_dict
        transfer_dictionary = {
            'ALBUM': info_dict['album'],
            'ALBUMARTIST': info_dict['album_artist'],
            'ARTIST': info_dict['artist'],
            'DATE': info_dict['date'][:4],
            'LABEL': info_dict['label'],
            'GENRE': info_dict['genre'],
            'TITLE': info_dict['tracks'][self.track_number],
            'TRACKNUMBER': self.track_number.zfill(2),
            'TOTALTRACKS': str(info_dict['total_tracks']),
            'DISCNUMBER': info_dict['disc'],
            'TOTALDISCS': info_dict['total_discs']
            }

        for tag in transfer_dictionary:
            self.song[tag] = transfer_dictionary[tag]

        self.song.save()

    def id3_paste(self):

        """ Similar to the function above, this function adds metadata to a
        an ID3 tag within an MP3 file. Prior to application, it sorts out a 
        few formatting tidbits on how the tracks/total tracks and disc/total 
        discs are applied.
        """

        info_dict = self.info_dict

        disc_number = ()
        try:
            disc_number = "%s/%s" % (info_dict['disc'], info_dict['total_discs'])
        except KeyError:
            disc_number = '1/1'

        track_number = ()
        try:
            track_number = "%s/%s" % (self.track_number, info_dict['total_tracks'])
        except KeyError:
            track_number = self.track_number       

        tranfer_dictionary = {           
            'TALB': info_dict['album'],
            'TPE1': info_dict['album_artist'],
            'TPE2': info_dict['artist'],
            'TDRL': info_dict['date'],
            'TPUB': info_dict['label'],
            'TCON': info_dict['genre'],
            'TIT2': info_dict['tracks'][number],
            'TRCK': track_number,
            'TPOS': disc_number
        }

        for tag in transfer_dictionary:
            self.song[tag] = transfer_dictionary[tag]

        self.song.save()

