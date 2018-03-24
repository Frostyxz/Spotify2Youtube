from __future__ import unicode_literals
from bs4 import BeautifulSoup
import storageFunctions
import yTFunctions

#Search term                                             | URL                                        |Time
#Mountain Sound Of Monsters and Men My Head Is An Animal | https://www.youtube.com/watch?v=hQJv7fcQduM 4:35
#This is bugged, it says a time of 4:35 but the video is 1:16:20, I don't know why this is happening it doesn't occur with the other songs

#If a video is unavailable it will crash for e.g.
#Search term                            | URL                                       |Time
#Naive The Kooks Inside In / Inside Out https://www.youtube.com/watch?v=jkaMiaRLgvY 3:29
#This video is unavailable and crashes the program

#TODO
#1. Set up multiple proxies in case on fails
#2. Make some of the code prettier with dem functions and enumerate if possible instead of counters

#File location or url for spotify playlist
url = r"C:\Users\steel\Desktop\spotifysource.html"

soup = BeautifulSoup(open(url), "html.parser")

searchInput = []

#9 minutes 99 seconds = 9:59 so 5 would be 99:59
maxDuration = 4

#Proxies to connect through go here, Youtube seems to block an ip with a 503 error after to many queries
proxies = {
  'https': 'https://37.120.177.241:3128',
}

#Json stuff
#Path to the json file
storageFile = 'storage.txt'
#Json object
storage = {}
storage['Songs'] = []

#Getting song/track name
for count, song in enumerate(soup.find_all('span', {'class' : 'tracklist-name'})):
    currentSong = "".join(song.strings)
    searchInput.append(currentSong)

#Getting artist Album and artist name
for count, song in enumerate(soup.find_all('span', {'class' : 'artists-album ellipsis-one-line'})):
    currentSong = "".join(song.strings)
    stringSplit = currentSong.split("â€¢")
    searchInput[count] += " " + stringSplit[0] + " " + stringSplit[1]

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