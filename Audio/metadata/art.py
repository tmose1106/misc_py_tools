# Standard
import base64
import os
import shutil
import subprocess
import sys
# Dependencies
import mutagen.flac as mflac
import mutagen.id3 as mid3
import mutagen.oggvorbis as mogg


def remove_space(a_string, replace_character):

    """ Remove all spaces from a string and return a 'spaceless' version of
    the original string.
    """

    modified_string = a_string.replace(' ', '')

    return modified_string

def remove_special(a_string, replace_character):

    """ Remove special characters that take away from the reading
    experience or which are not permitted to be used within a file
    name by the OS. Returns a modified version of the string without
    special characters.
    """

    mod_string = a_string
    removal_list = ['<>:\'"/\\|?!*']

    for real_list in removal_list:
        for character in real_list:
            if character in mod_string:
                mod_string = mod_string.replace(str(character), '-')

    return mod_string

def name_clean(a_string):

    """ Just run the two functions above to 'clean' the string for album
    art purposes.
    """
    spaceless_string = remove_space(a_string, '')
    clean_string = remove_special(spaceless_string, '-')

    return clean_string

def find_path(metadata_dictionary):

    artist = metadata_dictionary['album_artist'].lower()
    album = metadata_dictionary['album'].lower()

    raw_file_name = "%s-%s.jpg" % (artist.replace(' ', ''),
                                   album.replace(' ', ''))

    clean_file_name = remove_special(raw_file_name, '-')

    return clean_file_name


def art_path_check(a_path, a_file):

    art_path = "%s/%s" % (a_path, a_file)

    while not os.path.isfile(art_path):
        print("Album art not found:")
        print(" Directory: %s" % art_path)
        print(" File Name: %s" % a_file)

        prompt = input("Enter path manually? [Y/n/q] ")

        if prompt in ['y', 'Y', '']:
            art_path = prompt
            continue

        elif prompt in ['N', 'n']:
            art_path = ''
            break

        elif prompt in ['Q', 'q']:
            sys.exit(0)

        else:
            print("%s is an invalid response" % prompt)
            continue

class Apply_Art():

    def __init__(self, art_file):

        if os.path.isfile(art_file):
            #print("Art file loading!")
            self.art_file = art_file
            self.art_data = open(art_file, 'rb').read()
        else:
            print("No art file found")

    def flac_art(self, flac_file):

        song = mflac.FLAC(flac_file)

        pic = mflac.Picture()
        pic.data = self.art_data
        pic.type = 3
        pic.mime = 'image/jpeg'

        song.add_picture(pic)
        song.save()

    def id3_art(self, mp3_file):

        song = mid3.ID3(mp3_file)

        tag = mid3.APIC(encoding=3, mime='image/jpeg', type=3,
                        desc="Front Cover", data=self.art_data)
        song.add(tag)
        song.save()

    def vorbis_art(self, vorbis_file):

        song = mogg.OggVorbis(vorbis_file)

        pic = mflac.Picture()
        pic.data = self.art_data
        pic.type = 3
        pic.mime = 'image/jpeg'

        song['METADATA_BLOCK_PICTURE'] = str(base64.b64encode(pic.write()),
                                             'utf-8')
        song.save()

    def folder_art(self, output_dir):

        output_file = "%s/folder.jpg" % output_dir

        shutil.copy2(self.art_file, output_file)
