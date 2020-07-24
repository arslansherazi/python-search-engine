from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

es_ip = '127.0.0.1:9200'

es = Elasticsearch([es_ip])
client = IndicesClient(es)


def delete_index(index_name):
    """
    Deletes index by name if exists

    :param str index_name: index name
    """
    es.indices.delete(index=index_name)


if __name__ == '__main__':
    delete_index('menu_items')
