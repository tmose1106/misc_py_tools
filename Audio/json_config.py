# Standard
import json
# Dependencies
import xdg.BaseDirectory as xdg

CONVERTER_CONFIG_FILE = 'converter.cfg'
RIPPER_CONFIG_FILE = 'ripper.cfg'

def read_config(input_path):
    with open(input_path, 'r') as in_file:
        dictionary = json.load(in_file)

    return dictionary

def write_config(output_dict, output_path):

    output_string = json.dumps(output_dict, indent=2, sort_keys=True)

    with open(output_path, 'w') as out_file:
        out_file.write(output_string)

    print("Made %s" % output_path)

def read_convert_config():

    config_path = "%s/%s" % (xdg.load_first_config('trip'),
                             CONVERTER_CONFIG_FILE)
    config_dict = read_config(config_path)

    return config_dict

def write_convert_config():

    album_art_dict = {
        'album_art_dir': "~/Pictures/album_art",
        'embeded_art': True,
        'folder_art': False
    }

    encoders_dict = {}
    encoders_dict[0] = {
        'codec': 'mp3',
        'bitrate': 320,
        'output_dir': 'MP3_320'
    }

    config_out = {
        'album_art': album_art_dict,
        'encoders': encoders_dict,
        'output_prefix': "~/Music"
    }

    config_path = "%s/%s" % (xdg.load_first_config('trip'),
                             CONVERTER_CONFIG_FILE)
    write_config(config_out, config_path)

def read_ripper_config():

    config_path = "%s/%s" % (xdg.load_first_config('trip'), RIPPER_CONFIG_FILE)
    config_dict = read_config(config_path)

    return config_dict

def write_ripper_config():

    album_art_dict = {
        'album_art_dir': "~/Pictures/album_art",
        'embeded_art': True,
        'folder_art': False
    }

    encoders_dict = {}
    encoders_dict[0] = {
        'codec': 'flac',
        'output_dir': 'FLAC'
    }
    encoders_dict[1] = {
        'codec': 'mp3',
        'bitrate': 320,
        'output_dir': 'MP3_320'
    }

    config_out = {
        'album_art': album_art_dict,
        'encoders': encoders_dict,
        'output_prefix': "~/Music"
    }

    config_path = "%s/%s" % (xdg.load_first_config('trip'), RIPPER_CONFIG_FILE)

    write_config(config_out, config_path)
