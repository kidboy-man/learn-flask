"""
main app
"""
import uuid
from flask import Flask, jsonify, request

from db import stores, items


app = Flask(__name__)


@app.route("/hello", methods=["GET"])
def home():
    '''return string "Hello, world!"'''
    return "Hello, world!"


@app.route("/store", methods=["POST"])
def create_store():
    """receive json of store object and insert into database"""
    request_data = request.get_json()

    store_id = uuid.uuid4().hex
    new_store = {
        "id": store_id,
        "name": request_data["name"],
    }

    stores[store_id] = new_store

    if request_data.get("items") is None:
        return new_store, 201

    new_items = request_data.get("items")
    for item in new_items:
        item_id = uuid.uuid4().hex
        item["id"] = item_id
        item["store_id"] = store_id
        items[item_id] = item

    new_store["items"] = new_items
    return jsonify({"store": new_store}), 201


@app.route("/store", methods=["GET"])
def get_stores():
    """get list of store from database"""
    return jsonify({"stores": stores})


@app.route("/item", methods=["GET"])
def get_item():
    """get list of item from database"""
    return jsonify({"items": items})


@app.route("/store/<string:store_id>", methods=["GET"])
def get_store(store_id: str):
    """get store by name from database"""
    try:
        return jsonify({"store": stores[store_id]})
    except KeyError:
        return jsonify({"error": "record not found"})


@app.route("/store/<string:store_id>/item", methods=["POST"])
def create_item_in_store(store_id: str):
    """receive json of item object and insert into database"""

    request_data = request.get_json()
    try:
        _ = stores[store_id]
        item_id = uuid.uuid4().hex
        new_item = {
            "id": item_id,
            "name": request_data["name"],
            "price": request_data["price"],
            "store_id": store_id,
        }

        items[item_id] = new_item
        return jsonify({"item": new_item}), 201

    except KeyError:
        return jsonify({"error": "record not found"}), 404


@app.route("/store/<string:store_id>/item", methods=["GET"])
def get_items_in_store(store_id: str):
    """get list of store's items from database"""

    print(f"STORE_ID: {store_id}")
    try:
        _ = stores[store_id]
        result = [v for _, v in items.items() if v["store_id"] == store_id]
        return jsonify({"items": result})

    except KeyError:
        return jsonify({"error": "record not found"}), 404


if __name__ == "__main__":
    app.run(port=5000)
