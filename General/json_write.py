import json

def make_default_config(output_dict, output_path):

    output_string = json.dumps(output_dict, indent=2, sort_keys=True)

    with open(output_path, 'w') as out_file:
        out_file.write(output_string)

    print("Made %s" % output_path)

if __name__ == '__main__':

    encoders = {}
    encoders[0] = {
        'codec': 'flac',
        'output_dir': '/home/tedm1/squid'
    }
    encoders[1] = {
        'codec': 'mp3',
        'bitrate': 320,
        'output_dir': '/home/tedm1/chipmunk'
    }
 
    outsy = "/home/tedm1/test_cfg.txt"

    make_default_config(encoders, outsy)
