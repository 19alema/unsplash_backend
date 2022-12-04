from flask import Flask;
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sqlalchemy as sa

dbname = 'unsplash';
DATABASE_URL =  'postgresql://postgres:19alema@localhost:5432/'+ dbname;

db = SQLAlchemy()
def setup_app(app, database_path = DATABASE_URL):
    migrate = Migrate(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)

    if not inspector.has_table("users"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
    else:
        app.logger.info('Database already contains the users table.')







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

