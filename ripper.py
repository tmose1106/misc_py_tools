# Standard
import os
import subprocess
# Scripts
import config_parser
import metadata.album_art_paste as aap
import metadata.cd
import metadata.genre
import metadata.paste
import metadata.print

# Get information from the configuration file
# Configuration file should have been created during installation
parser = config_parser.Config_File_Parse('trip', 'trip.cfg')
configuration = parser.get_info()
print("Configuration file read")

# Get metadata online from the disc and print some info
metadata_dict = metadata.cd.musicbrainz_info()
metadata.print.print_album_information(metadata_dict)
# Add a genre to the metadata list
genre_dictionary = metadata.genre.genre_format()
metadata_dict['genre'] = metadata.genre.genre_choice(genre_dictionary)

# Set and create the output directory
output_prefix = os.path.expanduser(configuration['output_prefix'])
output_directory = "%s/%s/%s" % (output_prefix, 
                                 metadata_dict['album_artist'], 
                                 metadata_dict['album'])

if not os.path.isdir(output_directory):
    os.makedirs(output_directory)

subprocess.run(['clear'])

# Rip the tracks
for index in range(0, metadata_dict['total_tracks']):
    # Create variables holding a string and padded string of the track number
    raw_number = str(index + 1)
    pretty_number = raw_number.zfill(2)
    # Define the file title of the output file
    output_title = "%s-%s" % (pretty_number, 
                              metadata_dict['tracks'][raw_number])

    print("%s-%s" % (pretty_number, metadata_dict['tracks'][raw_number]))
    # Define the absolute output path for the output file
    output_file = "%s/%s.flac" % (output_directory, output_title)
    # Beginning the actually ripping progress
    cdparanoia_call = subprocess.Popen(['cdparanoia', '-q', '-B', raw_number, '-'], 
                                        stdout=subprocess.PIPE)
    # Meanwhile, convert the rip to FLAC through a pipe 
    flac_run = subprocess.run(["flac", "-sf", "--best", "-o", output_file, "-"], 
                              stdin=cdparanoia_call.stdout)

    metadata_paste = metadata.paste.Metadata_Paste(metadata_dict, output_file, 
                                                   raw_number)
    metadata_paste.flac_paste()
    album_art_prefix = os.path.expanduser(configuration['album_art_prefix'])
    album_art = aap.Album_Art(metadata_dict, album_art_prefix)
    album_art.flac_paste(output_file)

# All done!
os.system("eject cdrom")
print("Completed")
