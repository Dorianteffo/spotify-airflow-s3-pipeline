import pandas as pd 
import numpy as np 
import modules.extract as extract 

token =extract.get_token()

track = extract.get_all_tracks(token, 'Drake')
track = pd.DataFrame(track)

print(track['artists_name'])

