import fitbit
import gather_keys_oauth2 as Oauth2
import time
import spotipy
import spotipy.util as util
from datetime import datetime, timedelta
import os

CLIENT_ID_FITBIT = '22DPJQ'
CLIENT_SECRET_FITBIT = 'bc41e8a701f581ce6e6288d2a01bb766'
CLIENT_ID_SPOTIFY = '1da08e2fb3994edebbf758e0fa0ab23b'
CLIENT_SECRET_SPOTIFY = '98fe97db700b44f4ad0743b945e3084b'
CALLBACK_SPOTIFY = 'http://localhost:8888/callback/'
SPOTIFY_USER = 'cv2f8pc6v4yqhx9qsgiiynji5'
SCOPE = 'user-modify-playback-state user-read-playback-state'
token = util.prompt_for_user_token(SPOTIFY_USER, SCOPE, CLIENT_ID_SPOTIFY, CLIENT_SECRET_SPOTIFY, CALLBACK_SPOTIFY)
playing_device = None
Current_Date = datetime.now()
Date = str(Current_Date)[:10]

if token:
    print("Valid Token")
    playing_device = None
    sp = spotipy.Spotify(auth = token)
    all_devices = sp.devices()['devices']
    server =  Oauth2.OAuth2Server(CLIENT_ID_FITBIT, CLIENT_SECRET_FITBIT)
    server.browser_authorize()
    ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
    REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
    client = fitbit.Fitbit(client_id = CLIENT_ID_FITBIT, client_secret = CLIENT_SECRET_FITBIT,
    access_token = ACCESS_TOKEN, refresh_token = REFRESH_TOKEN)
    if os.path.exists('logid.txt'):
        with open('logid.txt', 'r') as f:
            client.delete_sleep(f.readline()[:-1])
        os.remove('logid.txt')
    while 1:
        #Handles if you start program before midnight but go to sleep after midnight
        if Date != str(datetime.now())[:10]:
            Current_Date = datetime.now()
        Sleep_Check = client.get_sleep(Current_Date)['sleep']
        #Logic to check if spotify should stop playing
        if len(Sleep_Check) != 0:
            with open('logid.txt', 'w') as f:
                f.write(Sleep_Check[0]['logId'])
            sp = spotipy.Spotify(auth = token)
            all_devices = sp.devices()['devices']
            for device in all_devices:
                if device['is_active']:
                    playing_device = device['id']
            if playing_device is not None:
                sp.pause_playback(playing_device)
            break
        print("You are still awake.")
        time.sleep(300)
    print("Stopped Playing at", datetime.now())
else:
    print("Invalid Username.")
