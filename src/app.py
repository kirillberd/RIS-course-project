from flask import Flask
from infrastructure.api.setup import setup
from infrastructure.container import Container
import logging
import sys
from os import getenv

logger = logging.getLogger(__name__)

def init():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    app = Flask(__name__)
    app.secret_key = getenv("APP_SECRET_KEY")
    container = Container()
    setup(app, container)
    return app



if __name__ == "__main__":
    app = init()
    app.run(host="0.0.0.0", port=3001, debug=True)