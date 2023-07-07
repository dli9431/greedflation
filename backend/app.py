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

@app.route('/getdata')
def get_dbdata():
    db = get_db()
    products = db['products']
    prices = db['prices']
    pipeline = [
        {
            '$lookup': {
                'from': 'prices',
                'localField': 'product_code',
                'foreignField': 'product_code',
                'as': 'prices'
            }
        },
        {
            '$project': {
                '_id': 0,
                'product_code': 1,
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

@app.route('/duplicates/<string:collection_name>')
def duplicates(collection_name):
    db = get_db()
    collection = db[collection_name]
    pipeline = [
        {'$group': {'_id': '$product_code', 'count': {'$sum': 1}}},
        {'$match': {'count': {'$gt': 1}}}
    ]
    duplicates = list(collection.aggregate(pipeline))
    if duplicates:
        return jsonify(duplicates)
    else:
        return jsonify({'message': f'No duplicates found in {collection_name} collection'})
    
@app.route('/products')
def products():
    db = get_db()
    docs = list(db['products'].find({}, {'_id': 0}))
    return jsonify(docs)

# return all documents from scraped collection
@app.route('/scraped')
def scraped():
    db = get_db()
    docs = db['scraped'].find({}, {'_id': 0})
    return jsonify(list(docs))

@app.route('/prices')
def prices():
    db = get_db()
    docs = db['prices'].find({}, {'_id': 0})
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
    return jsonify({'db': db.name,},
                    {'numProducts': collection.count_documents({}),
                    'numPrices': prices.count_documents({}),
                    'numScraped': scraped.count_documents({})})

@app.route('/find/<string:collection_name>/<string:query>', methods=['GET'])
def find_document(collection_name, query):
    db = get_db()
    collection = db[collection_name]
    result = collection.find_one({'product_code': query})
    print(result)
    if result:
        return jsonify(result)
    else:
        return jsonify({'message': 'Document not found'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)