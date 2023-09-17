import os
from flask import Flask, request, jsonify, make_response
from dotenv import load_dotenv
from flask_pymongo import PyMongo

# load virtual environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "secretkey"

# load mongo uri from env file
mongo_db_url = os.environ.get("MONGO_DB_CONN_STRING")
app.config['MONGO_URI'] = mongo_db_url

# connect database
mongo = PyMongo(app)

if __name__ == "__main__":
    app.run(debug=True)

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
