# Standard
import os
import subprocess
import sys
# Scripts
import json_config
import metadata.art
import metadata.cd
import metadata.dump
import metadata.genre
import metadata.write

""" This is my ripping script. It reads a JSON configuration file and
finds metadata on Musicbrainz.org using the CD's disc ID. Then it rips
the CD and exports the audio to several audio codecs as specified in
the configuration file. Finally, it adds metadata from Musicbrainz and
finally adds album art from a local database.
"""

# Get information from the configuration file
# Configuration file should have been created during first run
try:
    json_config = json_config.read_ripper_config()
    encoders = json_config['encoders']
    art_conf = json_config['album_art']
    print("Configuration file read")

except FileNotFoundError:
    json_config.write_ripper_config()
    print("Ripper config file create in ~/.config/trip folder")
    sys.exit(0)

# Get metadata online from Musicbrainz using the Disc ID and print some info
metadata_dict = metadata.cd.musicbrainz_info()
metadata.dump.print_album_information(metadata_dict)

# Add a genre to the metadata dictionary
genre_dictionary = metadata.genre.genre_format()
metadata_dict['genre'] = metadata.genre.genre_choice(genre_dictionary)

# Set the output directory for each encoder
output_dict = {}

for encoder in encoders:
    # Set and create the output directory
    output_prefix = os.path.expanduser(json_config['output_prefix'])
    encoder_prefix = os.path.expanduser(encoders[encoder]['output_dir'])
    clean_album = metadata.art.remove_special(metadata_dict['album'], '-')

    output_directory = "%s/%s/%s/%s" % (output_prefix, encoder_prefix,
                                        metadata_dict['album_artist'],
                                        clean_album)
    output_dict[encoder] = output_directory

    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

# Get album art file name and make sure the file exists in the art directory
album_art_dir = os.path.expanduser(art_conf['album_art_dir'])
album_art_file = metadata.art.find_path(metadata_dict)
album_art_path = metadata.art.art_path_check(album_art_dir, album_art_file)

# clear the screen for formatting purposes
subprocess.run(['clear'])

# Rip the tracks
for index in range(metadata_dict['total_tracks']):

    # Create variables holding a string and padded string of the track number
    raw_number = str(index + 1)
    pretty_number = raw_number.zfill(2)

    # Define the file title of the output file
    raw_title = "%s-%s" % (pretty_number, metadata_dict['tracks'][raw_number])
    clean_title = metadata.art.remove_special(raw_title, '-')

    print("%s-%s" % (pretty_number, metadata_dict['tracks'][raw_number]))
    # Define the absolute output path for the output file
    ffmpeg_commands = ['ffmpeg', '-loglevel', 'fatal', '-stats',
                       '-y', '-i', 'pipe:0']

    for encoder in encoders:

        codec = encoders[encoder]['codec']
        output_path = "%s/%s.%s" % (output_dict[encoder], clean_title, codec)

        if codec == 'flac':
            for x in ['-acodec', 'flac', output_path]:
                ffmpeg_commands.append(x)

        elif codec == 'ogg':
            bitrate = "%sk" % encoders[encoder]['bitrate']

            for x in ['-acodec', 'libvorbis', '-b:a', bitrate, output_path]:
                ffmpeg_commands.append(x)

        elif codec == 'mp3':
            bitrate = "%sk" % encoders[encoder]['bitrate']

            for x in ['-acodec', 'libmp3lame', '-b:a', bitrate, output_path]:
                ffmpeg_commands.append(x)
        else:
            print("%s is an unknown audio codec" % codec)

    # Beginning the actually ripping progress
    cdparanoia_call = subprocess.Popen(['cdparanoia', '-q', '-B', raw_number,
                                        '-'], stdout=subprocess.PIPE)

    #  Meanwhile, convert the rip to different formats through a UNIX pipe
    # using ffmpeg
    ffmpeg_run = subprocess.Popen(ffmpeg_commands, stdin=cdparanoia_call.stdout)
    ffmpeg_run.wait()

    # Load the metadata dictionary from the CD and apply it to the files
    metadata_write = metadata.write.Apply_Metadata(metadata_dict, raw_number)

    for encoder in encoders:

        codec = encoders[encoder]['codec']
        output_file = "%s/%s.%s" % (output_dict[encoder], clean_title, codec)

        if codec == 'flac':
            metadata_write.vorbis_tag(output_file, raw_number)
        elif codec == 'mp3':
            metadata_write.id3_tag(output_file, raw_number)
        elif codec == 'ogg':
            metadata_write.vorbis_tag(output_file, raw_number)
        else:
            print("%s is an unknown audio codec" % codec)

        if album_art_path != '':
            art_paste = metadata.art.Apply_Art(album_art_path)
            # Embed the album art in the audio file in enabled in config
            if art_conf['embeded_art']:

                if codec == 'flac':
                    art_paste.flac_art(output_file)
                elif codec == 'ogg':
                    art_paste.vorbis_art(output_file)
                elif codec == 'mp3':
                    art_paste.id3_art(output_file)
                else:
                    print("Album art not supported for %s." % codec)
            # Place album art in folder if enabled in config
            if art_conf['folder_art']:
                art_paste.folder_art(output_dict[encoder])

# All done!
os.system("eject cdrom")
print("Rip completed, enjoy your music!")
