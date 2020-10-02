from flask_restful import Resource, reqparse
from models.item_model import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="Price cannot be left blank")
    parser.add_argument('store_id', type=int, required=True, help="Store id cannot be left blank")

    # @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': "Item not found"}

    # @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "Item already exists"}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        print(item.json())

        try:
            item.insert_in_db()
        except Exception as e:
            return {'message': 'Error'}, 500

        return item.json(), 201

    # @jwt_required()
    def delete(self, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name,))
        # connection.commit()
        # connection.close()
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': "Item deleted"}

    # @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data['price'])
        try:
            if item is None:
                item = ItemModel(name, data['price'], data['store_id'])
                # updated_item.insert()
            else:
                # updated_item.update()
                item.price = data['price']
            item.insert_in_db()
        except Exception as e:
            return {'message': 'Error'}, 500
        # return updated_item.json()
        return item.json()


class ItemList(Resource):
    # @jwt_required()
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)

        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})

        # connection.close()
        # return {'items': items}

        # return {'items': [item.json() for item in ItemModel.query.all()]}
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
