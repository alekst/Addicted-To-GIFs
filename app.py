import os
from flask import Flask, render_template
from flask.ext.script import Manager, Server
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.bootstrap import Bootstrap
from flask.ext.mysqldb import MySQL
import urllib
import string
import random
from datetime import datetime
import simplejson as json


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py', silent=True)


manager = Manager(app)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

server = Server(host="0.0.0.0", port=5000)
manager.add_command("runserver", server)

#routes
@app.route('/')
def home():
    giffy = []
    for i in xrange(6):
        giffy_data = get_data()
        giffy.append(giffy_data)  
    print giffy 
    return render_template('index.html', giffy=giffy)

#database model
class Image(db.Model):
    __tablename__ ='images'
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(64), unique=True)
    title = db.Column(db.String(64), unique=True)
    excerpt = db.Column(db.Text(256)),
    created = db.Column(db.TimeStamp, server_default=db.func.now(), onupdate=db.func.now())


#helper methods
def get_data():
    wiki_data = get_wiki()
    print wiki_data
    for key, value in wiki_data.iteritems():
        title = clean_title(value['title'])
        excerpt = value['extract']
    giffy_data = get_giffy(title)
    if not giffy_data:
        row = get_random_row()
        giffy_data['title'] = row.title
        giffy_data['excerpt'] = row.excerpt
        giffy_data['image_url'] = row.image_url      
    else:
        giffy_data['title'] = title
        giffy_data['excerpt'] = excerpt
        record_data(giffy_data)
    return giffy_data

#writes data to the database
def record_data(giffy_record):
    record = Image(**giffy_record)
    print record
    db.session.add(record)
    db.session.commit()
    return
    
def get_random_row():
    #rand = 1
    rand = random.randrange(1, Image.query.count())
    row = Image.query.get(rand)
    return row

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
    exclude = set(string.punctuation)
    title = ''.join(ch for ch in title if ch not in exclude)
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
     raw_data = json['data']
     if raw_data:
         for item in raw_data:
             data['image_url'] = item['images']['fixed_height']['url']
     return data
         

if __name__ == '__main__':
    manager.run()
