from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pickle

# Instantiate SQLAlchemy to handle db process
db = SQLAlchemy()

#create the Flask app
app = Flask(__name__)


# load configuration from config.cfg
app.config.from_pyfile('config.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# new method for SQLAlchemy version 3 onwards
with app.app_context():
    db.init_app(app)
    from .models import Entry , EntryCifar
    db.create_all()
    db.session.commit()
    print('Created Database!')
    # print all tables in the database
    # print(f'Tables created{db.metadata.tables} ')

#AI model file
joblib_file = "application/static/Pickle_RL_Model.pkl"
# Load from file
with open(joblib_file, 'rb') as f:
    ai_model = pickle.load(f)



# run the file routes
from application import routes
