from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

from apis.v100.auto_suggest.validation import auto_suggest_parser
from common.base_resources import BasePostResource
from common.constants import ES_IP


class AutoSuggest(BasePostResource):
    end_point = 'auto_suggest'
    version = 100
    request_parser = auto_suggest_parser

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.query = self.request_args.get('query')

    def initialize_class_arguments(self):
        """
        Initialize class arguments
        """
        self.es = Elasticsearch([ES_IP])
        self.es_client = IndicesClient(self.es)
        self.index = 'menu_items'
        self.menu_items_data = []

    def get_suggestions_data(self):
        """
        Gets suggestions data
        """
        es_query = {
            'suggest': {
                'name_suggest_fuzzy': {
                    'prefix': self.query.lower(),
                    'completion': {
                        'field': 'name.completion',
                        'fuzzy': {
                            'fuzziness': 1
                        }
                    }
                }
            },
            'aggs': {
                'unique_names': {
                    'terms': {
                        'field': 'name.keyword',
                        'size': 1000
                    }
                }
            },
            '_source': ['name']  # used to select specific fields
        }
        self.es_response = self.es.search(timeout='3s', index=self.index, doc_type='doc', body=es_query)

    def process_es_response(self):
        """
        Process elastic search response
        """
        duplicate_suggestions_check = []
        suggestions_count_hash = {}
        suggestions_count = self.es_response.get('aggregations', {}).get('unique_names', {}).get('buckets', [])
        for suggestion_count in suggestions_count:
            suggestions_count_hash[suggestion_count.get('key')] = suggestion_count.get('doc_count')
        suggestions = self.es_response.get('suggest', {}).get('name_suggest_fuzzy')[0].get('options')
        for suggestion in suggestions:
            suggestion_name = suggestion.get('text', '')
            if suggestion_name not in duplicate_suggestions_check:
                menu_item_data = {
                    'name': suggestion.get('text', ''),
                    'count': suggestions_count_hash.get(suggestion_name)
                }
                self.menu_items_data.append(menu_item_data)
                duplicate_suggestions_check.append(suggestion_name)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'menu_items_data': self.menu_items_data
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_arguments()
        self.get_suggestions_data()
        self.process_es_response()
        self.prepare_response()
