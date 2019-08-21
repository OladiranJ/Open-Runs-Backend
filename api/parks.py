# Imports

import models

from flask                  import Blueprint, request, jsonify
from playhouse.shortcuts    import model_to_dict



# ------------------------------------------------------------------------------------------------------

# Blueprints


park = Blueprint('park', 'park', url_prefix="/api/v1")


# ------------------------------------------------------------------------------------------------------

# Decorations and Functions

@park.route('/', methods=["GET"])
def get_all_parks():
    try:
        parks   = [model_to_dict(park) for park in models.Park.select()]
        return  jsonify(data=parks, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return  jsonify(data={}, status={"code": 401, "message": "There was an error getting the resource"})


@park.route('/', methods=["POST"]) # may not be working because we haven't created any parks
def create_parks():
    payload = request.get_json()
    print(payload, 'payload', type(payload), 'type')
    park_dict   = model_to_dict(park)
    return  jsonify(data=park_dict, status={"code": 201, "message": "Success"})


@park.route('/<id>', methods=["GET"])
def get_one_park(id):
    park    = models.Park.get_by_id(id)
    return  jsonify(data=model_to_dict(park), status={"code": 200, "message": "Success"})


@park.route('/<id>', methods=["PUT"])
def update_park(id):
    payload = request.get_json()
    query   = models.Park.update(**payload).where(models.Park.id == id)
    query.execute()

    update_park = models.Park.get_by_id(id)
    return  jsonify(data=model_to_dict(updated_park), status={"code": 200, "message": "Success"})


@park.route('/<id>', methods=["Delete"])
def delete_park(id):
    query   = models.Park.delete().where(models.Park.id == id)
    query.execute()

    return  jsonify(data='resources successfully deleted', status={"code": 200, "message": "Resource Deleted"})
