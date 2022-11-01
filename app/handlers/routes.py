import this
from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os

def configure_routes(app):

    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    dclf = joblib.load(model_path)

    @app.route('/')
    def hello():
        return "try the predict route it is great!"

    @app.route('/clean')
    def clean():
        #cleans the data and prepares it for input to ML
        return "cleaned data"

    @app.route('/train')
    def train():
        # take json format data to train a model, data may be 
        # give back a model, select 
        return "mock model id"

    @app.route('/predict')
    def predict():
        # Planned modifications for next part of Hw4: 
        #   - change this fucntion to take json of one or many students and give back one or more G3 scores
        #   - use entries from the query string here but could also use json
        # Below function only implemented in case of prediction on one student
        # instead of multiple. Multiple student implementation will hold in 
        # next homework. 
        g1 = request.args.get('G1')
        absences = request.args.get('absences')
        g2 = request.args.get('G2')
        studytime = request.args.get('studytime')
        failures = request.args.get('failures')
        data = [[g1], [g2], [absences],[studytime],[failures]]
        query_df = pd.DataFrame({
            'G1': pd.Series(g1),
            'G2': pd.Series(g2),
            'absences': pd.Series(absences),
            'studytime': pd.Series(studytime),
            'failures': pd.Series(failures)
        })
        query = pd.get_dummies(query_df)
        prediction = clf.predict(query)
        return jsonify(np.asscalar(prediction))
    
    @app.route('/test')
    def test():
        # tests how well the model performs
        try:
            if True:
                return "better prediction on trained model" 
            else:
                return "need better training for better results"
        except:
            return "Error: testing cannot be done with invalid dataset"