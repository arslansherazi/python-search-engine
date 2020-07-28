from flask_restful import reqparse

search_parser = reqparse.RequestParser()

search_parser.add_argument(
    'offset',
    type=int,
    required=True,
    default=0
)
