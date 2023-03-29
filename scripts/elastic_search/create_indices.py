from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

es_ip = '127.0.0.1:9200'

es = Elasticsearch([es_ip])
client = IndicesClient(es)

index_meta = {
    'id': {
        'type': 'integer'
    },
    'name': {
        'type': 'text',
        'fields': {
            'completion': {
                'type': 'completion'
            },
            'keyword': {
                'type': 'keyword'
            }
        },
        'analyzer': 'standard'
    },
    'price': {
        'type': 'integer'
    },
    'unit': {
        'type': 'keyword'
    },
    'quantity': {
        'type': 'integer'
    },
    'discount': {
        'type': 'integer'
    },
    'image_url': {
        'type': 'keyword'
    },
    'rating': {
        'type': 'float'
    },
    'rating_count': {
        'type': 'integer'
    },
    'is_favourite': {
        'type': 'boolean'
    },
    'merchant_info': {
        'type': 'nested',
        'properties': {
            'id': {
                'type': 'integer'
            },
            'name': {
                'type': 'keyword'
            },
            'image_url': {
                'type': 'keyword'
            },
            'latitude': {
                'type': 'float'
            },
            'longitude': {
                'type': 'float'
            },
            'address': {
                'type': 'keyword'
            },
            'contact_no': {
                'type': 'keyword'
            },
            'is_takeaway': {
                'type': 'boolean'
            },
            'is_delivery': {
                'type': 'boolean'
            }
        }
    },
    'ingredients': {
        'type': 'nested',
        'properties': {
            'id': {
                'type': 'integer'
            },
            'name': {
                'type': 'keyword'
            },
            'quantity': {
                'type': 'integer'
            },
            'unit': {
                'type': 'keyword'
            }
        }
    },
    'menu_id': {
        'type': 'integer'
    }
}

mappings = {}
mappings.update({
    'doc': {
        'properties': index_meta
    }
})


if __name__ == '__main__':
    indices = ['takeaway_menu_items', 'delivery_menu_items']
    for index in indices:
        client.create(
            index=index,
            body={
                'mappings': mappings,
                'settings': {
                    'number_of_shards': 6,
                    'number_of_replicas': 2
                }
            }
        )
