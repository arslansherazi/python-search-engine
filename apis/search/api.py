from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

from apis.search.validation import search_parser
from common.base_resources import BasePostResource
from common.constants import ES_IP, ITEMS_LISTING_PAGE_LIMIT


class Search(BasePostResource):
    end_point = 'search'
    version = 100
    request_parser = search_parser

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.offset = self.request_args.get('offset')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.es = Elasticsearch([ES_IP])
        self.es_client = IndicesClient(self.es)
        self.index = 'menu_items'
        self.menu_items = []

    def get_menu_items_data(self):
        """
        Gets menu items data
        """
        self.es_query = {
            'size': ITEMS_LISTING_PAGE_LIMIT,
            'from': self.offset,
            'query': {
                'match_all': {}
            }
        }
        self.response = self.es.search(timeout='3s', index=self.index, doc_type='doc', body=self.es_query)

    def process_es_response(self):
        """
        Processes elastic search response
        """
        es_menu_items = self.response.get('hits', {}).get('hits', [])
        for es_menu_item in es_menu_items:
            menu_item = es_menu_item.get('_source')
            self.menu_items.append(menu_item)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': self.menu_items
        }

    def process_request(self):
        """
        process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.get_menu_items_data()
        self.process_es_response()
        self.prepare_response()
