from flask_api import FlaskAPI
from interpi_client import interpi_client
import os

# start button daemon
path = os.path.dirname(os.path.realpath(__file__))
os.system('python3 ' + path + '/button_daemon.py')

app = FlaskAPI(__name__)
api = interpi_client.Interpi_client()

from interpi_client import routes
