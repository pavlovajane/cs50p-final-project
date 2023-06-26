from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

APP = Flask(__name__)
API = Api(APP)

# Enable debug mode to allow on the fly updates (DISCLAIMER: this is an edu project - not for production)
APP.debug = True

def main():
    APP.run()


def function_1():
    ...


def function_2():
    ...


def function_n():
    ...


if __name__ == "__main__":
    main()
