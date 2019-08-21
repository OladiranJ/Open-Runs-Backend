# Imports

import models
import os
import sys
import secrets

from PIL                    import Image
from flask                  import Blueprint, request, jsonify, url_for, send_file
from flask_bcrypt           import generate_password_hash, check_password_hash
from flask_login            import login_user, current_user
from playhouse.shortcuts    import model_to_dict


# ------------------------------------------------------------------------------------------------------

# Blueprints

user    = Blueprint('users', 'user', url_prefix='/user')


# ------------------------------------------------------------------------------------------------------

# Decorations and Functions

def save_picture(form_picture):
    random_hex              = secrets.token_hex(8)
    f_name, f_ext           = os.path.splitext(form_picture.filename)
    picture_name            = random_hex + f_ext
    file_path_for_avatar    = os.path.join(os.getcwd(), 'static/profile_pics/' + picture_name)
    output_size             = (125, 175)

    i   = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(file_path_for_avatar)

    return picture_name
    

@user.route('/register', methods = ["POST"])
def register():
    pay_file    = request.files
    payload     = request.form.to_dict()
    dict_file   = pay_file.to_dict()

    print(payload)
    print(dict_file)

    payload['email'].lower()
    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, status={"code": 401, "message": "A user with that name or email exists"})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        file_picture_path   = save_picture(dict_file['file'])
        payload['image']    = file_picture_path
        user                = models.User.create(**payload)

        print(type(user))

        login_user(user)
        current_user.image  = model_to_dict(user)

        print(user_dict)
        print(type(user_dict))

        del user_dict['password']
        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

    return "Hi from register"


@user.route('<id>/parks', methods=['GET'])
def get_user_parks(id):
    user    = models.User.get_by_id(id)
    print(user.parks, '.parkssss')

    parks   = [model_to_dict(park) for park in parks]

    def delete_key():
        del item[key]
        return item

    park_without_user   = [delete_key(park, 'user') for park in parks]

    return  jsonify(data=park_without_user, status={"code": 200, "message": "Success"})