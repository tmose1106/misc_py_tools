# Standard
import os
# Dependencies
import mutagen
import mutagen.flac as mflac
import mutagen.id3 as mid3
import mutagen.oggvorbis as mogg

class Apply_Metadata():

    """ This class is used to apply metadata taken from a clean dictionary
    into a new file or set of files.
    """

    def __init__(self, metadata_dictionary, number):

        """ This function accepts a metadata dictionary, then splits a file
        through its name to find a format, and finally creates a mutagen
        object based on it's file extension.
        """

        self.info_dict = metadata_dictionary

    def vorbis_tag(self, a_file, track_number):

        """ This function takes a metadata dictionary and uses Mutagen to
        apply it to a FLAC or OGG Vorbis file.
        """

        title, extension = os.path.splitext(a_file)

        if extension == '.flac':
            song = mflac.FLAC(a_file)
        elif extension == '.ogg':
            song = mogg.OggVorbis(a_file)
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
            'TITLE': info_dict['tracks'][track_number],
            'TRACKNUMBER': track_number.zfill(2),
            'TOTALTRACKS': str(info_dict['total_tracks']).zfill(2),
            'DISCNUMBER': info_dict['disc'],
            'TOTALDISCS': info_dict['total_discs']}

        for tag in transfer_dictionary:
            song[tag] = transfer_dictionary[tag]

        song.save()

    def id3_tag(self, a_file, track_number):

        """ Similar to the function above, this function adds metadata to a
        an ID3 tag within an MP3 file. Prior to application, it sorts out a
        few formatting tidbits on how the tracks/total tracks and disc/total
        discs are applied.
        """

        title, extension = os.path.splitext(a_file)

        if extension == '.mp3':
            song = mid3.ID3(a_file)
        else:
            print("%s format not permitted by id3_paste" % extension)


        info_dict = self.info_dict

        try:
            id3_discs = "%s/%s" % (info_dict['disc'], info_dict['total_discs'])
        except KeyError:
            id3_discs = '1/1'

        try:

            id3_track = "%s/%s" % (track_number.zfill(2),
                                   str(info_dict['total_tracks']).zfill(2))
        except KeyError:
            id3_track = track_number

        transfer_dictionary = {
            'TALB': info_dict['album'],
            'TPE1': info_dict['album_artist'],
            'TPE2': info_dict['artist'],
            'TDRL': info_dict['date'],
            'TPUB': info_dict['label'],
            'TCON': info_dict['genre'],
            'TIT2': info_dict['tracks'][track_number],
            'TRCK': id3_track,
            'TPOS': id3_discs}

        for tag in transfer_dictionary:
            exec_string = 'song.add(mid3.%s(3, text="%s"))' % (tag, transfer_dictionary[tag])
            exec(exec_string)

        song.save()
