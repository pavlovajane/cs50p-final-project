#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from flask_injector import FlaskInjector
from swagger_server.persistence.database import get_dependencies


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', 
                dependencies=get_dependencies(),
                arguments={'title': 'MONTY PYTHON BEST QUOTES API'}, 
                pythonic_params=True)
    # FlaskInjector(app=app.app, modules=[configure_database])
    app.run(port=8080)


if __name__ == '__main__':
    main()
