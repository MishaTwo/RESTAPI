from flask import Flask, jsonify, json, request
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
from .database.users import *
from .database.base import *
from dotenv import load_dotenv
import os


load_dotenv()


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app, resources={r'/*': {"origins": os.getenv("ORIGINS") }})

api = Api(app)

class UserGetPost(Resource):
    def get(self):
        users = User.query.all()
        users_list = [{"user_id": user.id, "name": user.name, "email": user.email} for user in users]
        return jsonify(users_list)

    def post(self):
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")

        if not name or not email:
            return jsonify({"message": "Name and Email are required!"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"message": "User with this email already exists"}), 400

        new_user = User(
            name=name,
            email=email
        )

        session.add(new_user)
        session.commit()

        message = {
            "message": "User created",
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email
            }
        }
        return jsonify(message), 201

api.add_resource(UserGetPost, '/users')
    
SWAGGER_URL = "/swagger"
API_URL = "http://127.0.0.1:5000/swagger.json"
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "SAMPLE API"
    }
)
app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

from . import routes
