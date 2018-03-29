from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import requests
import youtube_dl

#Functions for YouTube

def find_youtube_url(search, proxies, maxDuration):
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

#Downloads the song based on the ydl_opts
def download_songs(ydl_opts, youtubeURLS):
    c = 0
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        while c < len(youtubeURLS):
            ydl.download([youtubeURLS[c]])
            c += 1
    return -1