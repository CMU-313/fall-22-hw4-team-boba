from flask import Flask
import pandas as pd
import os

from app.handlers.routes import configure_routes


def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)

    assert response.status_code == 200
    assert response.get_data() == b'try the predict route it is great!'

def test_predict_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    missing_data={'Dalc':1, 'failures':3, 'G1':18, 'G2':20, 'absences':4}
    response1 = client.get(url, query_string=missing_data)
    assert response1.status_code == 500
    #assert response1.get_data() == b'Error: Not given one or more required input columns.'

    # incorrect_data={'studytime':1, 'failures':-2, 'G1':18, 'G2':20, 'absences':4}
    # response2 = client.get(url, query_string=incorrect_data)
    # assert response2.status_code == 500
    #assert response2.get_data() == b'Error: One of the column values are invalid.'

    correct_data={'studytime':2, 'failures':0, 'G1':19, 'G2':19, 'absences':0}
    response3 = client.get(url, query_string=correct_data)
    assert response3.status_code == 200
    assert response3.get_data() == b'1\n'


    

