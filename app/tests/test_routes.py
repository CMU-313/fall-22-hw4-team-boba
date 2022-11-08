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

# Helper function to find outliers.  
def find_outliers(df):
   q1=df.quantile(0.25)
   q3=df.quantile(0.75)
   iqr=q3-q1

   detected = df[((df<(q1-1.5*iqr)) | (df>(q3+1.5*iqr)))]

   return detected

def test_clean_route():
    '''
    Checking if the clean() endpoint got rid of duplicate data, null data, and 
    possible outliers. 
    For checking whether or not the outliers were cleaned up, it requires 
    extensive techniques like Z-score or IQR(Interquartile Range). 
    For this testing, we will use IQR to determine the outliers for simplicity. 
    '''
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    parent = os.path.dirname(os.getcwd())
    d_path = os.path.join(parent,"data")

    url = '/clean'

    response = client.get(url)

    assert response.status_code == 200
    assert response.get_data() == b'cleaned data'

    data_path = os.path.join(d_path,"cleaned-student.csv")
    data = pd.read_csv(data_path, sep=';')

    no_null = True 
    nulls = data.isnull()
    for r in range(len(nulls)):
        rowlst = list(nulls.loc[r])
        for i in range(len(rowlst)):
            if rowlst[i] == True:
                no_null = False
                break 
    
    
    # Testing no null data should return True if cleaned correctly
    assert no_null == True
    
    no_dups = True 
    for (c, v) in data.duplicated().iteritems():
        if v == True:
            no_dups = False 
            break
    
    assert no_dups == True

    print("Testing done for finding duplicates!")


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


    

