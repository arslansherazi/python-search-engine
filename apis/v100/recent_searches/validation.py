from flask_restful import reqparse
from flask_restful.inputs import boolean

recent_searches_parser = reqparse.RequestParser()

recent_searches_parser.add_argument(
    'user_id',
    type=int,
    required=True
)
recent_searches_parser.add_argument(
    'is_delivery',
    type=boolean,
    required=True
)
