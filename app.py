import os
from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.bootstrap import Bootstrap
from flask.ext.mysqldb import MySQL
import urllib
import string
import simplejson as json


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')


manager = Manager(app)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


#routes
@app.route('/')
def home():
    wiki_data = get_wiki()
    for key, value in wiki_data.iteritems():
        title = clean_title(value['title'])
        print title
    giffy_data = get_giffy(title)
    print giffy_data
    return render_template('index.html')

#database models
class Image(db.Model):
    __tablename__ ='images'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(64), unique=True)
    datetime = db.Column(db.DateTime, unique=True)
    
    def __init__(self, url):
        self.url = url
    
    def __repr__(self):
        return '<Image %r>' % self.url
        
#helper methods
#gets a json object from a URL
def get_json(URL):
    fileObj = urllib.urlopen(URL)
    parsed_json = json.load(fileObj)
    return parsed_json

#gets a random Wikipedia page
def get_wiki():
    url = app.config['WIKI_URL']
    json = get_json(url)
    data = json['query']['pages']
    return data

def clean_title(title):
    title = title.replace("-", " ")
    printable = set(string.printable)
    title = filter(lambda x: x in printable, title) #strip non-ASCII characters
    return title

#gets a giffy URL from API
def get_giffy(title):
     data = {}
     url = app.config['GIFFY_URL']
     title = title.replace(" ", "+")
     url = url + title
     json = get_json(url)
     raw_data = dict(json['data'])
     if raw_data:
         data['image_url'] = raw_data['fixed_width_downsampled_url'].encode('ascii')
     return data
         

if __name__ == '__main__':
    manager.run()