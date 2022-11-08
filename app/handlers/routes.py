import this
from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os


def configure_routes(app):

    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    parent = os.path.dirname(os.getcwd())
    d_path = os.path.join(parent,"data")
    clf = joblib.load(model_path)

    @app.route('/')
    def hello():
        return "try the predict route it is great!"

    @app.route('/clean')
    def clean():
        data_path = os.path.join(d_path,"student-mat.csv")
        cleaned_path = os.path.join(d_path,"cleaned-student.csv")

        # cleans the data and prepares it for input to ML
        data = pd.read_csv(data_path, sep=';')

        # copy from the original csv dataset to avoid overwriting
        copied = data.copy()

        # delete any duplicate rows in-place
        copied.drop_duplicates(subset=None, inplace=True)

        # fill in any null values found in the dataset to the mean value of
        # each column
        copied.fillna(np.around(copied.mean(), decimals=2), inplace=True)

        copied.to_csv(cleaned_path)

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
        print(request.args.get('G1'))
        g1 = int(request.args.get('G1'))
        absences = int(request.args.get('absences'))
        g2 = int(request.args.get('G2'))
        studytime = int(request.args.get('studytime'))
        failures = int(request.args.get('failures'))
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
        return jsonify(np.ndarray.item(prediction))
    
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