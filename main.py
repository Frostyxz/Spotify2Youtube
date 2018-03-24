from __future__ import unicode_literals
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import requests
import youtube_dl
import json

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

#Checks if file exists
def storageChecker(file_name):
    try:
        open(file_name)
    except IOError:
        print('NOTE: Previous storage file not found, another will be made if possible.')
        return False
    return True

#Reads a json file and appends the contents to the object
def storageReader(file_name, storage):
    with open(file_name) as json_file:
        storageTemp = json.load(json_file)
        for s in storageTemp['Songs']:
            storage['Songs'].append(s)
            print('Song found:' , s['name'])
        return storage

#Appends a lists elements to the json object
def storageAppend(storage, list):
    for ele in list:
        storage['Songs'].append({
            'name': ele,
        })
    return storage

#Checks if a list's content matches a json object's content
def storageMatch(storage, list):
    for i, ele in enumerate(storage['Songs']):
        if ele['name'] in list:
            print("Song already found, removing:" , ele['name'])
            list.remove(ele['name'])
    return list

#Writes to the file
def storageWriter(file_name, storage):
    with open(file_name, 'w') as outfile:
        json.dump(storage, outfile, indent=2)

def findYTubeURL(search):
    textToSearch = search
    query = urllib.parse.quote(textToSearch)
    domain = 'https://www.youtube.com'
    url = domain + "/results?search_query=" + query

    req = requests.get(url, proxies=proxies)

    if req.status_code == 503:
        print(req.status_code, req.reason)
        return -1
    else:
        print(req.status_code, req.reason)

    html = req.text
    soup = BeautifulSoup(html, "html.parser")

    songs = soup.findAll(attrs={'class': 'yt-uix-tile-link'})
    duration = soup.findAll('span', {'class': 'video-time'})

    c = 0
    #Checks if the youtube video link isn't a playlist and the duration isn't longer than the max duration
    while True:
        if "list=" not in songs[c]['href'] and len(duration[c].text) <= maxDuration:
            print(domain + songs[c]['href'] , duration[c].text)
            return (domain + songs[c]['href'])
        else:
            c+= 1

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
if storageChecker(storageFile) == True:
    storage = storageReader(storageFile, storage)
    searchInput = storageMatch(storage, searchInput)
storage = storageAppend(storage, searchInput)
storageWriter(storageFile, storage)

if len(searchInput) == 0:
    print('No new songs were found exiting application.')
    exit()

#Finds Youtube url from song name, artist name and album name, doesn't return playlists and chooses from the first video down
c = 1
for ele in searchInput:
    print(ele)
    curURL = findYTubeURL(ele)
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
c = 1
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    while c < len(youtubeURLS):
        ydl.download([youtubeURLS[c]])
        c += 1