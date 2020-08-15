from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

from apis.v100.search.validation import search_parser
from common.base_resources import BasePostResource
from common.common_helpers import CommonHelpers
from common.constants import ES_IP, ITEMS_LISTING_PAGE_LIMIT
from mongo_models.recent_searches import RecentSearch
from repositories.menu_items_repo import MenuItemsRepository


class Search(BasePostResource):
    end_point = 'search'
    version = 100
    request_parser = search_parser

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.query = self.request_args.get('query')
        self.offset = self.request_args.get('offset')
        self.user_id = self.request_args.get('user_id')
        self.latitude = self.request_args.get('latitude')
        self.longitude = self.request_args.get('longitude')
        self.is_takeaway = bool(self.request_args.get('is_takeaway'))
        self.is_delivery = bool(self.request_args.get('is_delivery'))
        self.is_auto_suggest_items = bool(self.request_args.get('is_auto_suggest_items'))

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
        if self.is_auto_suggest_items:
            self.es_query = {
                'size': ITEMS_LISTING_PAGE_LIMIT,
                'from': self.offset,
                'query': {
                    'match': {
                        'name': {
                            'query': self.query.lower(),
                            'operator': 'and'
                        }
                    }
                }
            }
        else:
            self.es_query = {
                'size': ITEMS_LISTING_PAGE_LIMIT,
                'from': self.offset,
                'query': {
                    'match': {
                        'name': {
                            'query': self.query.lower(),  # query text will be converted into tokens
                            'fuzziness': 'AUTO',
                            'operator': 'or'  # returns documents which includes any token
                        }
                    }
                }
            }
        self.es_response = self.es.search(timeout='3s', index=self.index, doc_type='doc', body=self.es_query)

    def process_es_response(self):
        """
        Processes elastic search response
        """
        favourite_menu_items_ids = MenuItemsRepository.get_favourite_menu_items_ids(self.user_id)
        es_menu_items = self.es_response.get('hits', {}).get('hits', [])
        for es_menu_item in es_menu_items:
            menu_item = es_menu_item.get('_source')
            if menu_item.get('id') in favourite_menu_items_ids:
                menu_item['is_favourite'] = True
            self.menu_items.append(menu_item)
        self.menu_items = MenuItemsRepository.calculate_distance_btw_buyer_and_merchant(
            self.latitude, self.longitude, self.menu_items, self.is_takeaway, self.is_delivery
        )
        if self.is_takeaway:
            self.menu_items = CommonHelpers.sort_list_data(self.menu_items, key='distance', descending=True)
        else:
            self.menu_items = CommonHelpers.sort_list_data(self.menu_items, key='delivery_time', descending=True)

    def save_recent_search(self):
        """
        Saves recent search. It also verifies that either search query is already present in recent searches of user.
        """
        is_search_query_already_present = RecentSearch.verify_search_query(
            self.query, self.user_id, is_delivery=self.is_delivery
        )
        if not is_search_query_already_present:
            RecentSearch.save_search_query(self.query, self.user_id, is_delivery=self.is_delivery)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'items': self.menu_items
            }
        }

    def process_request(self):
        """
        process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.get_menu_items_data()
        self.process_es_response()
        self.save_recent_search()
        self.prepare_response()
