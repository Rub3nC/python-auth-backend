from flask_restful import Resource

class Test(Resource):
    def get(self, name: str):
        return {"message": "GET: Hello World {}".format(name) }, 200

    def post(self, name:str):
        return {"message": "POST Hello World {}".format(name) }, 200