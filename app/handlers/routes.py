import this
from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os

def configure_routes(app):
    # load model from 'database'
    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    clf = joblib.load(model_path)

    # default
    @app.route('/')
    def hello():
        return "try the predict route it is great!"

    # predict a student
    @app.route('/predict')
    def predict():
        # we use the G1, G2, absences, studytime, and failures features
        # data sent in parameters of request
        g1 = int(request.args.get('G1'))
        g2 = int(request.args.get('G2'))
        studytime = int(request.args.get('studytime'))
        failures = int(request.args.get('failures'))
        absences = int(request.args.get('absences'))
        #data = [[g1], [g2], [absences],[studytime],[failures]]
        
        # validate data
        assert(g1 in range(0, 20)) # (numeric: from 0 to 20)
        assert(g2 in range(0, 20))# (numeric: from 0 to 20)
        assert(studytime in range(1, 4)) # (numeric: 1 - <2 hours, 2 - 2 to 5 hours, 3 - 5 to 10 hours, or 4 - >10 hours)
        assert(failures in range(1, 4)) # (numeric: n if 1<=n<3, else 4)
        assert(absences in range(0, 93)) # (numeric: from 0 to 93)
        
        # load data into query_df
        query_df = pd.DataFrame({
            'G1': pd.Series(g1),
            'G2': pd.Series(g2),
            'absences': pd.Series(absences),
            'studytime': pd.Series(studytime),
            'failures': pd.Series(failures)
        })
        
        # set query and run predict ML
        query = pd.get_dummies(query_df)
        prediction = clf.predict(query)
        
        return jsonify(np.ndarray.item(prediction))
    