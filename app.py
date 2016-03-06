import os
from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.bootstrap import Bootstrap
from flask.ext.mysqldb import MySQL


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')


manager = Manager(app)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


#routes
@app.route('/')
def home():
    db.create_all()
    db.drop_all()
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

if __name__ == '__main__':
    manager.run()