from dotenv import load_dotenv
import os 
import base64
from requests import post,get
import json

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#take the access token 

def get_token() : 
    auth_string = client_id + ":" + client_secret 
    #encode it 
    auth_bytes = auth_string.encode("utf-8")
    #encode using base64
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded" 
    }

    data = {"grant_type" : "client_credentials"}
    result = post(url,headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token 

def get_auth_header(token) :
    return {"Authorization" : "Bearer " + token}


def get_artist(token,limit,offset): 
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query=f"?q=year:2023&type=artist&limit={limit}&offset={offset}"

    query_url = url + query 
    result = get(query_url,headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    return json_result 

def get_all_artist(token):
    limit = 50
    offset = 0 
    total_rows = 1000
    all_artist = []
    all_followers = []
    all_id = []
    all_genre = []
    all_popularity = []
    while len(all_artist)<=total_rows : 
        result_artist = get_artist(token,limit,offset)
        for i, artists in enumerate(result_artist) : 
            all_artist.append(artists['name'])
            all_followers.append(artists['followers']['total'])
            all_id.append(artists['id'])
            all_genre.append(artists['genres'])
            all_popularity.append(artists['popularity'])
        offset += limit
        if len(result_artist) < limit :
            break
    artist_data = {"artists_id":all_id,"artist_name":all_artist, "artist_followers": all_followers, "artists_popularity": all_popularity, "artists_genre": all_genre}
    return artist_data


def get_track(token,limit,offset,artist) : 
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q=artist:{artist}&type=track&limit={limit}&offset={offset}"

    query_url = url+query
    result = get(query_url,headers = headers)
    json_result = json.loads(result.content)['tracks']['items']
    return json_result


def get_all_tracks(token,artist):
    limit = 50
    offset = 0 
    total_rows = 500
    album_name = []
    album_id = []
    duration_ms = []
    explicit = []
    track_name = []
    track_popularity = []
    track_number = []
    available_markets = []
    artist_name = []
    artist_id = []
    while len(album_name)<=total_rows : 
        track = get_track(token,limit,offset,artist)
        for i in range(len(track)) : 
            album_name.append(track[i]['album']['name'])
            album_id.append(track[i]['album']['id'])
            duration_ms.append(track[i]['duration_ms'])
            explicit.append(track[i]['explicit'])
            track_name.append(track[i]['name'])
            track_popularity.append(track[i]['popularity'])
            track_number.append(track[i]['track_number'])
            available_markets.append(track[i]['available_markets'])
            all_artist_name = [arti['name'] for arti in track[i]['artists']]
            all_artist_id = [arti['id'] for arti in track[i]['artists']]
            artist_name.append(all_artist_name)
            artist_id.append(all_artist_id)
        offset += limit
        if len(track) < limit :
            break
    tracks_data = {'track_name':track_name, 'duration_ms':duration_ms, 'explicit':explicit,'popularity':track_popularity, 'track_number':track_number,
                           'available_markets':available_markets,'artists_name': artist_name, 'artists_id':artist_id, 'album_id':album_id, 'album_name':album_name}
    return tracks_data


def get_album(token,limit,offset,artist) : 
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q=artist:{artist}&type=album&limit={limit}&offset={offset}"

    query_url = url+query
    result = get(query_url,headers = headers)
    json_result = json.loads(result.content)['albums']['items']
    return json_result


def get_all_album(token,artist) : 
    limit = 50 
    offset = 0 
    total_rows = 100
    id = []
    name = []
    type = []
    date = []
    available_markets = []
    total_tracks = []
    while len(id)<=total_rows : 
        result_album = get_album(token,limit,offset,artist)
        for i, album in enumerate(result_album) : 
            id.append(album['id'])
            name.append(album['name'])
            type.append(album['album_type'])
            date.append(album['release_date'])
            available_markets.append(album['available_markets'])
            total_tracks.append(album['total_tracks'])
            albums_data = {"id": id , 'name': name, 'type': type, 'release_date':date, 'available_markets':available_markets, 'total_tracks':total_tracks}
        offset += limit 
        if len(result_album) < limit :
            break
    return albums_data