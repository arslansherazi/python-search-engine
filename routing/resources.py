from flask import current_app

from routing.routing_v100 import RoutingV100


# routing
def api_urls():
    RoutingV100(current_app).map_routing()
