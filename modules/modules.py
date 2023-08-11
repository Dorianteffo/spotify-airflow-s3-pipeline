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
    total_rows = 900
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
    tracks_data = {'track_name':track_name, 'duration_ms':duration_ms, 'explicit':explicit,'popularity':track_popularity,
                    'track_number':track_number,'available_markets':available_markets,
                    'artists_name': artist_name, 'artists_id':artist_id, 'album_id':album_id, 'album_name':album_name}
    return tracks_data


def get_album(token,limit,offset,artist) : 
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q=artist:{artist}&type=album&limit={limit}&offset={offset}"

    query_url = url+query
    result = get(query_url,headers = headers)
    json_result = json.loads(result.content)['albums']['items']
    return json_result

def get_album_info(token, id): 
    url = f"https://api.spotify.com/v1/albums/{id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
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
    artist_name = []
    artist_id = []
    popularity = []
    label = []
    while len(id)<=total_rows : 
        album = get_album(token,limit,offset,artist)
        for i in range(len((album))): 
            id.append(album[i]['id'])
            name.append(album[i]['name'])
            type.append(album[i]['album_type'])
            date.append(album[i]['release_date'])
            available_markets.append(album[i]['available_markets'])
            total_tracks.append(album[i]['total_tracks'])
            all_artist_name = [arti['name'] for arti in album[i]['artists']]
            all_artist_id = [arti['id'] for arti in album[i]['artists']]
            artist_name.append(all_artist_name)
            artist_id.append(all_artist_id)
            popularity.append(get_album_info(token,album[i]['id'])['popularity'])
            label.append(get_album_info(token,album[i]['id'])['label'])
        offset += limit 
        if len(album) < limit :
            break
    albums_data = {"id": id , 'name': name, 'type': type, 'release_date':date,
                    'available_markets':available_markets, 'total_tracks':total_tracks, 
                    "label":label, "popularity" : popularity,
                    "artist_name": artist_name, "artist_id": artist_id}
    return albums_data