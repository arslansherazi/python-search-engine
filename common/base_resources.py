import logging
import os

from flask import request
from flask_restful import Resource
from requests import codes

from common.constants import SUCCESS_STATUS_CODES


class BaseResource(Resource):
    request_parser = None
    status_code = 200
    end_point = ''
    version = None

    def request_flow(self):
        logger = None
        try:
            self.response = {}
            self.is_send_response = False
            self.request_args = None
            try:
                self.request_args = self.request_parser.parse_args()
            except Exception as e:
                self.response = {
                    'message': '{param}: {message}'.format(
                        param=list(e.data.get('message').keys())[0], message=list(e.data.get('message').values())[0]
                    )
                }
                self.status_code = codes.BAD_REQUEST
                return self.send_response()
            log_file_path = '../../logs/apis/{end_point}'.format(end_point=self.end_point)
            log_file = '{end_point}_v{version}.log'.format(end_point=self.end_point, version=self.version)
            logger = self.get_logger(log_file_path, log_file)
            self.process_request()
            return self.send_response()
        except Exception as e:
            if logger:
                logger.exception(str(e))
            self.status_code = codes.INTERNAL_SERVER_ERROR
            self.response = {
                'message': 'Internal Server Error'
            }
            return self.send_response()

    def get_logger(self, log_file_path, log_file):
        logger = logging.getLogger()
        if not os.path.isdir(log_file_path):
            os.makedirs(log_file_path)
        file_logging_formatter = logging.Formatter('%(asctime)s %(name)s %(message)s')
        file_handler = logging.FileHandler(filename='{log_file_path}/{log_file}'.format(
            log_file_path=log_file_path, log_file=log_file
        ))
        file_handler.suffix = '%Y-%m-%d'
        file_handler.setFormatter(file_logging_formatter)
        file_handler.setLevel(logging.INFO)
        file_handler.suffix = '%Y-%m-%d'
        logger.addHandler(file_handler)
        return logger

    def populate_request_arguments(self):
        pass

    def process_request(self):
        pass

    def send_response(self):
        self.response['success'] = True
        if self.status_code not in SUCCESS_STATUS_CODES:
            self.response['success'] = False
        self.response['status_code'] = self.status_code
        self.response['cmd'] = request.url_rule.rule
        return self.response, self.status_code


class BasePostResource(BaseResource):
    def post(self):
        return self.request_flow()


class BaseGetResource(BaseResource):
    def get(self):
        return self.request_flow()


class BasePutResource(BaseResource):
    def put(self):
        return self.request_flow()


class BaseDeleteResource(BaseResource):
    def delete(self):
        return self.request_flow()
