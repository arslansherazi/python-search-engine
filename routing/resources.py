from routing.routing_v100 import RoutingV100


# routing
def api_urls():
    RoutingV100().map_routing()


api_urls()
