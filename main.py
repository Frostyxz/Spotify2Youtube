from __future__ import unicode_literals
import storageFunctions
import yTFunctions
import spotifyFunctions
import configReader

#Search term                                             | URL                                        |Time
#Mountain Sound Of Monsters and Men My Head Is An Animal | https://www.youtube.com/watch?v=hQJv7fcQduM 4:35
#This is bugged, it says a time of 4:35 but the video is 1:16:20, I don't know why this is happening it doesn't occur with the other songs

#If a video is unavailable it will crash for e.g.
#Search term                            | URL                                       |Time
#Naive The Kooks Inside In / Inside Out https://www.youtube.com/watch?v=jkaMiaRLgvY 3:29
#This video is unavailable and crashes the program

#soup = BeautifulSoup(open(url), "html.parser") Crashes if theres a Japanese character, probably more if tested

#TODO
#1. Set up multiple proxies in case on fails
#2. Make some of the code prettier with dem functions and enumerate if possible instead of counters
#3. Make a config file so its PyInstaller exe works easier (add ydl_opts to config file)
#4. Add a path variable to the song downloader (The storage should also go there? or give an option for an independent playlist?)

if configReader.check_config('config.ini') == False:
    print('A template will be made. The application will close after creating the template so you should complete the config file.')
    configReader.create_config_template()
    exit()

#4 = 9 minutes 99 seconds = 9:59 so 5 would be 59:59
youtubeSettings = configReader.read_config_section('Youtube')

#Proxies to connect through go here, Youtube seems to block an ip with a 503 error after to many queries
#You can make ftp: and htpp:, I'm not sure if you can add multiple of the same though, have to test.
#Sometimes the proxie hosts fucks you, try changing both the http and https proxies if you are getting [WinError 10054] or something similar
proxies = configReader.read_config_section('Proxies')

#Spotify stuff
#You get this by making a spotify app. Make sure you get the redirect_url to be the same in the settings of the app to here, otherwise an error will happen
spotipyData = configReader.read_config_section('SpotifyApp')

#Username - Username of the Spotify account. Facebook username's are a sequence of numbers, I'm not sure about non facebook accounts
#Scope - What the application wants permission to do
spotifyInfo = configReader.read_config_section('Spotify')

#Json stuff
#Path to the json file
storageFile = configReader.read_config_section('Storage')
#Json object
storage = {}
storage['Songs'] = []

#File location or url for spotify playlist
searchInput = []

#Initialising spotify class
spotify = spotifyFunctions.spotipyHandle(spotifyInfo['username'], spotifyInfo['scope'], spotipyData)

#Finding all of the users playlists
avaliablePlaylists = spotify.get_playlists_id()

print('Playlists found: ')

#Prints Favorites playlist since that won't be found it must be done separately
print('> Favorites')

#Prints all found playlists
for playlist in avaliablePlaylists:
    print('>', playlist)
print('Please type a playlist name exactly the same as shown above.')

#The exact name of a playlist should be given as a string
userInputPlaylist = input('> ')

#Gets the track's name and artist from the playlist, since the favorite's playlist isn't obtainable in user_playlist_tracks() this is a work around
if userInputPlaylist != 'Favorites':
    searchInput = spotify.get_playlist_tracks(avaliablePlaylists[userInputPlaylist][0], avaliablePlaylists[userInputPlaylist][1])
else:
    searchInput = spotify.get_favorite_playlist_tracks()

#The YouTube video /watch URL, values are from yTFunctions.findYTubeURL
youtubeURLS = []

#Json storage file checker, sees if the file exists and if it does it compares it to the list and deletes previously downloaded songs
#then it appends the list to the json object and the json object is  dumped to the file completely re-writing it
if storageFunctions.storage_checker(storageFile['fileName']) == True:
    storage = storageFunctions.storage_reader(storageFile['fileName'], storage)
    searchInput = storageFunctions.storage_match(storage, searchInput)
storage = storageFunctions.storage_append(storage, searchInput)
storageFunctions.storage_writer(storageFile['fileName'], storage)

if len(searchInput) == 0:
    print('No new songs were found exiting application.')
    # Stops the window from auto closing
    input("Press enter to exit: ")
    exit()

#Finds Youtube url from song name, artist name and album name, doesn't return playlists and chooses from the first video down
c = 1
for ele in searchInput:
    print(ele)
    curURL = yTFunctions.find_youtube_url(ele, proxies, int(youtubeSettings['maxDuration']))
    youtubeURLS.append(curURL)
    print(c , r"/" , (len(searchInput)))
    c += 1

#Downloader options
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

#Downloads video
yTFunctions.download_songs(ydl_opts, youtubeURLS)

#Stops the window from auto closing
input("Press enter to exit: ")