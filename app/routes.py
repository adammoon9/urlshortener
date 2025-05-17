from flask import Blueprint, jsonify, request
from .db_helper import DBHelper as db
from .models.url import URL
from .extensions import db as sa
import string, random

main = Blueprint('main', __name__)

def create_short_code(length=6):
    alphabet = string.ascii_letters + string.digits
    short_code = ''.join(random.choices(alphabet, k=length))
    while sa.session.query(URL).filter_by(shortCode=short_code).first():
        short_code = ''.join(random.choices(alphabet, k=length))
    return short_code 

@main.route('/shorten',  methods=['POST'])
def create_url():
    data = request.json
    if not 'url' in data:
        return jsonify({'msg': 'Invalid URL or URL Not found in request data.'}), 400
    new_url = db.create_url(data['url'], create_short_code())
    return jsonify(new_url.serialize()), 201

@main.route('/shorten/<url>', methods=['GET'])
def get_url(url: str):
    result = db.get_url(url)
    if result:
        return jsonify(result.serialize()), 200
    return jsonify({'msg': 'URL Not Found'}), 404

@main.route('/shorten/<url>/stats', methods=['GET'])
def get_url_statistics(url:str):
    result = db.get_url(url)
    if result:
        return jsonify(result.serialize() | {'accessCount': result.accessCount}), 200
    return jsonify({'msg': 'URL Not Found'}), 404

@main.route('/shorten/<url>', methods=['PUT'])
def update_url(url:str):
    data = request.json
    if not 'url' in data:
        return jsonify({'msg': 'Invalid URL or URL Not found in request data.'}), 400
    
    new_url = request.json['url']
    result = db.update_url(new_url, url)
    if result:
        return jsonify(result.serialize()), 200
    return jsonify({'msg': 'URL Not Found'}), 404

@main.route('/shorten/<url>', methods=['DELETE'])
def delete_url(url:str):
    result = db.delete_url(url)
    if result == 404:
        return jsonify({'msg': 'URL Not Found'}), result
    return '', result