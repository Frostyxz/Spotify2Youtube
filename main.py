from __future__ import unicode_literals
import storageFunctions
import yTFunctions
import spotifyFunctions

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
#3. Use the spotify api to access the playlists
#4. Make a config file so its PyInstaller exe works easier (add ydl_opts to config file)
#5. Add a path variable to the song downloader (The storage should also go there? or give an option for an independent playlist?)

#File location or url for spotify playlist
searchInput = []

#9 minutes 99 seconds = 9:59 so 5 would be 99:59
maxDuration = 4

#Proxies to connect through go here, Youtube seems to block an ip with a 503 error after to many queries
#You can make ftp: and htpp:, I'm not sure if you can add multiple of the same though, have to test.
proxies = {
  'https': 'https://37.120.177.241:3128',
}

#Json stuff
#Path to the json file
storageFile = 'storage.txt'
#Json object
storage = {}
storage['Songs'] = []

#Spotify stuff
#What the application wants permission to do
scope = 'user-library-read'

#You get this by making a spotify app. Make sure you get the redirect_url to be the same in the settings of the app to here, otherwise an error will happen
spotipyData = {
    'client_id': 'yourClientIDHere',
    'client_secret': 'yourClientSecretHere',
    'redirect_uri': 'http://localhost'
}

#Username of the spotify account. Facebook usernames are a sequence of numbers, I'm not sure about non facebook accounts
username = 'yourUserNameHere'

#Getting song/track name
spotify = spotifyFunctions.spotify(username, scope, spotipyData)
searchInput = spotify.get_yourMusicLibrary_tracks()

youtubeURLS = []

#Json stuff
if storageFunctions.storageChecker(storageFile) == True:
    storage = storageFunctions.storageReader(storageFile, storage)
    searchInput = storageFunctions.storageMatch(storage, searchInput)
storage = storageFunctions.storageAppend(storage, searchInput)
storageFunctions.storageWriter(storageFile, storage)

if len(searchInput) == 0:
    print('No new songs were found exiting application.')
    # Stops the window from auto closing
    input("Press enter to exit: ")
    exit()

#Finds Youtube url from song name, artist name and album name, doesn't return playlists and chooses from the first video down
c = 1
for ele in searchInput:
    print(ele)
    curURL = yTFunctions.findYTubeURL(ele, proxies, maxDuration)
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
yTFunctions.downloadSongs(ydl_opts, youtubeURLS)

#Stops the window from auto closing
input("Press enter to exit: ")