import optparse

from flask import Flask
from flask_mongoengine import MongoEngine


def create_app():
    """
    Creates flask app. It also creates context of flask app

    :returns flaks app
    """
    app = Flask(__name__)
    with app.app_context():
        add_routing()
        app.config.from_envvar('APPLICATION_SETTINGS')
        mongo_db = MongoEngine(app)
        from security.middlewares import basic_authentication
    return app


def add_routing():
    """
    Adds routing of project into flask app
    """
    from routing.resources import api_urls
    api_urls()


def run_app(app, default_host='127.0.0.1', default_port='5000'):
    """
    Runs flask app. It also handles command line arguments for host and port

    :param app: flaks app
    :param str default_host: default host
    :param int default_port: default port
    """
    # Handles command line arguments
    parser = optparse.OptionParser()
    parser.add_option(
        '--host',
        help='Host of flask app. Default: {}'.format(default_host),
        default=default_host
    )
    parser.add_option(
        '--port',
        help='Port of flask app. Default: {}'.format(default_port),
        default=default_port
    )
    parser.add_option(
        '--debug',
        help='Handle debug mode of flask app',
        dest='debug',
        default='1'
    )
    options, _ = parser.parse_args()

    # run app
    app.run(
        host=options.host,
        port=options.port,
        debug=bool(int(options.debug))
    )


if __name__ == '__main__':
    app = create_app()
    run_app(app)
