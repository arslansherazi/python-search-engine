from flask import Flask
from flask_restful import Api

from apis.search.api import Search

# flask app
app = Flask(__name__)

# routing
apis = Api(app)
apis.add_resource(Search, '/ofd_search/v100/search')
