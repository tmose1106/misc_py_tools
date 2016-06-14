import json

def file_read(input_path):
    with open(input_path, 'r') as in_file:
        dictionary = json.load(in_file)
    
    return dictionary


if __name__ == '__main__':
    
    a_file = '/home/tedm1/test_cfg.txt'
    
    reader = file_read(a_file)
    
    for encoder in reader:

        codec = reader[encoder]['codec']

        print("Encoder %s:" % encoder)
        if codec in ['flac']:
            print("  Codec: %s" % codec)
        else:
            print("  Codec: %s (at %s Kb/s)" % (codec, reader[encoder]['bitrate']))
        print("  Out: %s" % reader[encoder]['output_dir'])

