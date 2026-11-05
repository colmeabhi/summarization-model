from flask import Flask

from config import Config
from routes.api import api
from routes.pages import pages


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(pages)
    app.register_blueprint(api)

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])
