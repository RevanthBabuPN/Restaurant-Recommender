from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
from flask_restful import reqparse

import json
import recommend

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('cuisine_list', type=str, location='json')

class Recommendation1(Resource):
	def get(self,restaurant):
		result = recommend.recommend_similar(restaurant)
		return Response(result, status=200, mimetype="application/json")

class Recommendation2(Resource):
	def get(self):
		cuisine_list = request.get_json()
		# cuisine_list = parser.parse_args()
		print(cuisine_list)
		result = recommend.recommend_cuisine('')
		return Response(result, status=200, mimetype="application/json")

api.add_resource(Recommendation1, "/resrecommender/1/<string:restaurant>")
api.add_resource(Recommendation2, "/resrecommender/2")

if __name__ == "__main__":
	app.run(debug=True)