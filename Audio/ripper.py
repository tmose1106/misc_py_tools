# Standard
import os
import subprocess
import sys
# Scripts
import json_config
import metadata.album_art_paste as aap
import metadata.cd
import metadata.genre
import metadata.paste
import metadata.print

# Get information from the configuration file
# Configuration file should have been created during installation
try:
    json_config = json_config.read_ripper_config()
    print("Configuration file read")
except FileNotFoundError:
    json_config.write_ripper_config()
    print("Ripper configuration create in your ~/.config/trip folder")
    sys.exit(0)

# Get metadata online from the disc and print some info
metadata_dict = metadata.cd.musicbrainz_info()
metadata.print.print_album_information(metadata_dict)

# Add a genre to the metadata list
genre_dictionary = metadata.genre.genre_format()
metadata_dict['genre'] = metadata.genre.genre_choice(genre_dictionary)

for encoder in json_config:
    # Set and create the output directory
    output_prefix = os.path.expanduser(json_config[encoder]['output_dir'])
    output_directory = "%s/%s/%s" % (output_prefix,
                                     metadata_dict['album_artist'], 
                                     aap.remove_special(metadata_dict['album'], '-'))

    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

# clear the screen for formatting purposes
subprocess.run(['clear'])

# Rip the tracks
for index in range(metadata_dict['total_tracks']):
    
    # Create variables holding a string and padded string of the track number
    raw_number = str(index + 1)
    pretty_number = raw_number.zfill(2)
    
    # Define the file title of the output file
    output_title = "%s-%s" % (pretty_number, 
                              metadata_dict['tracks'][raw_number])

    print("%s-%s" % (pretty_number, metadata_dict['tracks'][raw_number]))
    # Define the absolute output path for the output file
    ffmpeg_commands = ['ffmpeg', '-loglevel', 'fatal', '-stats', '-y', '-i', 
                       'pipe:0']
    output_file_dict = {}

    for encoder in json_config:
        
        codec = json_config[encoder]['codec']
        output_path = "%s/%s.%s" % (json_config[encoder]['output_dir'],
                                    aap.remove_special(output_title, '-'), 
                                    codec)
        output_file_dict[encoder] = (codec, output_path)
        
        if codec == 'flac':
            for x in ['-acodec', 'flac', output_path]:
                ffmpeg_commands.append(x)
        elif codec == 'mp3':

            bitrate = "%sk" % json_config[encoder]['bitrate']

            for x in ['-acodec', 'libmp3lame', '-b:a', bitrate, output_path]:
                ffmpeg_commands.append(x)
        else:
            print("%s is an unknown audio codec" % codec)

    # Beginning the actually ripping progress
    cdparanoia_call = subprocess.Popen(['cdparanoia', '-q', '-B', raw_number,
                                        '-'], stdout=subprocess.PIPE)
    
    # Meanwhile, convert the rip to different formats through a UNIX pipe using ffmpeg
    ffmpeg_run = subprocess.run(ffmpeg_commands, stdin=cdparanoia_call.stdout)
    
    # Load the metadata dictionary from the CD and apply it to the files
    metadata_paste = metadata.paste.Metadata_Paste(metadata_dict, raw_number)

    for encoder in output_file_dict:
        
        codec, output_file = output_file_dict[encoder]

        if codec == 'flac':
            metadata_paste.flac_paste(output_file)
        elif codec == 'mp3':
            metadata_paste.id3_paste(output_file)
        else:
            print("%s is an unknown audio codec" % codec)
    """ 
    # Apply album art to the files
    album_art_prefix = os.path.expanduser(configuration['album_art_prefix'])
    album_art = aap.Album_Art(metadata_dict, album_art_prefix)
    album_art.flac_paste(output_file_one)
    """

# All done!
os.system("eject cdrom")
print("Completed")
