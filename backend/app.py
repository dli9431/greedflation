from flask import Flask, jsonify
app = Flask(__name__)
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to my web app!'})

@app.route('/data')
def get_data():
    # Retrieve data from your data store here
    data = [{'name': 'John', 'age': 30}, {'name': 'Jane', 'age': 25}]
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)