from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from config.database import mongo
import json
from bson import json_util

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
            # print(token)
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data  =  jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            print(data)
            # resp = json.loads(json_util.dumps(data))
            # current_user = mongo.db.user.find_one({"email": json.loads(json_util.dumps(data))["email"]})
            current_user = data 
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            # if not current_user["active"]:
            #     abort(403)
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e),
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated