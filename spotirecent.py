import ConfigParser
import spotipy
import spotipy.util as util

config = ConfigParser.ConfigParser()
config.read('config.ini')

CLIENT_ID = config.get('USER', 'client_id')
CLIENT_SECRET = config.get('USER', 'client_secret')
REDIRECT_URI = config.get('USER', 'redirect_uri')
USERNAME = config.get('USER', 'username')

SCOPE = 'user-library-read playlist-read-private playlist-modify-private'

PLAYLIST_NAME = config.get('PLAYLIST', 'playlist')
NUM_TRACKS = config.getint('PLAYLIST', 'number')

token = util.prompt_for_user_token(USERNAME, scope=SCOPE, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)

if token:
    sp = spotipy.Spotify(auth=token)
    tracks = []
    results = sp.current_user_saved_tracks()
    while results:   
        for item in results['items']:
            tracks.append({'uri': item['track']['uri'], 'date': item['added_at']})
        results = sp.next(results)
    
    tracks.sort(key=lambda track: track['date'], reverse=True)
    tracks = tracks[:NUM_TRACKS]
    playlist_tracks = [t['uri'] for t in tracks]
        
    playist = None
    results = sp.current_user_playlists()
    while results:
        playlist = next((r for r in results['items'] if r['name'] == PLAYLIST_NAME), None)
        if playlist:
            break
        results = sp.next(results)
    
    if not playlist:
        playlist = sp.user_playlist_create(USERNAME, PLAYLIST_NAME, public=False)
        
    sp.user_playlist_replace_tracks(USERNAME, playlist['id'], playlist_tracks)