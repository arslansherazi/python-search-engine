from operator import itemgetter


class CommonHelpers(object):
    """
    Common Helpers
    """
    @staticmethod
    def sort_list_data(data, key, descending=False):
        """
        Sorts list of dictionaries data according to the key

        :param list data: data
        :param str key: sorting key
        :param bool descending: descending order
        :rtype list
        :return: sorted data
        """
        data.sort(key=itemgetter(key), reverse=descending)
        return data
