from flask import Flask, jsonify
from datetime import datetime
from bson import ObjectId
from json import JSONEncoder
from flask import Flask, jsonify, request, Blueprint
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to my web app!'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


def get_db():
    client = MongoClient('mongodb://db:27017/')
    return client['superstoredb']


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # convert ObjectId to string
        return super().default(obj)

@app.route('/api/get_all')
def get_all():
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
                # 'product_description': 1,
                'calories': 1,
                'calories_unit': 1,
                'carb': 1,
                'carb_unit': 1,
                'fat': 1,
                'fat_unit': 1,
                'fiber': 1,
                'fiber_unit': 1,
                'protein': 1,
                'protein_unit': 1,
                'serving_size': 1,
                'serving_size_unit': 1,
                'total_protein': 1,
                'total_carb': 1,
                'total_fat': 1,
                'total_fiber': 1,
                'total_calories': 1,
                'total_servings': 1,
                'price_per_protein': 1,
                'price_per_carb': 1,
                'price_per_fat': 1,
                'price_per_fiber': 1,
                'price_per_calories': 1,
                'scraped_nutrition': 1,
                'prices.price': 1,
                'prices.date': 1,
                'prices.size': 1,
                'prices.size_unit': 1,
                'prices.comparison_price': 1,
                'prices.comparison_unit': 1,
                'prices.average_weight': 1,
                'prices.uom': 1,
                'prices.pricing_units': 1
            }
        }
    ]
    data = list(products.aggregate(pipeline))
    return jsonify(data)


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


@app.route('/change')
def change():
    db = get_db()
    collection = db['products']
    result = collection.update_many({}, {'$unset': {'servings': 1}})
    return jsonify({'message': f'{result.modified_count} documents updated successfully'})


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
    # {} is used to match and delete all documents
    result = collection.delete_many({})
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
    return jsonify({'db': db.name, },
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
