from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@35.246.19.86:3306/NEW"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "123"

db = SQLAlchemy(app)

from application import routes 