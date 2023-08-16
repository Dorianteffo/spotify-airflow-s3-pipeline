import pandas as pd
import modules.modules as modules  
import s3fs

def etl_track(): 
    #extract track data from the api
    token =modules.get_token()
    df = modules.get_all_tracks(token, 'Lil Baby')
    df = pd.DataFrame(df)

    #data cleaning 
    #convert explicit column to bool
    df['explicit'] = df['explicit'].replace({"0.0": False,"1.0": True, 0.0 : "False", 1.0 : "True"})
    df['explicit'] = df['explicit'].astype('bool')

    df.to_csv('s3://dorian-spotify-api/tracks_data.csv')


def etl_album(): 
    #extract album data from the api
    token = modules.get_token()
    df = modules.get_all_album(token, "Lil Baby")
    df = pd.DataFrame(df)

    # data cleaning 
    #convert the release_date to datetime 
    df['release_date'] = pd.to_datetime(df['release_date'])

    df.to_csv('s3://dorian-spotify-api/album_data.csv')

