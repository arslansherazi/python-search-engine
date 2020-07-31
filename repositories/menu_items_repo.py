import geopy.distance

from common.constants import AVERAGE_PREPARATION_TIME, BUFFER_TIME
from wrapper.py_sql import PySQL


class MenuItemsRepository(object):
    @staticmethod
    def get_favourite_menu_items_ids(user_id):
        """
        Gets favourite menu items ids

        :param int user_id: user id
        :rtype list
        :return favourite menu items ids
        """
        py_sql = PySQL(host='127.0.0.1', port=3306, database='ofd_db', user='root', password='rootroot')
        py_sql.query = '''
        SELECT menu_item_id 
        FROM favourite
        WHERE user_id = %s
        '''
        py_sql.params = [user_id]
        menu_items_data = py_sql.fetch_all()
        favourite_menu_items_ids = []
        for menu_item_data in menu_items_data:
            menu_item_id = menu_item_data.get('menu_item_id')
            favourite_menu_items_ids.append(menu_item_id)
        return favourite_menu_items_ids

    @staticmethod
    def calculate_distance_btw_buyer_and_merchant(latitude, longitude, merchants, is_takeaway, is_delivery):
        """
        Calculates distance between buyer and merchant

        :param float latitude: buyer latitude
        :param float longitude: buyer longitude
        :param list merchants: merchants
        :param bool is_takeaway: takeaway flag
        :param bool is_delivery: delivery flag
        :rtype list
        :return: merchants after calculating distance
        """
        for merchant in merchants:
            merchant_latitude = merchant.get('merchant_info').get('latitude')
            merchant_longitude = merchant.get('merchant_info').get('longitude')
            merchant_location = (merchant_latitude, merchant_longitude)
            buyer_location = (latitude, longitude)
            distance = geopy.distance.geodesic(merchant_location, buyer_location).km  # geopy.distance.vincenty is deprecated in newer version of geopy  # noqa: 501
            distance_unit = 'km'
            if is_delivery:
                delivery_time = round(distance + AVERAGE_PREPARATION_TIME + BUFFER_TIME)
                if delivery_time <= 60:
                    merchant['delivery_time_with_unit'] = '{} MIN'.format(delivery_time)
                else:
                    delivery_time_hours = delivery_time // 60
                    delivery_time_minutes = delivery_time % 60
                    merchant['delivery_time_with_unit'] = '{hours} HRS {minutes} MIN'.format(
                        hours=delivery_time_hours, minutes=delivery_time_minutes
                    )
                merchant['delivery_time'] = delivery_time
            if is_takeaway:
                if not distance >= 1:
                    distance = distance * 1000
                    distance_unit = 'm'
                distance = round(distance, 2)
                merchant['distance'] = distance
                merchant['distance_with_unit'] = '{distance} {unit}'.format(
                    distance=distance, unit=distance_unit
                )
        return merchants
