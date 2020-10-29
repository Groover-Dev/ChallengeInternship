from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from datetime import datetime,timedelta

db = SQLAlchemy(session_options={'expire_on_commit': False})

class Abstract(db.Model):
    __abstract__ = True

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Album(Abstract):
    __tablename__ = 'album'
    
    album_id =  db.Column(db.Integer, primary_key=True)
    spotify_id =  db.Column(db.String(200), nullable = False, unique=True)
    album_type = db.Column(db.String(200), nullable=False)
    #artists = db.relationship('Artist',  lazy=True, secondary = "join_album_artist")
    available_markets = db.Column(db.String)
    external_url_key = db.Column(db.String(200))
    external_url_value = db.Column(db.String(200))
    href =  db.Column(db.String(200))
    images = db.relationship('Image', backref='album', lazy=True, passive_deletes = True, cascade='delete,all')
    name = db.Column(db.String(200))
    a_type = db.Column(db.String(200))
    uri = db.Column(db.String(200))
    release_date = db.Column(db.DateTime)


    #convert spotify json to db model
    def json_to_model(self,json_obj):
        self.spotify_id = json_obj['id']
        self.album_type = json_obj['album_type']
        self.available_markets = ''.join(str(m) for m in json_obj['available_markets'])
        self.external_url_key = list(json_obj['external_urls'].keys()).__getitem__(0)
        self.external_url_value = json_obj['external_urls'][self.external_url_key]
        self.href = json_obj['href']
        self.name = json_obj['name']
        self.a_type = json_obj['type']
        self.uri = json_obj['uri']
        self.release_date = datetime.strptime(json_obj['release_date'], "%Y-%m-%d")
        # artists = []
        # for artist in json_obj['artists']:
        #     artist_model = Artist()
        #     artist_model.json_to_model(artist)
        #     artists.append(artist_model)
        # self.artists = artists
        images = []
        for image in json_obj['images']:
            image_model = Image()
            image_model.json_to_model(image)
            images.append(image_model)
        self.images = images


    #track element creation
    def __repr__(self):
        return '<Album %r>' %self.album_id


class Artist(Abstract):
    __tablename__ = 'artist'

    artist_id =  db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(200), nullable = False, unique = True)
    external_url_key = db.Column(db.String(200))
    external_url_value = db.Column(db.String(200))
    href =  db.Column(db.String(200))
    name = db.Column(db.String(200))
    a_type = db.Column(db.String(200))
    uri = db.Column(db.String(200))
    #album_id = db.Column(db.Integer, db.ForeignKey('album.id'),nullable = False)

    #convert spotify json to db model
    def json_to_model(self,json_obj):
        self.spotify_id = json_obj['id']
        self.external_url_key = list(json_obj['external_urls'].keys()).__getitem__(0)
        self.external_url_value = json_obj['external_urls'][self.external_url_key]
        self.href = json_obj['href']
        self.name = json_obj['name']
        self.a_type = json_obj['type']
        self.uri = json_obj['uri']

    #track element creation
    def __repr__(self):
        return '<Artist %r>' %self.artist_id

class JoinAlbumArtist(Abstract):
    __tablename__ = "join_album_artist"

    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.album_id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.artist_id'))

    #track element creation
    def __repr__(self):
        return '<Join %r>' %self.id


class Image(Abstract):
    __tablename__ = 'image'

    id =  db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Integer)
    width = db.Column(db.Integer)
    url = db.Column(db.String(200), nullable = False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.album_id'), nullable = False)

    #convert spotify json to db model
    def json_to_model(self,json_obj):
        self.height = json_obj['height']
        self.width = json_obj['width']
        self.url = json_obj['url']

    #track element creation
    def __repr__(self):
        return '<Image %r>' %self.id


#model for token usage
class Tokens(Abstract):

    __tablename__ = 'tokens'

    id =  db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(200), nullable = False)
    refresh_token = db.Column(db.String(200), nullable = False)
    access_token_expires = db.Column(db.DateTime, nullable = False) 

    #convert spotify json to db model
    def json_to_model(self,json_obj):
        self.access_token = json_obj['access_token']
        self.refresh_token = json_obj['refresh_token']
        self.access_token_expires = datetime.now() + timedelta(seconds=json_obj['expires_in'])

    #track element creation
    def __repr__(self):
        return '<Tokens %r>' %self.id