DEBUG = True
SQLALCHEMY_ECHO = True

SQLALCHEMY_DATABASE_URI = 'mysql://root:worldpeace@localhost/images'

WIKI_URL = 'https://en.wikipedia.org/w/api.php?action=query&generator=random&grnlimit=1&prop=extracts&exsentences=10&grnnamespace=0&format=json'
GIFFY_URL = 'http://api.giphy.com/v1/gifs/search?api_key=dc6zaTOxFJmzC&limit=1&q='

SQLALCHEMY_TRACK_MODIFICATIONS  = True