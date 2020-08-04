from apis.v100.search import Search
from routing.base_routing import BaseRouting


class RoutingV100(BaseRouting):
    api_version = '100'

    def set_routing_collection(self):
        self.routing_collection = {
            'search': Search
        }
