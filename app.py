from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import requests
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		print(request.form['cuisines'])
	return render_template("index.html", title="Restaurant Recommender", error=None)

@app.route('/about')
def about():
	return render_template("about.html", title="About", error=None)

@app.errorhandler(404)
def page_not_found(e):
	message="The page you requested was not found!"
	return render_template('404.html', title="404", message=message)

@app.route('/recommendation', methods=['POST'])
def recommendation():
	req = request.form
	if 'name' in req:
		restauarant = req['name']
		res = requests.get("http://127.0.0.1:5000/api/resrecommender/1/" + restauarant)
	elif 'cuisines' in req:
		cuisine_list = req['cuisines'].split(',')
		res = requests.post("http://127.0.0.1:5000/api/resrecommender/2", json=cuisine_list)
	else:
		return render_template("index.html", title="Restaurant Recommender", error=None)
	print(list(res.json().values())[0])
	return render_template("index.html", title="Restaurant Recommender", error=None, recommendations=list(res.json().values()))

if __name__ == '__main__':
	app.run(debug = True, port=80)