
import connexion
from swagger_server import encoder

class WebApi:

    def init_flask_app(self):
        app = connexion.App(__name__, specification_dir='./swagger/')
        app.app.json_encoder = encoder.JSONEncoder
        app.add_api('swagger.yaml',
                arguments={'title': 'MONTY PYTHON BEST QUOTES API'},
                pythonic_params=True)
        return app
