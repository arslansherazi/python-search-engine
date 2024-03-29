from flask_restful import reqparse
from flask_restful.inputs import boolean

search_parser = reqparse.RequestParser()

search_parser.add_argument(
    'offset',
    type=int,
    required=True
)
search_parser.add_argument(
    'query',
    type=str,
    required=True
)
search_parser.add_argument(
    'user_id',
    type=int,
    required=True
)
search_parser.add_argument(
    'latitude',
    type=float,
    required=True
)
search_parser.add_argument(
    'longitude',
    type=float,
    required=True
)
search_parser.add_argument(
    'is_takeaway',
    type=boolean,
    required=True
)
search_parser.add_argument(
    'is_delivery',
    type=boolean,
    required=True
)
search_parser.add_argument(
    'is_auto_suggest_items',
    type=boolean,
    required=False,
    default=False
)
