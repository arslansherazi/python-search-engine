from flask import Flask
from flask_restful import Api

# flask app configurations
from apis.search.api import Search

app = Flask(__name__)
api = Api(app)

# routing
api.add_resource(Search, '/ofd_search/v100/search')


# run flask app
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8001)
    app.run(debug=True)
