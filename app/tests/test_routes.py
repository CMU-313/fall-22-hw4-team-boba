from flask import Flask
import pandas as pd
import os
import sys

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

    # missing data test
    missing_data={'Dalc':1, 'failures':3, 'G1':18, 'G2':20, 'absences':4}
    response1 = client.get(url, query_string=missing_data)
    assert response1.status_code == 500
    
    # invalid data test
    invalid_data_queries = [
        {'G1': 30, 'G2': 8, 'studytime': 2, 'failures': 4, 'absences': 0}, # G1
        {'G1': 20, 'G2': -2, 'studytime': 2, 'failures': 4, 'absences': 0}, # G2
        {'G1': 20, 'G2': 8, 'studytime': 10, 'failures': 4, 'absences': 0}, # studytime
        {'G1': 20, 'G2': 8, 'studytime': 2, 'failures': -10, 'absences': 0}, # failres
        {'G1': 20, 'G2': 8, 'studytime': 2, 'failures': 4, 'absences': 94}] # absences
    for query in invalid_data_queries:
        invalid = client.get(url, query_string=query)
        assert invalid.status_code == 400     
        print(invalid.get_data())
        sys.stdout.flush()
        
    # success test good student
    correct_data={'studytime':2, 'failures':1, 'G1':19, 'G2':19, 'absences':0}
    response3 = client.get(url, query_string=correct_data)
    assert response3.status_code == 200
    assert response3.get_data() == b'1\n'
    
    # success test not good student
    correct_data={'studytime':1, 'failures':3, 'G1':6, 'G2':9, 'absences':17}
    response3 = client.get(url, query_string=correct_data)
    assert response3.status_code == 200
    assert response3.get_data() == b'0\n'

    

