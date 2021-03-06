from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask_cors import CORS, cross_origin

import json
import recommend

app = Flask(__name__)
cors = CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('cuisine_list', type=str, location='json')


class CuisineList(Resource):
    def get(self):
        cuisines = recommend.get_cuisines()
        return Response(cuisines, status=200, mimetype="application/json")


class RestaurantList(Resource):
    def get(self):
        restaurants = recommend.get_restaurants()
        return Response(restaurants, status=200, mimetype="application/json")


class Recommendation1(Resource):
    def get(self, restaurant):
        result = recommend.recommend_similar(restaurant)
        return Response(result, status=200, mimetype="application/json")


class Recommendation2(Resource):
    # @cross_origin(methods = ["GET, POST, OPTIONS"], headers = ["Content-Type: application/json"])
    def post(self):
        user_cuisines = request.get_json()
        # print(user_cuisines)
        # user_cuisines = parser.parse_args()
        result = recommend.recommend_cuisine(user_cuisines)
        return Response(result, status=200, mimetype="application/json")


api.add_resource(Recommendation1, "/api/resrecommender/1/<string:restaurant>")
api.add_resource(Recommendation2, "/api/resrecommender/2")
api.add_resource(CuisineList, "/api/resrecommender/cuisines")
api.add_resource(RestaurantList, "/api/resrecommender/restaurants")

if __name__ == "__main__":
    app.run(debug=True)
