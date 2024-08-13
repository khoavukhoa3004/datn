import logging
from flask import Blueprint, request, Response
from flask.globals import current_app
from flask.json import jsonify

blueprint = Blueprint('hello', __name__)

@blueprint.route('/api/hello', methods=['GET',])
def hello():
  return 'Hello'

@blueprint.route('/api/hellofile', methods=['POST',])
def receive_file():
  body = []
  for key in request.files.keys():
    body.append(key)
  # print(body)
  return ['Filename', body]