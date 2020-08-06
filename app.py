from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restful import Api

from apis.v100.auto_suggest.api import AutoSuggest
from apis.v100.recent_searches.api import RecentSearches
from apis.v100.search.api import Search

# flask app
app = Flask(__name__)

# mongo db configurations
app.config['MONGODB_SETTINGS'] = {
    'db': 'ofd_db',
    'host': 'localhost',
    'port': 27017
}
mongo_db = MongoEngine(app)

# routing
apis = Api(app)
apis.add_resource(Search, '/ofd_search/v100/search')
apis.add_resource(AutoSuggest, '/ofd_search/v100/auto_suggest')
apis.add_resource(RecentSearches, '/ofd_search/v100/recent_searches')
