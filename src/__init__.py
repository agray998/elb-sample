from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import pymysql
import os

application = Flask(__name__)

xray_recorder.configure(service='My application')
XRayMiddleware(application, xray_recorder)

application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = "wjdvbbVBSCSFCVllmcl"

db = SQLAlchemy(application)

from src import forms
from src import routes
from src import models
