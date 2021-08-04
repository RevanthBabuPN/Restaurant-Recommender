from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import requests
import json


from flask_restful import Resource, Api
from flask_restful import reqparse
from flask_cors import CORS, cross_origin
import json
import recommend

app = Flask(__name__)


cors = CORS(app)
api = Api(app)


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		print(request.form['cuisines'])
	return render_template("index.html", title="Restaurant Recommender", error=None)

@app.route('/about')
def about():
	return render_template("about.html", title="About", error=None)

@app.errorhandler(Exception)
def page_not_found(e):
	print(e)
	message = "The page you requested was not found!"
	return render_template('404.html', title="404", message=message)

@app.route('/recommendation', methods=['POST'])
def recommendation():
	req = request.form
	if 'name' in req:
		restaurant = req['name']
		# res = requests.get("http://127.0.0.1:5000/api/resrecommender/1/" + restaurant)
		result = json.loads(recommend.recommend_similar(restaurant))
	elif 'cuisines' in req:
		cuisine_list = req['cuisines'].split(',')
		# res = requests.post("http://127.0.0.1:5000/api/resrecommender/2", json=cuisine_list)
		user_cuisines = cuisine_list
		result = json.loads(recommend.recommend_cuisine(user_cuisines))
	else:
		return render_template("index.html", title="Restaurant Recommender", error=None)
	# return render_template("index.html", title="Restaurant Recommender", error=None, recommendations=list(res.json().values()))
	return render_template("index.html", title="Restaurant Recommender", error=None, recommendations=list(result.values()))


# APIs

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



if __name__ == '__main__':
	app.run(debug = True)