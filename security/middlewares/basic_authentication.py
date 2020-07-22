from flask import Response, request

from app import app
from security.security_credentials import BASIC_AUTH_PASSWORD


@app.before_request
def basic_authentication():
    header_authorized_key = request.headers.environ['HTTP_HEADER_AUTHORIZED_KEY']
    if header_authorized_key != BASIC_AUTH_PASSWORD:
        response = Response()
        response.data = str.encode('Unauthorized Access')
        response._status = '401 OK'
        response._status_code = 401
        return response
