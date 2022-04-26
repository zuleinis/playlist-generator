from backend import generate_full_playlist 
import cred
from  flask import Flask, request, render_template, url_for, flash, redirect

app = Flask(__name__)

@app.route('/result')
@app.route('/result/<id>')
def result(id=None):
    return render_template('result.html', id=id)

@app.route('/', methods=('GET', 'POST'))
def index():
    
    if request.method == 'POST':
        artist = request.form['artist']
        playlistName = request.form['playlist-name']
        playlistDescription = request.form['description']

        if not artist:
            flash('Artist is required!')
        else:
            playlist_id = generate_full_playlist(artist_requested=artist, playlist_name=playlistName, playlist_description=playlistDescription)
            return redirect(url_for('result', id=playlist_id))
    
    return render_template('index.html')