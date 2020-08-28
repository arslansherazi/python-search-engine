from flask import Flask


def create_app():
    app = Flask(__name__)
    return app


def add_routing():
    from routing.resources import api_urls
    api_urls()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        add_routing()
        app.debug = True
        app.run(host='0.0.0.0', port=5000)
        app.run(debug=True)
