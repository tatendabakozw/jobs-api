from flask import Blueprint, request, jsonify, Response
import bcrypt
from bson import json_util
# import sys
# sys.path.append("..") 
from config.database import mongo
import json
import jwt
from flask import current_app

job_route = Blueprint('job_route',__name__)