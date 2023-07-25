from bs4 import BeautifulSoup
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


Client_ID = os.environ.get("CLIENT_ID")
Client_secret = os.environ.get("CLIENT_SECRET")
redirect_uri = "http://example.com"
date = input("Which year do you want to travel to? Type the date in this format YYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
billboard_web = response.content

soup = BeautifulSoup(billboard_web, "html.parser")

songs = soup.select("li ul li h3")

song_names = [song.getText().strip() for song in songs]
# print(song_names)

scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=scope,
    client_id=Client_ID,
    client_secret=Client_secret,
    redirect_uri=redirect_uri,
    show_dialog=True,
    cache_path=".cache.txt"
    )
)

results = sp.current_user()
# print(results)
user_id = results["id"]
# print(user_id)
year = date.split("-")[0]
song_uris = []
for song in song_names:
    search_song = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(res)
    try:
        uri = search_song["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)


sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
