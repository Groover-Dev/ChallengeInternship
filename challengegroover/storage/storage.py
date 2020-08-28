from tinydb import TinyDB, Query
import os

if not os.path.isfile('./db.json'):
    tmp = open('./db.json', "w+")
    tmp.close()
db = TinyDB('./db.json')

"""store data about the tracks (could have a lot more aobut tacks and artists)"""
def actualize_new_releases(artists):
    db.drop_table('artists')
    table = db.table('artists')
    for elem in artists.json().get('albums')['items']:
        tmpartist = []
        for artist in elem.get('artists'):
            tmpartist.append(artist['name'])
        table.insert({
            'name':elem['name'],
            'artists': tmpartist,
            'release_date':elem['release_date'],
        })

"""send data stored previously"""
def get_new_releases():
    table = db.table('artists')
    return table.all()
