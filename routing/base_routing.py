from app import api
from common.constants import API_BASE_END_POINT


class BaseRouting(object):
    routing_collection = {}
    api_version = None

    def set_routing_collection(self):
        pass

    def set_routing(self):
        for api_endpoint, api_class in self.routing_collection.items():
            api_path = 'v{version}/{end_point}'.format(version=self.api_version, end_point=api_endpoint)
            api.add_resource(api_class, API_BASE_END_POINT, endpoint=api_path)

    def map_routing(self):
        self.set_routing_collection()
        self.set_routing()
