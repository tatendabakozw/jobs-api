from flask import Blueprint, request, jsonify, Response
import bcrypt
from bson import json_util
from config.database import mongo
import json
import jwt
from flask import current_app
from middleware.auth_middleware import token_required

user_route = Blueprint('user_route',__name__)

# get single user
# get request
# /api/user/single
@user_route.route("/api/user/single", methods=["GET"])
@token_required
def get_single_user(current_user):
    return jsonify(current_user)

# edit single user
# patch request
# /api/user/edit
@user_route.route("/api/user/edit", methods=["PATCH"])
@token_required
def edit_single_user(current_user):
    return jsonify(current_user)

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