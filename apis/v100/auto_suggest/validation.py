from flask_restful import reqparse
from flask_restful.inputs import boolean

auto_suggest_parser = reqparse.RequestParser()

auto_suggest_parser.add_argument(
    'query',
    type=str,
    required=True
)
auto_suggest_parser.add_argument(
    'is_takeaway',
    type=boolean,
    required=True
)
auto_suggest_parser.add_argument(
    'is_delivery',
    type=boolean,
    required=True
)
