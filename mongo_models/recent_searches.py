from flask_mongoengine import Document
from mongoengine import (EmbeddedDocument, EmbeddedDocumentField, IntField,
                         ListField)


class Searches(EmbeddedDocument):
    takeaway = ListField()
    delivery = ListField()


class RecentSearch(Document):
    user_id = IntField(required=True)
    recent_searches = EmbeddedDocumentField(Searches)

    meta = {
        'collection': 'recent_search',
        'indexes': [{'fields': ['-user_id'], 'unique': True}]
    }

    @classmethod
    def verify_search_query(cls, search_query, user_id, is_delivery=False):
        """
        Verifies that either search query is already present in recent searches of user

        :param str search_query: search query
        :param int user_id: user id
        :param bool is_delivery: delivery flag
        :rtype bool
        """
        user_data = cls.objects(user_id=user_id).first()
        if user_data:
            recent_searches = user_data.recent_searches.takeaway
            if is_delivery:
                recent_searches = user_data.recent_searches.delivery
            if search_query in recent_searches:
                return True
            return False
        return False

    @classmethod
    def save_search_query(cls, search_query, user_id, is_delivery=False):
        """
        Saves search query in recent searches

        :param str search_query: search query
        :param int user_id: user id
        :param bool is_delivery: delivery flag
        """
        user_data = cls.objects(user_id=user_id).first()
        if user_data:
            recent_searches = user_data.recent_searches.takeaway
            if is_delivery:
                recent_searches = user_data.recent_searches.delivery
            recent_searches.insert(0, search_query)
            if is_delivery:
                user_data.recent_searches.delivery = recent_searches[:5]
            else:
                user_data.recent_searches.takeaway = recent_searches[:5]
            user_data.save()
        else:
            recent_searches = Searches(takeaway=[search_query])
            if is_delivery:
                recent_searches = Searches(delivery=[search_query])
            user_data = cls(user_id=user_id, recent_searches=recent_searches)
            user_data.save()

    @classmethod
    def get_recent_searches(cls, user_id, is_delivery=False):
        """
        Gets recent searches

        :param int user_id: user id
        :param bool is_delivery: delivery flag
        :rtype list
        :returns recent searches
        """
        user_data = cls.objects(user_id=user_id).first()
        if user_data:
            if is_delivery:
                return user_data.recent_searches.delivery
            return user_data.recent_searches.takeaway
        return []
