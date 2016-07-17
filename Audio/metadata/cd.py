# Standard
import json
import os
import subprocess
import sys
# Dependencies
import discid
import musicbrainzngs

def musicbrainz_info():
    try:
        # Read the disc
        disc_read = discid.read()
        # Get the disc ID from the read object
        disc_id = disc_read.id
        # Also get the submission URL in case of an accident
        disc_submission = disc_read.submission_url
    except:
        print("Please insert a compact disc")
        sys.exit(0)

    musicbrainzngs.set_useragent("Tedm ripper", "0.0.1", "tmoseley1106@gmail.com")

    try:
        result = musicbrainzngs.get_releases_by_discid(disc_id,
                                                       includes=['artists',
                                                                 'labels',
                                                                 'recordings'])
        release_list = result['disc']['release-list'][0]
        number_of_discs = release_list['medium-count']
        disc_number_list = list(range(1, (number_of_discs + 1)))
        disc_string = ', '.join(map(str, disc_number_list))
        if number_of_discs > 1:
            print('This disc is part of a set. You can choose from %s' % disc_string)

            choice = input('Please enter the proper disc number: ')
            if not int(choice) in disc_number_list:
                print("Invalid disc number")
                sys.exit(0)
            pretty_disc_number = choice
            raw_disc_number = int(pretty_disc_number) - 1
        else:
            pretty_disc_number = '1'
            raw_disc_number = 0

    except musicbrainzngs.ResponseError:
        print("Disc was not found in database, check if available on musicbrainz.org")
        print(disc_submission)
        sys.exit(0)
    except musicbrainzngs.musicbrainz.NetworkError:
        print("You do not seem to be connected to the internet")
        sys.exit(0)
    else:
        album_info_dict = {
            'album': release_list['title'],
            'album_artist': release_list['artist-credit'][0]['artist']['name'],
            'artist': release_list['artist-credit'][0]['artist']['name'],
            'date': release_list['date'],
            'disc': pretty_disc_number,
            'disc_id': result['disc']['id'],
            'total_discs': str(number_of_discs),
            'total_tracks': release_list['medium-list'][raw_disc_number]['track-count'],
            'tracks': {}
        }
        try:
            album_info_dict['label'] = release_list['label-info-list'][0]['label']['name']
        except IndexError:
            album_info_dict['label'] = ''

        for track in release_list['medium-list'][raw_disc_number]['track-list']:

            title = track['recording']['title']
            track_number = track['position']

            album_info_dict['tracks'][track_number] = title

        return album_info_dict

if __name__ == '__main__':
    disc_info = musicbrainz_info()
    json_info = json.dumps(disc_info, indent=2)
    print(json_info)
