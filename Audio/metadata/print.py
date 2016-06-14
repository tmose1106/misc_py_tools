
def print_album_information(metadata_dictionary):

    print("Album Info:")

    print("Title:\t\t%s" % metadata_dictionary['album'])
    print("Artist:\t\t%s" % metadata_dictionary['artist'])
    print("Year:\t\t%s" % metadata_dictionary['date'][:4])
    print("Tracks:\t\t%s" % metadata_dictionary['total_tracks'])
    print()

