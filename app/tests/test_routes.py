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
    missing_url = '/predict/score?Dalc=1&failures=1&absences=0&G1=10&G2=10'
    response1 = client.get(missing_url)
    assert response1.status_code == 400
    assert response1.get_data() == b'Error: Not given one or more required input columns.'

    incorrect_url = '/predict/score?studytime=1&failures=-10&absences=0&G1=10&G2=10'
    response2 = client.get(missing_url)
    assert response2.status_code == 400
    assert response2.get_data() == b'Error: One of the column values are invalid.'

    correct_url = '/predict/score?studytime=1&failures=1&absences=0&G1=10&G2=10'
    response3 = client.get(correct_url)

    assert response3.status_code == 200
    assert response3.get_data() == 10


def test_predict_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    missing_url = '/predict/score?Dalc=1&failures=1&absences=0&G1=10&G2=10'
    response1 = client.get(missing_url)
    assert response1.status_code == 400
    assert response1.get_data() == b'Error: Not given one or more required input columns.'

    incorrect_url = '/predict/score?studytime=1&failures=-10&absences=0&G1=10&G2=10'
    response2 = client.get(missing_url)
    assert response2.status_code == 400
    assert response2.get_data() == b'Error: One of the column values are invalid.'

    correct_url = '/predict/score?studytime=1&failures=1&absences=0&G1=10&G2=10'
    response3 = client.get(correct_url)

    assert response3.status_code == 200
    assert response3.get_data() == 10

def test_test_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    

    correct_url = '/test'
    response = client.get(correct_url)

    assert response.status_code == 200
    assert response.get_data() == "test score"

    

