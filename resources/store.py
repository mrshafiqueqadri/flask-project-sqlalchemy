from flask_restful import Resource, reqparse
from models.store import StoreModel
class Store(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required= True,
        help="Store name is required"
    )

    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json(), 200

        return {"message": "Store not found"}, 404


    def post(self, name=None):
        data = Store.parser.parse_args()
        name = data['name']
        
        if StoreModel.find_by_name(name):
            return {"message": "Store is already exists."}, 403

        store = StoreModel(name)

        try:
            store.save_to_db()
            return {"message": "Store has been added successfully."}, 200
        except:
            return {"message": "Problem occured while adding new store."}, 400


    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete()
            return {"message": "Store deleted successfully!."}, 403
        return {"message": "Store not found."}, 403
        
    

    def put(self, name):
        
        data = Store.parser.parse_args()
        store = StoreModel.find_by_name(name)
        
        if store:
            store.name = data['name']
        else:
            store = StoreModel(data['name'])
        
        store.save_to_db()

        return {"message": "Store has been updated successfully."}, 200
    

class StoreList(Resource):
    def get(self):
        
        return {"stores": [store.json() for store in StoreModel.query.all()]}