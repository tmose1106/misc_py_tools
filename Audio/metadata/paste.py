# Standard
import os
# Dependencies
import mutagen
import mutagen.flac as mflac
import mutagen.id3 as mid3

class Metadata_Paste():
    
    """ This class is used to 'paste' or apply metadata taken from a clean 
    dictionary into a new file or set of files.
    """

    def __init__(self, metadata_dictionary, number):

        """ This function accepts a metadata dictionary, then splits a file
        through its name to find a format, and finally creates a mutagen
        object based on it's file extension.
        """

        self.info_dict = metadata_dictionary

        self.track_number = number

    def flac_paste(self, a_file):

        """ This function takes a metadata dictionary and uses Mutagen to
        apply it to a FLAC file.
        """

        title, extension = os.path.splitext(a_file)

        if extension in '.flac':
            song = mflac.FLAC(a_file)
        else:
            print("%s format not permitted by flac_paste" % extension)


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
            song[tag] = transfer_dictionary[tag]

        song.save()

    def id3_paste(self, a_file):

        """ Similar to the function above, this function adds metadata to a
        an ID3 tag within an MP3 file. Prior to application, it sorts out a 
        few formatting tidbits on how the tracks/total tracks and disc/total 
        discs are applied.
        """

        title, extension = os.path.splitext(a_file)

        if extension in '.mp3':
            song = mid3.ID3(a_file)
        else:
            print("%s format not permitted by id3_paste" % extension)


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

        transfer_dictionary = {           
            'TALB': info_dict['album'],
            'TPE1': info_dict['album_artist'],
            'TPE2': info_dict['artist'],
            'TDRL': info_dict['date'],
            'TPUB': info_dict['label'],
            'TCON': info_dict['genre'],
            'TIT2': info_dict['tracks'][self.track_number],
            'TRCK': track_number,
            'TPOS': disc_number
        }

        for tag in transfer_dictionary:
            exec_string = "song.add(mid3.%s(3, text='%s'))" % (tag, transfer_dictionary[tag])
            exec(exec_string) 
        song.save()

