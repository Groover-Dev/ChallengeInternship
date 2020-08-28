# Groover Backend Challenge

Your goal is to create an app using the [spotify web api](https://developer.spotify.com/documentation/web-api/).
We have already provided you with a flask project able to authenticate to spotify.
Your job is to add two new features:
 - A way to fetch data from spotify's new releases API and persist it somewhere. For example using [TinyDB](https://tinydb.readthedocs.io/en/stable/intro.html)
 - A route : `/api/artists/` returning a JSON containing informations about artists that have released new tracks recently, from your local copy of today's spotify's new releases.

# How to run this sample

- move to this directory
- setup a new virtualenv and activate it
- install the requirements in requirements.txt
- run:
```
FLASK_ENV=development \
  CLIENT_ID=e18d6952d6854b6c9ab1a161a013e6e3 \
  CLIENT_SECRET=7555b89676e34ac69a1c32c49b3dfef6 \
  flask run
```


- go to http://localhost:5000/
- You can now log to spotify through the app.

# Project Structure

The initialisation of the app is done in **./challengegroover/__init__.py**.

The spotify auth is provided by us: (follows [spotify web api](https://developer.spotify.com/documentation/web-api/).): it is located in **./challengegroover/spotify_auth.py**. The flow ends with a call to `/auth/callback/` which will give you the necessary access tokens.

New routes can be added in **./challengegroover/routes.py**

Feel free to move and re-organise as you please, we expect a well organised and clean code.

# Tech Specifications

- Be smart in your token usage (no unnecessary refreshes)
- Don't request spotify artists at each request we send you
- The way you store the artists is going to be important. 
- As stated above, to test your server we will GET `/api/artists/` and we expect a nicely organized payload of artists.
- All stability, performance, efficiency adds-up are highly recommended.
- not mandatory but if you want to make a UI, go ahead and complete folder ui/. 

# modification explication

- adding storage using tinydb
- adding a 404 error handler
- adding a api/artist route 
- adding a api/artist/<artist_name> route