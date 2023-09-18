from flask import Blueprint, request, jsonify, Response
from bson.objectid import ObjectId
from bson import json_util
from ...config.database import mongo
import json
from flask import current_app
from ...middleware.auth_middleware import token_required

user_route = Blueprint('user_route',__name__)

# get single user
# get request
# /api/user/single/<user_id>
@user_route.route("/api/user/single/<user_id>", methods=["GET"])
def get_single_user(user_id):
    try:
        user = mongo.db.user.find_one({"_id": ObjectId(user_id)})
        if user:
            resp = json.loads(json_util.dumps(user))
            return jsonify(resp)
        else:
            return {
                    "error": "User does not exist",
                    "message": str(e)
                }, 404

    except Exception as e:
        return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500
    

# edit single user
# patch request
# /api/user/edit
@user_route.route("/api/user/edit/<user_id>", methods=["PATCH"])
@token_required
def edit_single_user(current_user, user_id):
    mongo.db.user.update_one({"_id": ObjectId(user_id)},
                  { "$set": {
                             "name": request.json .get('name'),
                              "photoURL": request.json .get('photoURL'),
                             }
                 })
    return {
        "message": "Account edited"
    }
    # return jsonify(current_user)

# delete single user
# delete request
# /api/user/delete
# @user_route.route("/api/user/delete", methods=["DELETE"])
# @token_required
# def edit_single_user(current_user):
#     return jsonify(current_user)

# get all users and search
# post request
# /api/user/all
# @user_route.route("/api/user/all", methods=["POST"])
# @token_required
# def edit_single_user(current_user):
#     return jsonify(current_user)