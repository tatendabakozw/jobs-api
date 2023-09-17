import os
from flask import Flask, jsonify, json
from dotenv import load_dotenv
from routes.auth.auth import app_file1
from routes.user.user import user_route
from werkzeug.exceptions import HTTPException
from config.database import mongo

# load virtual environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "secretkey"

# load mongo uri from env file
mongo_db_url = os.environ.get("MONGO_DB_CONN_STRING")
app.config['MONGO_URI'] = mongo_db_url

# jwt keys

JWT_SECRET = os.environ.get('JWT_SECRET') or 'this is a secret'
print(JWT_SECRET)
app.config['JWT_SECRET'] = JWT_SECRET

# connect database
# mongo = PyMongo(app)
mongo.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)

#user defined routes
app.register_blueprint(app_file1)
app.register_blueprint(user_route)
    
# default app route
@app.route('/', methods=['GET'])
def check_api():
    _json = {
        "message": "Jobs API running",
        "status": 200 
    }

    resp = jsonify(_json)
    resp.status_code = 200

    return resp

"""
404 Page not found error default handler
"""
@app.errorhandler(404)
def page_not_found(e):
    _json = {
        "message": "Route not found",
        "status": 404 
    }

    resp = jsonify(_json)
    resp.status_code = 404

    return resp

"""
Parse other errors to json
"""
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "status": e.code,
        "name": e.name,
        "message": e.description,
    })
    response.content_type = "application/json"
    return response