from flask import Blueprint, redirect, request, jsonify, render_template
from .spotify_auth import SpotifyAuth
import requests
from .storage import storage


# Landing page of the app.
root = Blueprint("root", "root", url_prefix="/")


@root.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@root.route("/")
def index():
    return render_template("index.html")


# Spotify Authorization.
auth = Blueprint("auth", "auth", url_prefix="/auth")


@auth.route("/")
def get_user():
    response = SpotifyAuth().getUser()
    return redirect(response)


@auth.route("/callback")
def callback():
    code = request.values["code"]
    tokens = SpotifyAuth().getUserToken(code)
    """"get data of new releases and store them"""
    token = tokens.get('access_token')
    headers = {'content-type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer ' + token
               }
    r = requests.get(
        "https://api.spotify.com/v1/browse/new-releases", headers=headers)
    storage.actualize_new_releases(r)

    return jsonify(tokens)


# API
api = Blueprint("api", "api", url_prefix="/api")

# Add your "artists" route here.
@api.route('/artist')
def send_artists_data():
    """get data of a all artists"""
    return jsonify(storage.get_new_releases())


@api.route('/artist/<name>')
def send_artist_data(name):
    """get data of a specific artist"""
    tracks = []
    for elem in storage.get_new_releases():
        if name in elem['artists']:
            tracks.append(elem)
    if len(tracks) == 0:
        return 'this artist does not exist or doesn\'t have any new releases'
    return jsonify(tracks)
