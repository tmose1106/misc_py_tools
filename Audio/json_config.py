# Standard
import json
# Dependencies
import xdg.BaseDirectory as xdg 

def read_config(input_path):
    with open(input_path, 'r') as in_file:
        dictionary = json.load(in_file)
    
    return dictionary

def write_config(output_dict, output_path):

    output_string = json.dumps(output_dict, indent=2, sort_keys=True)

    with open(output_path, 'w') as out_file:
        out_file.write(output_string)

    print("Made %s" % output_path)

def read_ripper_config():
    
    config_path = "%s/%s" % (xdg.load_first_config('trip'), 'encoder.cfg')
    
    encoder_conf = read_config(config_path)

    return encoder_conf

def write_ripper_config():
 
    encoders = {}
    encoders[0] = {
        'codec': 'flac',
        'output_dir': '~/Music/FLAC'
    }
    encoders[1] = {
        'codec': 'mp3',
        'bitrate': 320,
        'output_dir': '~/Music/MP3_320'
    }

    config_path = "%s/%s" % (xdg.load_first_config('trip'), 'encoder.cfg')

    write_config(encoders, config_path) 


