from flask_restful import reqparse

auto_suggest_parser = reqparse.RequestParser()

auto_suggest_parser.add_argument(
    'query',
    type=str,
    required=True
)
