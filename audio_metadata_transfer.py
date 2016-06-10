import mutagen
import mutagen.flac as mflac
import mutagen.id3 as mid3

mpeg_transfer_dict = {
    'ALBUM': 'TALB',
    'ALBUM_ARTIST': 'TPE1',
    'ARTIST': 'TPE2',
    'DATE': 'TDRL',
    'GENRE': 'TCON',
    'TITLE': 'TIT2',
    }


class Metadata_Transfer:

    def __init__(self, flac_file, mpeg_file):

        """ This function only creates objects of the two imported files.
        """
        self.in_song = mflac.FLAC(flac_file)
        self.out_song = mid3.ID3(mpeg_file) 

    def flac_to_mpeg(self):
        
        """ This function is responsible for reading a mutagen FLAC object,
        converting its tags into a dictionary of ID3 keys and tag values, and
        finally adding them to a mutagen ID3 object.
        """

        tag_dict = {}
        
        flac = self.in_song
        mpeg = self.out_song

        try:
            value = "%s/%s" % (flac['TRACKNUMBER'], flac['TOTALTRACKS'])
            tag_dict['TRCK'] = value
        except KeyError:
            tag_dict['TRCK'] = flac['TRACKNUMBER']

        try:
            value = "%s/%s" % (flac['DISCNUMBER'], flac['TOTALDISCS'])
            tag_dict['TPOS'] = value
        except KeyError:
            tag_dict['TPOS'] = "1/1"

        for flac_tag in mpeg_transfer_dict:
            
            try:
                key = mpeg_transfer_dict[flac_tag]
                value = flac[flac_tag]
                tag_dict[key] = value
            
            except KeyError:
                print("WARNING: FLAC tag %s not found!" % flac_tag)

        print(tag_dict)

        for mpeg_tag in tag_dict:

            value = tag_dict[mpeg_tag]
            
            if type(value) == list:
                value = value[0]
            # Since tags are strings, the command is made a string and executed
            execute_str = "mpeg.add(mid3.%s(3, text='%s'))" % (mpeg_tag, value)
            
            exec(execute_str)
