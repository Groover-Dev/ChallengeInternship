import requests
import datetime
from .spotify_auth import SpotifyAuth
from .models import db, Album, Artist, Image, JoinAlbumArtist, Tokens
from .utilities import AlchemyJsonEncoder
from flask import  jsonify, make_response, abort
from flask_sqlalchemy import SQLAlchemy
import json

class SpotifyAPI(object):
    access_token = None
    refresh_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True

    #accessing and checking token from local copy, checking expiration before refresh
    def get_access_token(self):
        tokens = Tokens.query.first()
        token = tokens.access_token
        now = datetime.datetime.now()
        expires = tokens.access_token_expires
        if expires < now:
            spotify_auth = SpotifyAuth()
            result = spotify_auth.refreshAuth(tokens.refresh_token)
            data = result.json()
            now = datetime.datetime.now()
            db.session.delete(tokens)
            self.save_tokens(data)
            return self.get_access_token()
        elif token == None:
            abort(make_response(jsonify(message="Token not found, please authenticate"), 400)) 
        return token

    #headers helper
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            'content-type': 'application/json',
            'Accept': 'application/json',
            "Authorization": f"Bearer {access_token}"
        }
        return headers
    
    #saving access credentials 
    def save_tokens(self,tokens):

        try:
            token_model = Tokens()
            token_model.json_to_model(tokens)
            print(token_model.access_token)
            db.session.add(token_model)
            db.session.commit()
        except:
            db.session.rollback()
            abort(500,"There was a token issue")
            raise
        finally:
            db.session.close()

    # getting new releases from spotify API
    def browse_new_releases(self, version='v1'):

        endpoint = f"https://api.spotify.com/{version}/browse/new-releases"
        # loop until reaching the limit - the total releases available
        while endpoint != None: 
            headers = self.get_resource_header()
            print(endpoint)
            print(headers)
            r = requests.get(endpoint, headers=headers)
            if r.status_code not in range(200, 299):
                return {}
            response = r.json()
            endpoint = response['albums']['next']
            for item in response['albums']['items']:
                album_obj = Album()
                album_obj.json_to_model(item)
                album_exists = db.session.query(Album.album_id).filter_by(spotify_id=album_obj.spotify_id).scalar() is not None
                
                #check if album already exists in local copy
                if album_exists == False:
                    artists = []
                    for artist in item['artists']:
                        artist_model = Artist()
                        artist_model.json_to_model(artist)
                        artists.append(artist_model)
                        try:
                            db.session.add(album_obj)
                            db.session.commit()
                            #print("added new album to database")
                            for artist_obj in artists:
                                #check if artist already exists in local copy - dublicates handling
                                artist_exists = db.session.query(Artist.artist_id).filter_by(spotify_id=artist_obj.spotify_id).scalar() is not None
                                if not artist_exists: 
                                    db.session.add(artist_obj)
                                    db.session.commit()
                                    #print("added new artist to database")
                                #join album - artist
                                join_artist_album = JoinAlbumArtist(album_id = album_obj.album_id, artist_id = artist_obj.artist_id)
                                db.session.add(join_artist_album)
                                db.session.commit()
                                #print("added new join artist-album to database")
                        except:
                            db.session.rollback()
                            raise
                            abort(500,"There was an issue adding to local copy")
                        finally:
                            db.session.close()

        return r.json()
