from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

from wrapper.py_sql import PySQL

es_ip = '127.0.0.1:9200'
db_host = '127.0.0.1'
db_port = '3306'
db_user = 'root'
db_password = 'rootroot'
db_name = 'ofd_db'

es = Elasticsearch([es_ip])
client = IndicesClient(es)


def get_menu_items_data():
    """
    gets menu items data

    :return menu items data
    :rtype list
    """
    py_sql = PySQL(db_host, db_port, db_name, db_user, db_password)
    py_sql.query = '''
    SELECT mi.id, mi.name, mi.price, mi.unit, mi.discount, mi.image_url, mi.rating, mi.rating_count, mi.is_active,
    mi.quantity, i.id AS ingredient_id, i.name AS ingredient_name, i.quantity AS ingredient_quantity, 
    i.unit AS ingredient_unit, m.id AS merchant_id, m.name AS merchant_name, m.latitude, m.longitude, 
    apis_user.profile_image_url AS merchant_image_url, mi.menu_id, m.address, m.contact_no, m.is_takeaway_enabled, 
    m.is_delivery_enabled
    FROM menu_item mi
    INNER JOIN ingredient i ON mi.id = i.menu_item_id
    INNER JOIN merchant m ON mi.merchant_id = m.id
    INNER JOIN apis_user ON m.user_id = apis_user.id
    '''
    menu_items = py_sql.fetch_all()
    return menu_items


def put_menu_items_data_into_es_indices(menu_items):
    """
    Puts menu items data into elastic search indices

    :param list menu_items: menu items
    """
    menu_items_data = {}
    for menu_item in menu_items:
        menu_item_id = menu_item.get('id')
        menu_item_ingredient = {
            'id': menu_item.get('ingredient_id'),
            'name': menu_item.get('ingredient_name'),
            'quantity': menu_item.get('ingredient_quantity'),
            'unit': menu_item.get('ingredient_unit'),
        }
        if menu_item_id not in menu_items_data:
            menu_items_data[menu_item_id] = {
                'id': menu_item_id,
                'name': menu_item.get('name'),
                'price': menu_item.get('price'),
                'unit': menu_item.get('unit'),
                'quantity': menu_item.get('quantity'),
                'discount': menu_item.get('discount'),
                'image_url': menu_item.get('image_url'),
                'rating': menu_item.get('rating'),
                'rating_count': menu_item.get('rating_count'),
                'ingredients': [],
                'is_favourite': False,
                'merchant_info': {
                    'id': menu_item.get('merchant_id'),
                    'name': menu_item.get('merchant_name'),
                    'image_url': menu_item.get('merchant_image_url'),
                    'latitude': menu_item.get('latitude'),
                    'longitude': menu_item.get('longitude'),
                    'address': menu_item.get('address'),
                    'contact_no': menu_item.get('contact_no'),
                    'is_takeaway': bool(menu_item.get('is_takeaway_enabled')),
                    'is_delivery': bool(menu_item.get('is_delivery_enabled'))
                },
                'menu_id': menu_item.get('menu_id')
            }
        menu_items_data[menu_item_id]['ingredients'].append(menu_item_ingredient)

    for menu_item_id, menu_item_data in menu_items_data.items():
        if menu_item_data.get('merchant_info', {}).get('is_takeaway', False):
            es.index(index='takeaway_menu_items', doc_type='doc', id=menu_item_id, body=menu_item_data)
        if menu_item_data.get('merchant_info', {}).get('is_delivery', False):
            es.index(index='delivery_menu_items', doc_type='doc', id=menu_item_id, body=menu_item_data)


if __name__ == '__main__':
    menu_items = get_menu_items_data()
    put_menu_items_data_into_es_indices(menu_items)
