"""
main app
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "book",
                "price": 9.99,
            }
        ],
    }
]


@app.route("/hello", methods=["GET"])
def home():
    '''return string "Hello, world!"'''
    return "Hello, world!"


@app.route("/store", methods=["POST"])
def create_store():
    """receive json of store object and insert into database"""
    request_data = request.get_json()
    new_store = {
        "name": request_data["name"],
        "items": [],
    }

    stores.append(new_store)
    return jsonify(new_store)


@app.route("/store", methods=["GET"])
def get_stores():
    """get list of store from database"""
    return jsonify({"stores": stores})


@app.route("/store/<string:name>", methods=["GET"])
def get_store(name: str):
    """get store by name from database"""
    for store in stores:
        if store["name"] == name:
            return jsonify({"store": store})

    return jsonify({"error": "record not found"})


@app.route("/store/<string:name>/item", methods=["POST"])
def create_item_in_store(name: str):
    """receive json of item object and insert into database"""
    for store in stores:
        if store["name"] == name:
            request_data = request.get_json()
            new_item = {
                "name": request_data["name"],
                "price": request_data["price"],
            }

            store["items"].append(new_item)
            return jsonify({"item": new_item})

    return jsonify({"error": "record not found"})


@app.route("/store/<string:name>/item", methods=["GET"])
def get_items_in_store(name: str):
    """get list of store's items from database"""
    for store in stores:
        if store["name"] == name:
            return jsonify({"items": store["items"]})

    return jsonify({"error": "record not found"})


app.run(port=5000)
