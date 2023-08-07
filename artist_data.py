import pandas as pd 
import numpy as np 
import modules.extract as extract 

#get the token
token = extract.get_token()

#extract the artist data
artist_data = extract.get_all_artist(token)
artist_data = pd.DataFrame(artist_data)

#data cleaning

#drop duplicated rows
artist_data.drop_duplicates(subset=['artists_id'],inplace=True) #drop duplicated
artist_data.reset_index(drop=True)

#transform the artists_genre column into a single string
for i in range (artist_data.shape[0]): 
    artist_data.loc[i,'artists_genre'] = ','.join(artist_data.loc[i, 'artists_genre'])

print(artist_data)