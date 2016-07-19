# Standard
import glob
import os
import subprocess
import sys
# Scripts
import json_config
import metadata.art
import metadata.genre
import metadata.read
import metadata.write

# Get information from the configuration file
# Configuration file should have been created during first run
try:
    json_config = json_config.read_convert_config()
    encoders = json_config['encoders']
    art_conf = json_config['album_art']
    print("Configuration file read")

except FileNotFoundError:
    json_config.write_convert_config()
    print("Converter config file create in ~/.config/trip folder")
    sys.exit(0)

in_folder = sys.argv[1]
in_files = glob.glob("%s/*.flac" % in_folder)

# Set the output directory for each encoder
output_dict = {}

for encoder in encoders:
    # Set and create the output directory
    output_prefix = os.path.expanduser(json_config['output_prefix'])
    encoder_prefix = os.path.expanduser(encoders[encoder]['output_dir'])

    root_output_directory = "%s/%s" % (output_prefix, encoder_prefix)
    output_dict[encoder] = root_output_directory

for a_file in in_files:

    song = metadata.read.Read_Metadata(a_file)
    info = song.flac_tag()

    # Define the file title of the output file
    track_number = info['track_number']
    raw_title = "%s-%s" % (track_number, info['title'])
    clean_title = metadata.art.remove_special(raw_title, '-')
    clean_album = metadata.art.remove_special(info['album'], '-')

    ffmpeg_commands = ['ffmpeg', '-loglevel', 'fatal',
                       '-y', '-i', a_file]
    output_path = ()

    for encoder in encoders:

        codec = encoders[encoder]['codec']
        file_output_directory = "%s/%s/%s" % (output_dict[encoder],
                                              info['album_artist'],
                                              clean_album)

        if not os.path.isdir(file_output_directory):
            os.makedirs(file_output_directory)

        output_path = "%s/%s.%s" % (file_output_directory, clean_title, codec)
        bitrate = "%sk" % encoders[encoder]['bitrate']

        if codec == 'ogg':
            for x in ['-acodec', 'libvorbis', '-b:a', bitrate, output_path]:
                ffmpeg_commands.append(x)
        elif codec == 'mp3':
            for x in ['-acodec', 'libmp3lame', '-b:a', bitrate, output_path]:
                ffmpeg_commands.append(x)
        else:
            print("%s is an unknown audio codec" % codec)

    print(raw_title)
    subprocess.run(ffmpeg_commands)

    metadata_write = metadata.write.Apply_Metadata(info, track_number,
                                                   info['title'])
    for encoder in encoders:

        codec = encoders[encoder]['codec']

        if codec == 'mp3':
            metadata_write.id3_tag(output_path)
        elif codec == 'ogg':
            metadata_write.vorbis_tag(output_path)
        else:
            print("%s is an unknown audio codec" % codec)
