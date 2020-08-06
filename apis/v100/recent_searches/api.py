from apis.v100.recent_searches.validation import recent_searches_parser
from common.base_resources import BasePostResource
from mongo_models.recent_searches import RecentSearch


class RecentSearches(BasePostResource):
    end_point = 'recent_searches'
    version = 100
    request_parser = recent_searches_parser

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.user_id = self.request_args.get('user_id')
        self.is_delivery = self.request_args.get('is_delivery')

    def get_recent_searches(self):
        """
        Gets recent searches
        """
        self.recent_searches = RecentSearch.get_recent_searches(self.user_id, is_delivery=self.is_delivery)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'recent_searches': self.recent_searches
            }
        }

    def process_request(self):
        """
        process request
        """
        self.populate_request_arguments()
        self.get_recent_searches()
        self.prepare_response()
