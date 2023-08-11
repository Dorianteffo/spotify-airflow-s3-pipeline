import pandas as pd
import extract 

def etl_track(): 
    df = extract.tracks_data()
    #delete unnecessary column 
    df = df.drop(['Unnamed: 0'], axis=1)

    #convert explicit column to bool
    df['explicit'] = df['explicit'].replace({"0.0": False,"1.0": True, 0.0 : "False", 1.0 : "True"})
    df['explicit'] = df['explicit'].astype('bool')

    #strip unnecessary characters
    char_strip = ["[", "]", "'", '"']
    for char in char_strip : 
        df['artists_name'] = df['artists_name'].str.replace(char, '')
        df['available_markets'] = df['available_markets'].str.replace(char, '')
        df['artists_id'] = df['artists_id'].str.replace(char, '')

    df.to_csv('s3://dorian-spotify-api/tracks_data')

def etl_album(): 
    df = extract.album_data()

    #delete unnecessary column
    df = df.drop('Unnamed: 0', axis=1)

    #convert the release_date to datetime 
    df['release_date'] = pd.to_datetime(df['release_date'])
    
    #strip unnecessary characters
    char_strip = ["[", "]", "'", '"']
    for char in char_strip : 
        df['artist_name'] = df['artist_name'].str.replace(char, '')
        df['available_markets'] = df['available_markets'].str.replace(char, '')
        df['artist_id'] = df['artist_id'].str.replace(char, '')
    df.to_csv('s3://dorian-spotify-api/album_data.csv')

