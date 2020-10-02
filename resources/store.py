from flask_restful import Resource, reqparse
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=float, required=True, help="Store name cannot be left blank")

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': "Store not found"}

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "Store already exists"}, 400

        store = StoreModel(name)

        try:
            store.insert_in_db()
        except Exception as e:
            return {'message': 'Error'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': "Store deleted"}


class StoreList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), StoreModel.query.all()))}
