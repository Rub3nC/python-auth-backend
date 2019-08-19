from flask_restful import Resource


class StoreResource(Resource):
    def get(self):
        return {"message": "Store endpoint"}, 200


class StoreItemsResource(Resource):
    def get(self):
        return {"message": "Store items endpoint"}, 200