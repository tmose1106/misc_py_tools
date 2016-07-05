# Standard
import glob
import os
import sys
# Dependencies
import wand.image

def give_file_title(a_file):

    basename = os.path.basename(a_file)
    title = os.path.splitext(basename)[0]

    return title

def remove_spaces(a_string, replace_character):

    modified_string = a_string.replace(' ', '')

    return modified_string

def remove_special(a_string, replace_character):

    """ This function removes special characters that take away from the
    reading experience or which are not permitted to be used within a file
    name.
    """

    mod_string = a_string
    removal_list = ['<>:\'"/\\|?!*']

    for real_list in removal_list:
        for character in real_list:
            if character in mod_string:
                mod_string = mod_string.replace(str(character), '-')

    return mod_string

# The script
file_dict = {}
input_dir = sys.argv[1]
output_dir = sys.argv[2]

for format in ['jpg', 'png']:

    glob_path = "%s/*.%s" % (input_dir, format)

    glob_files = glob.glob(glob_path)

    for a_file in glob_files:
        file_title = give_file_title(a_file)

        file_dict[a_file] = file_title

for pic_file in file_dict:

    space_title = remove_spaces(file_dict[pic_file], '')
    clean_title = remove_special(space_title, '-')
    output_file = "%s/%s.jpg" % (output_dir, clean_title.lower())

    with wand.image.Image(filename=pic_file) as original:
        with original.convert('jpeg') as converted:
            converted.resize(500, 500)
            converted.save(filename=output_file)

#print(file_dict)
