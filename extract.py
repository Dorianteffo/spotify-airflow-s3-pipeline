import pandas as pd 
import modules.modules as modules 

def tracks_data(): 
    token =modules.get_token()

    track = modules.get_all_tracks(token, 'Lil Baby')
    track = pd.DataFrame(track)

    return track

def album_data() : 
    token = modules.get_token()

    album = modules.get_all_album(token, "Lil Baby")
    album = pd.DataFrame(album)

    return album


