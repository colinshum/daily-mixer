# ---------------------------------------------------------
# daily mix/discovery tool for spotify users
# created by @colinshum
# consider your headtops blessed with the good chunes
# ---------------------------------------------------------
# to install dependencies in terminal: pip install spotipy
# create your developer app at http://developer.spotify.com
# ---------------------------------------------------------
# usage: python dailymixer.py <spotify_username>
# ---------------------------------------------------------

import spotipy
import spotipy.util as util
import sys
import pprint

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

# ---------------------------------------------------------
# available scopes:
# https://developer.spotify.com/web-api/using-scopes/
#
# playlist-read-private
# playlist-read-collaborative
# playlist-modify-public
# playlist-modify-private
# user-follow-read
# user-follow-modify
# user-top-read
# ---------------------------------------------------------

scope = 'user-top-read playlist-modify-private playlist-modify-public'
token = util.prompt_for_user_token(username, scope)


sp = spotipy.Spotify(auth=token)
sp.trace = False


def top_tracks():
    print("This app will now generate a new playlist for your account. Please check your Spotify for today's Daily Mix!")
    results = sp.current_user_top_tracks(time_range='long_term', limit=5)
    track_uri = []

    for item in results['items']:
        track_uri.append(item['uri'])
    track_seed = ' '.join(track_uri)


    recos = sp.recommendations(seed_tracks=track_uri, limit=40)
    reco_uri = []
    for track in recos['tracks']:
        reco_uri.append(track['uri'])

    playlists = sp.user_playlist_create(username, 'Colin\'s God Tier Daily Mix')

    existing = sp.user_playlists(username, limit=1)
    for item in existing['items']:
        playid = item['id']

    results = sp.user_playlist_add_tracks(username, playid, reco_uri)

top_tracks()
