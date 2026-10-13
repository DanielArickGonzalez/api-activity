from flask import Flask, request
from flask_restful import Resource, Api
from my_api.db import Database
from flask_bcrypt import Bcrypt
from flask import Flask, jsonify, request, g
from flask_restful import Resource, Api, reqparse
from flask_bcrypt import Bcrypt
from functools import wraps

# Adjust these paths if the certs are not two levels up
_CERTIFICATE_PATH = "/home/daniel/CS188/MyCertificate.crt"
_KEYFILE_PATH = "/home/daniel/CS188/DanielKey.pem"


class Hello(Resource):
    def get(self):
        return {"message": "Hello World!"}


class Square(Resource):
    def get(self, num):
        return {"Shape": self.__class__.__name__, "Area": num * num}


class Echo(Resource):
    def get(self):
        return {
            "arg1": request.args.get("arg1"),
            "arg2": request.args.get("arg2"),
        }

class Profile(Resource):
    @auth_required
    def get(self):
        return jsonify({"message": f"Hello, {g.username}!"})

def init_api(app: Flask) -> None:
    api = Api(app)
    api.add_resource(Hello, "/")
    api.add_resource(Square, "/square/<int:num>")
    api.add_resource(Echo, "/echo")
    api.add_resource(Register, "/register")
    api.add_resource(Profile, "/profile")


class Register(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "username", type=str, required=True,
            help="Username cannot be blank",
    )
        parser.add_argument(
            "password", type=str, required=True,
            help="Password cannot be blank",
        )
        args = parser.parse_args()
        username = args['username']
        password = args['password']

        # Hash the password before storing it
        hashed_pwd = Bcrypt().generate_password_hash(password).decode(
            'utf-8'
        )

        db = get_db()
        if db.add_user(username, hashed_pwd):
            response = jsonify(
                {"message": f"User {username} registered successfully"}
            )
            response.status_code = 201
            return response
        else:
            return {"message": f"User {username} already exists"}, 409


def create_app() -> Flask:
    app = Flask(__name__)
    init_api(app)
    return app


def run_app(debug: bool = True, with_ssl: bool = True) -> None:
    ssl_context = (_CERTIFICATE_PATH, _KEYFILE_PATH) if with_ssl else None
    create_app().run(debug=debug, ssl_context=ssl_context)


def main() -> None:
    run_app()

def get_db()-> Database:
    if "db" not in g:
        g.db = Database()
    return g.db

def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if auth is None:
            return {"message": "Authentication required"}, 401
        db = get_db()
        hashed_pwd = db.get_password(auth.username)
        valid = hashed_pwd is not None and Bcrypt().check_password_hash(
            hashed_pwd, auth.password
        )
        if not valid:
            return {"message": "Invalid credentials"}, 401
        g.username = auth.username
        return func(*args, **kwargs)
    return wrapper

if __name__ == "__main__":
    run_app()