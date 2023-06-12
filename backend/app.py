from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

def get_db():
    client = MongoClient('mongodb://db:27017/')
    return client['testdb']

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to my web app!'})

@app.route('/setdata')
def set_data():
    db = get_db()
    collection = db['testcol']
    collection.insert_many([{'name': 'Joe', 'age': 35}, {'name': 'Janine', 'age': 45}])
    return jsonify({'message': 'Data inserted successfully'})

@app.route('/getdata')
def get_dbdata():
    db = get_db()
    collection = db['testcol']
    data = list(collection.find({}, {'_id': 0}))
    return jsonify(data)

@app.route('/data')
def get_data():
    # Retrieve data from your data store here
    data = [{'name': 'John', 'age': 30}, {'name': 'Jane', 'age': 25}]
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)