from flask import Flask

from app.handlers.routes import configure_routes


def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)

    assert response.status_code == 200
    assert response.get_data() == b'try the predict route it is great!'

def test_clean_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/clean'

    response = client.get(url)

    assert response.status_code == 200
    assert response.get_data() == b'cleaned data'

def test_train_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/train'

    response = client.get(url)

    assert response.status_code == 200
    assert response.get_data() == b'mock model id'

