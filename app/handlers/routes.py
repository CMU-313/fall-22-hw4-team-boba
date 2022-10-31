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
        # change this fucntion to take json of one or many students and give back one or more G3 scores
        #use entries from the query string here but could also use json
        age = request.args.get('age')
        absences = request.args.get('absences')
        health = request.args.get('health')
        data = [[age], [health], [absences]]
        query_df = pd.DataFrame({
            'age': pd.Series(age),
            'health': pd.Series(health),
            'absences': pd.Series(absences)
        })
        query = pd.get_dummies(query_df)
        prediction = clf.predict(query)
        return jsonify(np.asscalar(prediction))
    
    @app.route('/test')
    def test():
        # tests how well the model performs 
        return "test score"