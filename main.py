import json
import requests
from secrets import spotify_user_id, discover_weekly
from datetime import date
from requests.api import request
from refresh import Refresh

#adding buttons next commit

class SpotifyBox:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.playlist_id = ""
        self.tracks = ""
        self.end_playlist_id = ""
        self.current_song_id = ""
        self.current_progress = ""
        self.volume_percent = 100
        self.position_ms = 0
        self.discover_weekly = discover_weekly
        #how do i save headers into variables? i can't replace headers with this
        self.headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer {}".format(self.spotify_token),
        }
    
    def call_refresh(self):
        print("Refreshing token")
        refreshCaller = Refresh()
        self.spotify_token = refreshCaller.refresh()
        
    def find_songs(self, playlist_id): #scanns a playlist, needs playlist id
        print("Finding songs in playlist...")
        # Loop through playlist tracks, add them to list
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)
        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                        "Authorization": "Bearer {}".format(self.spotify_token)})
        response_json = response.json()
        print(response)
        
        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"]+ ",") #comma seperated list of tracks is easier to work with
            #goes to items branch, then tracks and then uri
        self.tracks = self.tracks[:-1] #slices the last comma because nothing comes after it
        print(self.tracks)     

    def create_playlist(self):#creates playlist with todays date, may change to be customizable
        # Create a new playlist standart format is date
        print("Trying to create playlist...")
        today = date.today()
        todayFormatted = today.strftime("%d/%m/%Y")

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)

        request_body = json.dumps({
            "name": todayFormatted + " discover weekly", 
            "description": "Discover weekly rescued by my python script",
            "public": True
        })

        response = requests.post(query, data=request_body, headers={ #posts query, sends body specifications and headers
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        })
        response_json = response.json()
        self.end_playlist_id = response_json["id"] #return id because we need it in add_to_playlist

    def add_to_playlist(self, end_playlist_id): #needs a end playlist id to fill with songs from self.tracks
        print("Adding songs to given playlist...")
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            end_playlist_id,
            self.tracks
        )
        #/tracks?uris= is optional for lists seperated by a comma
        
        response = requests.post(query, headers={"Content-Type": "application/json",
                                                 "Authorization": "Bearer {}".format(self.spotify_token)})
        print(response.json)

    def copy_discover_weekly(self):
        print("coping your discover weekly playlist...")
        a.call_refresh()
        a.find_songs(self.discover_weekly)
        a.create_playlist()
        a.add_to_playlist(self.end_playlist_id)

    def find_current_song(self):
        print("Finding currently playing song...")
        query = "https://api.spotify.com/v1/me/player/currently-playing"
        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})
        response_json = response.json()
        self.current_progress = response_json["progress_ms"]
        self.current_song_id = response_json["item"]["id"]
    
    def like_song(self):
        print("adding current song to Liked Songs...")
        a.find_current_song()
        query = "https://api.spotify.com/v1/me/tracks?ids={}".format(
            self.current_song_id)
        response = requests.put(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})

# may rewrite this volume section    
# if volume % is not a 10 step it stops at the highest number 
# before 100 ex. 81%, 91%, 101, but stops at 91 since player only goes
# upto 100% same goes for negative numbers

    def bass_boost(self):
        print("Volume set to 100")
        query = "https://api.spotify.com/v1/me/player/volume?volume_percent={}".format(
            self.volume_percent)
        response = requests.put(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})
        
    def get_volume(self):
        query = "https://api.spotify.com/v1/me/player"
        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})
        response_json = response.json()
        self.volume_percent = response_json["device"]["volume_percent"]
        return self.volume_percent
        
    def volume_down(self):
        
            a.get_volume()
            self.volume_percent -=10 
            query = "https://api.spotify.com/v1/me/player/volume?volume_percent={}".format(
            self.volume_percent)
            print(self.volume_percent)
            response = requests.put(query,
                                headers={"Content-Type": "application/json",
                                        "Authorization": "Bearer {}".format(self.spotify_token)})
                  
    def volume_up(self):
        a.get_volume()
        self.volume_percent +=10 
        query = "https://api.spotify.com/v1/me/player/volume?volume_percent={}".format(
        self.volume_percent)
        print(self.volume_percent)
        response = requests.put(query,
                            headers={"Content-Type": "application/json",
                                        "Authorization": "Bearer {}".format(self.spotify_token)})
    
    def resume(self):
        #spotify doesn't have a play/resume query so this works just as well
        query = "https://api.spotify.com/v1/me/player/play"
        response = requests.put(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})
        if response.status_code > 204 :
            query = "https://api.spotify.com/v1/me/player/pause"
            response = requests.put(query,headers={"Content-Type": "application/json","Authorization": "Bearer {}".format(self.spotify_token)})
    
    def skip_song(self):
            query = "https://api.spotify.com/v1/me/player/next"
            response = requests.post(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})           

    def reset_song(self):
        #On Spotify you can repeat the song if it has not passed the 3 seconds mark by pressing 'previous track' 
            query = "https://api.spotify.com/v1/me/player/seek?position_ms={}".format(self.position_ms)
            response = requests.put(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.spotify_token)})
            print("reseting the song...")
   
    def previous_song(self):
                query = "https://api.spotify.com/v1/me/player/previous"
                response = requests.post(query,
                                    headers={"Content-Type": "application/json",
                                             "Authorization": "Bearer {}".format(self.spotify_token)})
                print("playing previous song...")
    
    def reset_by_previous(self):
        #does the same as pressing the prevoius button on spotify app (QoL)
        a.find_current_song()
        if self.current_progress > 3000:
            a.reset_song()
        else:
            a.previous_song()
            
a = SpotifyBox()
a.call_refresh()
a.volume_up()


