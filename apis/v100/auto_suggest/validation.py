from flask_restful import reqparse

auto_suggest_parser = reqparse.RequestParser()

auto_suggest_parser.add_argument(
    'query',
    type=str,
    required=True
)
auto_suggest_parser.add_argument(
    'is_takeaway',
    type=int,
    required=True
)
auto_suggest_parser.add_argument(
    'is_delivery',
    type=int,
    required=True
)
