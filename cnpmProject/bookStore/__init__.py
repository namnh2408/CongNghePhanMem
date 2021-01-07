from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager

app = Flask(__name__)

app.secret_key = '^%*&!^@^*gsuias1&^&!*^!&1bsa656&*9R54fgvc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234567890@localhost/bookstore?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app= app)
admin = Admin(app=app, name="N&B BookStore", template_mode='bootstrap3')
login = LoginManager(app=app)