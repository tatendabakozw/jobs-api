from flask import Blueprint, request, jsonify, Response
import bcrypt
from bson import json_util
from ...config.database import mongo
import json
import jwt
from flask import current_app

app_file1 = Blueprint('app_file1',__name__)

# default route location
# get request
# /api/post/auth/
@app_file1.route("/auth", methods=["GET"])
def hello():
    return "Auth route"

# register new user
# post request
# /api/post/auth/register
@app_file1.route("/auth/register", methods=["POST"])
def register_user():

    if request.method != "POST":
        resp = {
            "message": "method not allowed",
            "status": 500
        }
        return jsonify(resp)

    _json = request.json
    _name = _json.get("name", None)
    _email = _json.get("email", None)
    _password = _json.get("password", None)
    _password2 = _json.get("password2", None)
    _account_type = _json.get("account_type", None)

    # check if all fields are entered
    if _name is None or _email is None or _password is None or _password2 is None or _account_type is None:
        resp = {
            "message": "Please enter required feilds",
            "status": 401
        }
        return jsonify(resp)
    
    # check length of password
    if len(_password) <6 :
        resp = {
            "message": "Password must be greater than 6 characters",
            "status": 401
        }
        return jsonify(resp)

    # check if passwords mnatch
    if _password != _password2:
        resp = {
            "message": "Passwords do not match",
            "status": 401
        }
        return jsonify(resp)
    
    # ecrypt password
    # converting password to array of bytes
    bytes = _password.encode('utf-8')
    # generating the salt
    salt = bcrypt.gensalt()
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)

    user = mongo.db.user.find_one({"email": _email})

    if user:
        resp = {
            "message": "User already exists",
            "status": 400
        }
        return jsonify(resp)

    new_user = {
        "name": _name,
        "password": hash,
        "email": _email,
        "account_type": _account_type
    }

    id = mongo.db.user.insert(new_user)
    # id = mongo.db.

    if(id):
        resp = {
            "message": "Account created successfully!",
            "status": 200
        }
        return jsonify(resp)
    else:
        resp = {
            "message": "Could not create account",
            "status": 500
        }
        return jsonify(resp)
    
# login user
# post request
# /api/post/auth/login
@app_file1.route("/auth/login", methods=["POST"])
def login_user():
    if request.method != "POST":
        resp = {
            "message": "method not allowed",
            "status": 500
        }
        return jsonify(resp)

    _json = request.json
    _email = _json.get("email", None)
    _password = _json.get("password", None)

    # check if user exists in database
    user = mongo.db.user.find_one({"email": _email})

    if user:
        # encoding user password
        userBytes = _password.encode('utf-8')
        resp = json.loads(json_util.dumps(user))
        result = bcrypt.checkpw(userBytes, resp["password"].encode('utf-8'))

        print(result)
        if(result):
            try:
                resp["token"] = jwt.encode(
                    {"user_id": resp["_id"], "email": resp["email"]},
                    current_app.config["SECRET_KEY"],
                    algorithm="HS256"
                )
                return {
                    "message": "Successfully fetched auth token",
                    "data": {
                        "email": resp["email"],
                        "name": resp["name"],
                        "account_type": resp["account_type"],
                        "token": resp["token"],
                        "user_id": resp["_id"]
                    }
                }
            except Exception as e:
                return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500
        
        resp = {
            "message": "Wrong login details",
            "status": 403
            }

        return resp

    else:
        resp = {
            "message": "Account does not exist",
            "status": 404
        }
        return jsonify(resp)

