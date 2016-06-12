
# Standard
import subprocess

def special_characters(a_string, replace_character):

    """ This function removes special characters that take away from the
    reading experience or which are not permitted to be used within a file
    name.
    """

    mod_string = a_string
    removal_list = ['<>:\'"/\\|?!* ']

    for real_list in removal_list:
        for character in real_list:
            if character in mod_string:
                mod_string = mod_string.replace(str(character), '-')

    return mod_string


class Album_Art():

    def __init__(self, metadata_dictionary, file_prefix):

        self.meta_dict = metadata_dictionary
        self.file_prefix = file_prefix

        self.artist = self.meta_dict['album_artist'].lower()
        self.album = self.meta_dict['album'].lower()
    
    def get_file_name(self):
        raw_file_name = "%s-%s.jpg" % (self.artist.replace(' ', ''), 
                                       self.album.replace(' ', ''))

        clean_file_name = special_characters(raw_file_name, '-')
        
        return clean_file_name

    def flac_paste(self, flac_file):

        # The syntax for entering an image as define in the metaflac manual
        picture_file = "%s/%s" % (self.file_prefix , self.get_file_name())
        picture_syntax = "||%s||%s" % ('Front Cover', picture_file)
        picture_flag = "--import-picture-from=%s" % picture_syntax
        
        subprocess.run(['metaflac', picture_flag, flac_file])


if __name__ == '__main__':

    art_name = Album_Art({'album_artist': 'Defeater', 'album': 'Travels'}, 
                              "/home/tedm1/Pictures/resized_art")

    art_name.flac_paste("/home/tedm1/Music/Defeater/Travels/01-Blessed Burden.flac")
