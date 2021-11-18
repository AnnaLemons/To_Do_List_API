"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os

from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin

from models import db, Task
from sqlalchemy import exc
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

    #GET TASK

@app.route('/task', methods=['GET'])
def get_task():
    tasks= Task.get_all()
    if tasks:
        return jsonify(tasks),200

    return jsonify({'msg':'No task available'}), 404

    #GET TASK BY ID

@app.route('/task/<int:id>', methods=['GET'])
def get_task_by_id(id):
    task= Task.get_by_id(id)

    if task:
        return jsonify(task.to_dict()), 200

    return jsonify({'error': 'Task is not found'}), 404

    #CREATE "TO DO"

@app.route('/task', methods=['POST'])
def create_to_do():
    new_to_do=request.json.get('item',None)

    if not new_to_do:
        return jsonify({'error':'Missing task'}), 400

    task= Task(to_do=new_to_do, done=False)
    try:
        task_created=task.create()
        return jsonify(task_created.to_dict()), 201
    except exc.IntegrityError:
        return jsonify({'error': 'Fail in data'}), 400

    #UPDATE "TO DO"

@app.route('/task/<int:id>', methods=['PUT','PATCH'])
def update_to_do(id):
    new_to_do=request.json.get('item', None)

    if not new_todo:
        return jsonify({'error': 'Missing task'}), 400

    task= Task.get_by_id(id)
    if task:
        task=task.update(new_to_do)
        return jsonify(task.to_dict()), 200

    return jsonify({'error': 'Task is not found'}), 404

    #DELETE "TO DO"

@app.route('/task/<int:id>', methods=['DELETE'])
def delete_to_do(id):
    task=Task.get_by_id(id)
    if task:
        task.delete()
        return jsonify(task.to_dict()), 200

    return jsonify({'error':'Task is not found'}), 404

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
