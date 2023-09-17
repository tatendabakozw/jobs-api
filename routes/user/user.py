from flask import Blueprint, request, jsonify, Response
import bcrypt
from bson import json_util
from ...config.database import mongo
import json
import jwt
from flask import current_app
from ...middleware.auth_middleware import token_required

user_route = Blueprint('user_route',__name__)

# get single user
# get request
# /api/user/single
@user_route.route("/api/user/single", methods=["GET"])
@token_required
def get_single_user(current_user):
    return jsonify(current_user)