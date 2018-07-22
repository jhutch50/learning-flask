#Import SQLAlchemy class from Flask-SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

import geocoder
from urllib.request import urlopen
from urllib.request import urljoin
import json

#db will be the usable instance of the SQLAlchemy class
db = SQLAlchemy()

#Create a python class to model the user's attributes
#These are the same as the columns in the db table
class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))

        
    #Here is a constructor to set each class attribute
    #Note that the constructor has firstname and last name with .title(), this allows
    #for the firstname and lastname to have the first letter capitalized,
    #it saves the email in lowercase so it can match regardless of how the user types
    # and right away we encrypt the user's password using the set_password function
    #we call from what we create below and storing that into pwdhash
    #generate_password_hash comes from one of Flask's libraries, werkzeug

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

class Place(object):
  def meters_to_walking_time(self, meters):
    # 80 meters is one minute walking time
    return int(meters / 80)  

  def wiki_path(self, slug):
    return urljoin("http://en.wikipedia.org/wiki/", slug.replace(' ', '_'))
  
  def address_to_latlng(self, address):
    g = geocoder.google(address)
    return (g.lat, g.lng)

  def query(self, address):
    lat, lng = self.address_to_latlng(address)
    
    query_url = 'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord={0}%7C{1}&gslimit=20&format=json'.format(lat, lng)
    g = urlopen(query_url)
    results = g.read()
    g.close()

    data = json.loads(results)
    
    places = []
    for place in data['query']['geosearch']:
      name = place['title']
      meters = place['dist']
      lat = place['lat']
      lng = place['lon']

      wiki_url = self.wiki_path(name)
      walking_time = self.meters_to_walking_time(meters)

      d = {
        'name': name,
        'url': wiki_url,
        'time': walking_time,
        'lat': lat,
        'lng': lng
      }

      places.append(d)

    return places