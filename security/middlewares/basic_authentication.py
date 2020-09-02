import json

from flask import Response, current_app, request

from security.security_credentials import (BASIC_AUTH_PASSWORD,
                                           BASIC_AUTH_USERNAME)


@current_app.before_request
def basic_authentication():
    if request.authorization:
        if (
                request.authorization.username == BASIC_AUTH_USERNAME and
                request.authorization.password == BASIC_AUTH_PASSWORD
        ):
            return
    response = Response()
    response.mimetype = 'application/json'
    response.data = json.dumps({
        'message': 'Unauthorized Access',
        'status_code': 401,
        'success': False
    })
    response._status = '401 OK'
    response._status_code = 401
    return response
