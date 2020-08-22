"""Add direct routes here"""

from flask import current_app as app
from application.model.predict import mongo


@app.route('/ping')
def ping():
    return {"text": "Pong"}

@app.route('/file/<filename>')
def image(filename):
    return '<img src="{mongo.send_file(filename)}">'
