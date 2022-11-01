from flask import Flask
import pandas as pd

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

    url = '/clean'

    response = client.get(url)

    assert response.status_code == 200
    assert response.get_data() == b'cleaned data'

    data = pd.read_csv('data/student-mat.csv', sep=';')

    no_null = True 
    for r in range(len(data.values)):
        for c in range(len(data.values[0])):
            if data.values[r][c] == True:
                # Null data found - data cleaning not successful
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

    outliers = find_outliers(data)
    assert len(outliers) == 0

def test_train_route():
    '''
    theoretically, testing train() endpoint is not necessary since 
    this testing will happen in test() endpoint. 
    '''
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/train'

    response = client.get(url)

    assert response.status_code == 200
    assert response.get_data() == b'mock model id'

def test_predict_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/predict'

    missing_data={'Dalc':1, 'failures':3, 'G1':18, 'G2':20, 'absences':4}
    response1 = client.get(url, query_string=missing_data)
    assert response1.status_code == 400
    assert response1.get_data() == b'Error: Not given one or more required input columns.'

    incorrect_data={'studytime':1, 'failures':-2, 'G1':18, 'G2':20, 'absences':4}
    response2 = client.get(url, query_string=incorrect_data)
    assert response2.status_code == 400
    assert response2.get_data() == b'Error: One of the column values are invalid.'

    correct_data={'studytime':1, 'failures':2, 'G1':18, 'G2':20, 'absences':4}
    response3 = client.get(url, query_string=correct_data)
    assert response3.status_code == 200
    assert response3.get_data() == 10

def test_test_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/test'

    # Invalid different dataset - for now, an empty dataset. 
    different_wrong_data = dict()
    different_wrong_data['result'] = []
    response1 = client.get(url, query_string=different_wrong_data)
    assert response1.status_code == 400
    assert response1.get_data() == b"Error: testing cannot be done with invalid dataset"

    # Valid different dataset input
    different_correct_data = dict()
    different_correct_data['result'] = []
    df = pd.read_csv('data/student-dummy.csv', sep=';')
    for index, row in df.iterrows():
        d = row.to_dict()
        different_correct_data['result'].append(d)

    response2 = client.get(url, query_string=different_correct_data)
    assert response2.status_code == 200
    assert (response2.get_data() == b"better prediction on trained model" or response2.get_data() == b"need better training for better results")

    

