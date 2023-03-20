from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join('/Users/', 'database.db')
db = SQLAlchemy(app)

app.config.from_object(__name__)
from app import router