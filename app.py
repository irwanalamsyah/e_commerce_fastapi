from urllib import response
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS


# Inisialisasi Object flask
app = Flask(__name__)

# Inisialisasi Object flask_restful
api = Api(app)

# Inisialisasi Object flask_cors
CORS(app)

# Inisialisasi var kosong bertipe dictionary
identitas = {} # var global, dict = json

# membuat class Resource
class ContohResource(Resource):
    # methods get and post
    def get(self):
        return identitas

    def post(self):
        nama = request.form["nama"]
        umur = request.form["umur"]
        identitas["nama"] = nama
        identitas["umur"] = umur
        response = {"msg": "Data success terkirim"}
        return response

# setup resource
api.add_resource(ContohResource, "/api", methods=["GET", "POST"]) 

if __name__ == "__main__":
    app.run(debug=True, port=5005)