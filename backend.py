# -*- coding: utf-8 -*-
# from flask import Flask, render_template
from http import client
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

import os

client_ID = os.getenv("client_ID")
client_SECRET = os.getenv("client_SECRET")
redirect_url = os.getenv("redirect_url")
scopes = ["user-library-read", "playlist-modify-public"]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_ID, client_secret=client_SECRET, redirect_uri=redirect_url, scope=scopes))



def standarize_name(name):
    
    name = name.lower().replace(" ", "")
    
    return name

def get_saved_tracks(sp, artist_requested):
    matched_tracks = dict()

    saved_tracks = sp.current_user_saved_tracks(50)
    off = 0
    start = 0
    
    while saved_tracks['next'] != None:
        
        if start != 0:
            saved_tracks = sp.current_user_saved_tracks(50,off)
            
        for idx, item in enumerate(saved_tracks['items']):
            artists = set()
            start += 1
            track = item['track']
            
            for artist in track['artists']:
                
                artist_standard_name = standarize_name(artist['name'])
                
                artists.add(artist_standard_name)
            
            # artist = track['artists'][0]['name']
                
            if standarize_name(artist_requested) in artists:
                
                matched_tracks[track['name']] = track['uri']

        off += 50
        # time.sleep(1)
        
    return matched_tracks 
        
def create_playlist(sp, playlist_name, playlist_description):
    user = sp.current_user()
    user_id = user['id']
    playlist = dict()

    # playlist_name = "Drake 2"
    # playlist_description = "Testing COMP4999 Project"

    new_playlist = sp.user_playlist_create(user_id, playlist_name, public=True, collaborative=False, description=playlist_description)
    playlist['id'] = new_playlist['id']
    playlist['url'] = new_playlist['external_urls']['spotify']
    return playlist

def add_tracks_playlist(sp, playlist_id, items):

    sp.playlist_add_items(playlist_id, items)
      
def generate_full_playlist(artist_requested, playlist_name, playlist_description):
    
    # artist_requested = input("Please enter the name the artist as it appears on Spotify: ")
    # playlist_name = input("What would you like your new playlist to be called? ")
    # playlist_description = input("Describe your playlist: ")
    
    try:
        tracks = get_saved_tracks(sp, artist_requested)
        playlist = create_playlist(sp, playlist_name, playlist_description)
        add_tracks_playlist(sp, playlist['id'], tracks.values())
        
        return playlist['id']
    except:
        return None
    
