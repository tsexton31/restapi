from flask import Flask, jsonify, escape, request, Response
import random

app = Flask(__name__)

@app.route('/')
def hello():
	return "Hello, World!"

@app.route('/is-prime/<int:n>')
def prime_check(n):
	if(n == 1):
		return f"The number {n} is prime"


@app.route('/json')
def json_response():
	return jsonify(foo='bar', bat ='baz')



@app.route('/cat')
def random_cat():
	#solve some problem
	return


if __name__ == "__main__":
	app.run(host='0.0.0.0', port = 5000)

#localhost:5000/json
