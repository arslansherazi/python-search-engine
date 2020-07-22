from flask import Flask
from flask_restful import Api

from routing.routing_v100 import RoutingV100

# flask app configurations
app = Flask(__name__)
api = Api(app)

# routing
RoutingV100().map_routing()


# run flask app
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8001)
    app.run(debug=True)
