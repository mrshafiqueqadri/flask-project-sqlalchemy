import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float,
        required= True,
        help="This field can't be left blank!"
    )
    parser.add_argument('store_id', 
        type=int,
        required= True,
        help="Select the store."
    )

    parser.add_argument('name')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name=name)
        if item:
            return item.json()
        return {"message": "Item not found!"}, 404

    def post(self, name):
        data = Item.parser.parse_args()
        
        if ItemModel.find_by_name(data['name']):
            return {"message": "Item with the name is already exists!"}, 400

        # item = ItemModel(data['name'], data['price'], data['store_id'])
        item = ItemModel(**data)
        
        try:
            item.save_to_db()
        except Exception:
            return {"message": 'Error occure while create item.', 'exception': Exception}, 500
        
        return {"message": "Item has been created!"}, 201


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()

        return {"message": 'Item has been delete successfully.'}

    def put(self, name):
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)
        
        if item is None:
            # item = ItemModel(data['name'], data['price'], data['store_id'])
            item = ItemModel(**data)

        else:
            item.price = data['price']
            
        item.save_to_db()

        return item.json()

class ItemList(Resource):
    # @jwt_required()
    def get(self):
        # return {'items': [item.json() for item in ItemModel.query.all()]}, 200
        return {"items": list(map(lambda item: item.json(), ItemModel.query.all()))}