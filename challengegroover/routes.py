from flask import Blueprint, redirect, request, jsonify, render_template, abort, make_response
from .spotify_auth import SpotifyAuth
from .spotify_api import SpotifyAPI
from .utilities import AlchemyJsonEncoder
from .models import db, Album, Artist, Image, JoinAlbumArtist
import json

# Landing page of the app.
root = Blueprint("root", "root", url_prefix="/")




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
    db.drop_all()
    db.create_all()
    code = request.values["code"]
    tokens = SpotifyAuth().getUserToken(code)
    spotify_api = SpotifyAPI()
    spotify_api.save_tokens(tokens)
    new_releases = spotify_api.browse_new_releases()
    return jsonify(tokens)


# API
api = Blueprint("api", "api", url_prefix="/api")

# Add your "artists" route here.
# Get artists - from local copy
@api.route("/artists")
def load_artists():
    artists = Artist.query.all()
    return json.dumps(artists,cls=AlchemyJsonEncoder)

# Get recent albums - from local copy
@api.route("/recent-albums")
def load_recent_albums():
    albums = Album.query.all()
    return json.dumps(albums,cls=AlchemyJsonEncoder)

# Search for artist by name - from local copy
@api.route("/artist/<artist_name>")
def get_artist(artist_name):
    artist = Artist.query.filter_by(name=artist_name).first()
    if artist == None:
        abort(make_response(jsonify(message="Artist not found in local copy"), 404))
    return json.dumps(artist,cls=AlchemyJsonEncoder)


@api.route("/test-refresh")
def test_refresh():
    spotify_api = SpotifyAPI()
    new_releases = spotify_api.browse_new_releases()
    return "done"
