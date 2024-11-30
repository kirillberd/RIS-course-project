from flask import Flask
from infrastructure.api.setup import setup
from infrastructure.container import Container
import logging
import sys

logger = logging.getLogger(__name__)

def init():
    logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
    app = Flask(__name__)
    container = Container()
    setup(app, container)
    return app



if __name__ == "__main__":
    app = init()
    app.run(host="0.0.0.0", port=4000, debug=True)