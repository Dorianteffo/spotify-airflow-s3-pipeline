import pandas as pd 
import numpy as np 
import modules.modules as modules 

def extract_artist(): 
    #get the token
    token = modules.get_token()

    #extract the artist data
    artist_data = modules.get_all_artist(token)
    artist_data = pd.DataFrame(artist_data)
    return artist_data

