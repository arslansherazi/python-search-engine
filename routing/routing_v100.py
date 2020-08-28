from apis.v100.auto_suggest.api import AutoSuggest
from apis.v100.recent_searches.api import RecentSearches
from apis.v100.search.api import Search
from routing.base_routing import BaseRouting


class RoutingV100(BaseRouting):
    api_version = 100

    def set_routing_collection(self):
        self.routing_collection = {
            'search': Search,
            'auto_suggest': AutoSuggest,
            'recent_searches': RecentSearches
        }
