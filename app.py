from backend import test 
import cred
from  flask import Flask, request, render_template, url_for, flash, redirect

backend = Flask(__name__)

@backend.route('/', methods=('GET', 'POST'))
def index():
    
    if request.method == 'POST':
        artist = request.form['artist']
        playlistName = request.form['playlist-name']
        playlistDescription = request.form['description']

        if not artist:
            flash('Artist is required!')
        else:
            test(artist_requested=artist, playlist_name=playlistName, playlist_description=playlistDescription)
            return redirect(url_for('index'))
    
    return render_template('index.html')