from flask import current_app


# mongo db configurations
current_app.config['MONGODB_SETTINGS'] = {
    'db': 'ofd_db',
    'host': 'localhost',
    'port': 27017
}
