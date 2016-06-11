
# Standard
import json
import os
import subprocess
# Dependencies
import discid
import musicbrainzngs

def musicbrainz_info():
    # Read the disc
    disc_read = discid.read()
    # Get the disc ID from the read object
    disc_id = disc_read.id
    # Also get the submission URL in case of an accident
    disc_submission = disc_read.submission_url

    musicbrainzngs.set_useragent("Tedm ripper", "0.0.1", "tmoseley1106@gmail.com")

    try:
        result = musicbrainzngs.get_releases_by_discid(disc_id,
                                                       includes=['artists',
                                                                 'labels',
                                                                 'recordings'])

    except musicbrainzngs.ResponseError:
        print("Disc was not found, check if available on musicbrainz.org")
        print(disc_submission)

    else:

        album_info_dict = {
            'album': result['disc']['release-list'][0]['title'],
            'album_artist': result['disc']['release-list'][0]['artist-credit'][0]['artist']['name'],
            'artist': result['disc']['release-list'][0]['artist-credit'][0]['artist']['name'],
            'date': result['disc']['release-list'][0]['date'],
            'disc_id': result['disc']['id'],
            'label': result['disc']['release-list'][0]['label-info-list'][0]['label']['name'],
            'total_tracks': result['disc']['offset-count'],
            'tracks': {}
        }
        
        for track in result['disc']['release-list'][0]['medium-list'][0]['track-list']:

            title = track['recording']['title']
            track_number = track['position']

            album_info_dict['tracks'][track_number] = title

        #print(result)   
        #print(json.dumps(result, indent=4))
        #print(album_info_dict)

        return album_info_dict
