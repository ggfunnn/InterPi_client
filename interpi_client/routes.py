from interpi_client import app
from interpi_client import api


@app.route('/ring/', methods=['GET', 'POST'])
def ring():
    return api.ring()
