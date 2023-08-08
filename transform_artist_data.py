import pandas as pd 
import numpy as npo
import extract_artist_data as extract 

def transform_artist_data():
    #data cleaning
    artist_data = extract.extract_artist()
    #drop duplicated rows
    artist_data = artist_data.drop_duplicates(subset=['artists_id']) #drop duplicated
    artist_data = artist_data.reset_index(drop=True)

    #transform the artists_genre column into a single string
    for i in range (artist_data.shape[0]): 
        artist_data.loc[i,'artists_genre'] = ','.join(artist_data.loc[i, 'artists_genre'])

    artist_data.to_csv('artist_data.csv')

    return artist_data
