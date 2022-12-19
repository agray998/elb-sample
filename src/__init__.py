from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import pymysql
import os

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = "jdvbavsbbsSDBVVBASV"

db = SQLAlchemy(application)

from src import forms
from src import routes
from src import models
