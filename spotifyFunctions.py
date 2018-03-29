import sys
import spotipy
import spotipy.util as util


class spotipyHandle:
    def __init__(self, input_username, input_scope, input_spotipyData):
        self.username = input_username
        self.scope = input_scope
        self.spotipyData = input_spotipyData
        self.token = util.prompt_for_user_token(self.username,self.scope,client_id=self.spotipyData['client_id'],client_secret=self.spotipyData['client_secret'],redirect_uri=self.spotipyData['redirect_uri'])
        self.sp = spotipy.Spotify(auth=self.token)

    def get_favorite_playlist_tracks(self):
        results = self.sp.current_user_saved_tracks()
        tracks = results['items']
        tracksSearch = []
        #Theres a 50 limit return so this fixes that
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        for item in tracks:
            track = item['track']
            tracksSearch.append(track['name'] + ' - ' + track['artists'][0]['name'])
        return tracksSearch

#Returns a dictionary with all playlist names bound with their respective id
#If a user has two playlists with the exact same name the dictionary will wipe the first playlist
    def get_playlists_ID(self):
        playlists = self.sp.current_user_playlists()
        playlist = playlists['items']
        playlistReturn = {}
        while playlists['next']:
            playlists = self.sp.next(playlists)
            playlist.extend(playlists['items'])
        for item in playlist:
            playlistName = item['name']
            playlistID = item['id']

            #Gets the uri of the playlist thats used to get the playlists tracks
            playlistURI = item['uri']
            playlistURI = playlistURI.split(':')[2]

            #array stores the uri and id of a playlist that gets appended to the dictionary so they can be called with the same key
            #[0] playlistID, [1] username
            playlistData = []
            playlistData.append(playlistID)
            playlistData.append(playlistURI)

            playlistReturn[playlistName] = playlistData
        return playlistReturn

    def get_playlist_tracks(self, playlistID, username=None):
        if username == None:
            username = self.username
        results = self.sp.user_playlist_tracks(username, playlistID)
        tracks = results['items']
        tracksSearch = []
        # Theres a 50 limit return so this fixes that
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        for item in tracks:
            track = item['track']
            tracksSearch.append(track['name'] + ' - ' + track['artists'][0]['name'])
        return tracksSearch