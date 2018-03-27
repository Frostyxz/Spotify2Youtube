import sys
import spotipy
import spotipy.util as util

class spotify:
    def __init__(self, input_username, input_scope, input_spotipyData):
        self.username = input_username
        self.scope = input_scope
        self.spotipyData = input_spotipyData
        self.token = util.prompt_for_user_token(self.username,self.scope,client_id=self.spotipyData['client_id'],client_secret=self.spotipyData['client_secret'],redirect_uri=self.spotipyData['redirect_uri'])
        self.sp = spotipy.Spotify(auth=self.token)

    def get_yourMusicLibrary_tracks(self):
        results = self.sp.current_user_saved_tracks()
        tracks = results['items']
        tracksSearch = []
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        for item in tracks:
            track = item['track']
            tracksSearch.append(track['name'] + ' - ' + track['artists'][0]['name'])
        return tracksSearch