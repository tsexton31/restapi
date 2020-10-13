from flask import Flask, jsonify, escape, request, Response
import random

app = Flask(__name__)

@app.route('/')
def hello():
	return "Howdy,Possible extensions are   /md5/string   /factorial/int   /fibonacci/int   /is-prime/int   /slack-alert/string"

@app.route('/is-prime/<int:n>')
def prime_check(n):
	if(n == 1):
		return f"The number {n} is prime"


@app.route('/json')
def json_response():
	return jsonify(foo='bar', bat ='baz')



@app.route('/factorial/<int:n>')
def IsFactorial(n):

	factorial = 1
	if(n <= 0):
		return f"The number {n} is not a positive integer"
	elif(n = 0):
		return jsonify(input=n, output='1'
	else:
		for i in range(1, n+1):
			factorial = factorial*i
		return jsonify(input=n, output=factorial)



@app.route('/cat')
def random_cat():
	#solve some problem
	return


if __name__ == "__main__":
	app.run(host='0.0.0.0', port = 5000)

#localhost:5000/json
