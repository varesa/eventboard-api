import datetime
import os
import json

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Initialize app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.Text, nullable=False)
    body  = db.Column(db.Text, nullable=True)

    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    handled = db.Column(db.Boolean, default=False)

    reoccurring = db.Column(db.Boolean, default=False)
    interval = db.Column(db.Text)
    next_occurrance = db.Column(db.DateTime)


def get_all(handled=False):
    if handled:
        events = db.session.query(Event).all()
    else:
        events = db.session.query(Event).filter_by(handled=False).all()

    arr = []

    for event in events:
        next = event.time if not event.reoccurring else event.next_occurrance
        arr.append({
            "id": event.id,

            "title": event.title,
            "body": event.body,

            "handled": event.handled,
            "next_occurrance": next.isoformat()
        })

    return arr


@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        event = Event(title=request.json['title'],
                      body=request.json['body'],
                      time=datetime.datetime.strptime(request.json['time'], '%Y-%m-%d %H:%M:%S'),
                      reoccurring=request.json['reoccurring'],
                      interval=request.json['interval'])
        db.session.add(event)
        db.session.commit()
        return "OK"
    else:
        return json.dumps(get_all())


# Basic healthcheck for orchestration and monitoring

@app.route('/health')
def healthcheck():
    return 'OK'

