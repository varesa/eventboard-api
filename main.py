import datetime
import os
import random
import string

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Initialize app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def root():
    return ""


# Basic healthcheck for orchestration and monitoring

@app.route('/health')
def healthcheck():
    return 'OK'

