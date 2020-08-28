from flask_restful import Api

from common.constants import API_BASE_END_POINT


class BaseRouting(object):
    api_version = None

    def __init__(self, app):
        self.routing_collection = {}
        self.api = Api(app)

    def set_routing_collection(self):
        pass

    def set_routing(self):
        for api_endpoint, api_class in self.routing_collection.items():
            api_path = '{base_url}/v{version}/{endpoint}'.format(
                base_url=API_BASE_END_POINT, version=self.api_version, endpoint=api_endpoint
            )
            self.api.add_resource(api_class, api_path)

    def map_routing(self):
        self.set_routing_collection()
        self.set_routing()
