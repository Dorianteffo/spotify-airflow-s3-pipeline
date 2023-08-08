import pandas as pd 
import numpy as np 
import modules.modules as modules 
import transform_artist_data as transform 

token =modules.get_token()

artist_data = transform.transform_artist_data()
i=1
for artist in artist_data['artist_name']:
    if i==1 : 
        track1 = modules.get_all_tracks(token, artist)
        track = pd.DataFrame(track1)
    else : 
        track1 = modules.get_all_tracks(token,artist)
        track1 = pd.DataFrame(track1)
        track = pd.concat([track, track1],ignore_index=True)
    i+=1

print(track)

