from flask_mongoengine import MongoEngine

from app import app

# mongo db configurations
app.config['MONGODB_SETTINGS'] = {
    'db': 'ofd_db',
    'host': 'localhost',
    'port': 27017
}
mongo_db = MongoEngine(app)
