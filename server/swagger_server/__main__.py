#!/usr/bin/env python3
from swagger_server.api import WebApi

def main():

    app = WebApi().init_flask_app()
    app.run(port=8080)


if __name__ == '__main__':
    main()
