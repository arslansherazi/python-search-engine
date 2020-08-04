from flask import Flask
from flask_restful import Api

from apis.v100.auto_suggest.api import AutoSuggest
from apis.v100.search.api import Search

# flask app
app = Flask(__name__)

# routing
apis = Api(app)
apis.add_resource(Search, '/ofd_search/v100/search')
apis.add_resource(AutoSuggest, '/ofd_search/v100/auto_suggest')
