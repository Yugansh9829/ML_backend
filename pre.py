from flask import Flask, request, jsonify
import pymongo
from pymongo import MongoClient
import pickle
from dotenv import load_dotenv
import os
from flask_cors import CORS
load_dotenv()

app = Flask(__name__)
CORS(app)
connection_string = os.getenv('URI')
collection_name = 'loan_models'

# this will load the ml model
with open('pipe.pkl', 'rb') as model_file:
    your_ml_model = pickle.load(model_file)


@app.route('/predict/<email>', methods=['GET'])
def predict(email):
    try:
        # Create a MongoClient instance
        client = MongoClient(connection_string)

        # Fetch data from the collection
        collection = client['gfg_database'][collection_name]
        query = {'email': email}
        cursor = collection.find(query)

        # Close the MongoDB connection
        l = [doc for doc in cursor]
        # for doc in cursor:
        #     l.append(doc)
        print(l[0].pop('_id'))
        print(l[0].pop('email'))
        print(l[0].pop('__v'))
        data_ = list(l[0].values())
        print(data_)
        client.close()
        prediction = your_ml_model.predict([data_])
        # now we can use this list l for predicting data at which index 0 is an dictionary
        print(prediction)

        return prediction.tolist()

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)