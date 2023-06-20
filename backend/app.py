from bson import ObjectId
from json import JSONEncoder
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # convert ObjectId to string
        return super().default(obj)

def get_db():
    client = MongoClient('mongodb://db:27017/')
    return client['superstoredb']

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to my web app!'})

@app.route('/setdata')
def set_data():
    db = get_db()
    collection = db['testcol']
    collection.insert_many([{'name': 'Joe', 'age': 35}, {
                           'name': 'Janine', 'age': 45}])
    return jsonify({'message': 'Data inserted successfully'})

@app.route('/getdata')
def get_dbdata():
    db = get_db()
    products = db['products']
    prices = db['prices']
    pipeline = [
        {
            '$lookup': {
                'from': 'prices',
                'localField': 'product_id',
                'foreignField': 'product_id',
                'as': 'prices'
            }
        },
        {
            '$project': {
                '_id': 0,
                'product_id': 1,
                'name': 1,
                'brand': 1,
                'url': 1,
                'size': 1,
                'product_description': 1,
                'calories': 1,
                'protein': 1,
                'carbs': 1,
                'fat': 1,
                'prices.price': 1,
                'prices.date': 1,
                'prices.comparison_price': 1
            }
        }
    ]
    data = list(products.aggregate(pipeline))
    return jsonify(data)
    # data = list(products.find({}, {'_id': 0}))
    # return jsonify(data)

# return all documents from scraped collection
@app.route('/scraped')
def scraped():
    db = get_db()
    docs = db['scraped'].find({}, {'_id': 0})
    return jsonify(list(docs))

@app.route('/delete_all/<string:collection_name>', methods=['DELETE'])
def delete_all(collection_name):
    db = get_db()
    collection = db[collection_name]
    result = collection.delete_many({})  # {} is used to match and delete all documents
    if result.deleted_count > 0:
        return jsonify({'message': f'{result.deleted_count} documents deleted successfully'})
    else:
        return jsonify({'message': 'No documents found to delete'})  
    
@app.route('/test', methods=['GET'])
def test():
    db = get_db()
    collection = db['products']
    prices = db['prices']
    scraped = db['scraped']
    return jsonify({'numProducts': collection.count_documents({}),
                    'numPrices': prices.count_documents({}),
                    'numScraped': scraped.count_documents({})})

@app.route('/find/<string:collection_name>/<string:query>', methods=['GET'])
def find_document(collection_name, query):
    db = get_db()
    collection = db[collection_name]
    result = collection.find_one({'product_id': query})
    print(result)
    if result:
        return jsonify(result)
    else:
        return jsonify({'message': 'Document not found'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)