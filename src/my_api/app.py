import pytest
from flask import Flask, request
from flask_restful import Resource, Api


class Hello(Resource):
    def get(self):
        return {"message": "Hello World!"}


class Square(Resource):
    def get(self, num):
        return {"Shape": self.__class__.__name__, "Area": num * num}


class Echo(Resource):
    def get(self):
        # Query string only: /echo?arg1=foo&arg2=bar
        return {
            "arg1": request.args.get("arg1"),
            "arg2": request.args.get("arg2"),
        }


def init_api(app: Flask) -> None:
    api = Api(app)
    api.add_resource(Hello, "/")
    api.add_resource(Square, "/square/<int:num>")
    api.add_resource(Echo, "/echo")


def create_app() -> Flask:
    app = Flask(__name__)
    init_api(app)
    return app


def run_app(debug: bool = True) -> None:
    create_app().run(debug=debug)


if __name__ == "__main__":
    run_app()