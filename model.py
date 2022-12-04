from flask import Flask;
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# app = Flask(__name__)   
dbname = 'unsplash';
DATABASE_URL =  'postgresql://postgres:19alema@localhost:5432/'+ dbname;

db = SQLAlchemy()
def setup_app(app, database_path = DATABASE_URL):
    migrate = Migrate(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)


    db.drop_all()
    db.create_all()
  





class Photos(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String , nullable=False)
    url = db.Column(db.String, nullable=False);

    def __init__(self, label, url):
        self.label = label
        self.url = url

    def insert(self):
        db.session.add(self)
        db.session.commit()

        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'label': self.label,
            'url': self.url
        }

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String , nullable=False)

