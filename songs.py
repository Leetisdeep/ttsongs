import requests
from bs4 import BeautifulSoup


def get_songs():
    songs = []
    url_to_parse = 'https://www.tokhits.com/songs/trending'
    html = requests.get(url_to_parse).text
    soup = BeautifulSoup(html, 'html.parser')

    songs_stuff = soup.find('tbody').find_all('tr')
    for song in songs_stuff:
        if song.find('img') == None: break
        image_url = song.find('img').get('src')
        audio_url = song.find('audio').get('src')
        title = song.find('a',{'class':'hover:underline'}).get_text()
        author = song.find('div',{'class':'font-light text-slate-500'}).get_text()
        new_videos , total_videos = song.find_all('div',{'class':'text-left'})[0].get_text(),song.find_all('div',{'class':'text-left'})[1].get_text()
        tiktok_song_url = song.find('a').get('href').split('/')[-1]

        song = {
            'image_url': image_url,
            'audio_url': audio_url,
            'title': title,
            'author': author,
            'new_videos': new_videos,
            'total_videos': total_videos,
            'tiktok_song_url': tiktok_song_url,
        }
        songs.append(song)

    return songs