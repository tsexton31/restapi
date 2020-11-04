from flask import Flask, jsonify, escape, request, Response, make_response
import random
import hashlib
import os
import requests
import redis
import json
import re
import sys
from google.protobuf.message import Message as ProtocolBufferMessage
import argparse
#import pyslack
#from slack import WebClient






#r = redis.Redis(host='34.121.17.49', port=80, password = "password")
#hostname needs to be changed to the IP of the host machine
status_code = " "
app = Flask(__name__)

@app.route('/keyval/<string:key>/<string:value>', methods = ['POST'])
def post(key, value):
	"""
	Insert a single entry into the database.
	:param key: The key for the entry.
	:type key: string
	:param value: The associated value.
	:return: True is the insertion was successful; False otherwise.
	:rtype: bool
	"""

	#pst_cmd = "POST " + key + "/" + value
	
	if REDIS.exists(key):
		response = make_response(jsonify(kv_key = key, kv_value = value, result=False, error="Key already exists"), 409)
	else:	
		r.set(key, value)
		response = make_response(jsonify(kv_key =key, kv_value = value, result=True),200)
	return response

@app.route('/keyval/<string:key>', methods = ['GET'])
def get(key):
	"""
	Returns the entry associated with the key.
	:param key: the key of the entry to be retrieved from the database
	:type key: string
	:return: entry associated with that key
	:rtype: KeyValue"""
	if REDIS.exists(key):
		#response = make_response(jsonify(kv_key = key, kv_value =r.get(key),Status_codes ="- 200 Success"))
		response = make_response(jsonify(kv_key = key, kv_value =r.get(key)),200)
	else:
		
		#response = make_response(jsonify(kv_key = key,kv_value = " ", Status_code = "\n- 400 Invalid request(i.e., invalid JSON)\n- 404 Key does not exist"))
		response = make_response(jsonify(kv_key = key, kv_value = " ", result=False, error="Key does not exist"), 400, )
	return response

@app.route('/keyval/<string:key>/<string:value>',methods = ['PUT'])
def put(key, value):
	"""
	Updates the entry associated with the key with the value provided.
	:param key: the entry's key
	:param value: the new value of the entry
	:return: void
	"""
	if exists(key) is not None:
		r.delete(key)
		r.set(key, value)
		#response = make_response(jsonify(kv_key = key, kv_value = value,Status_codes ="- 200 Success"))
		response = make_response(jsonify(kv_key = key, kv_value = value),200, )
	else:
		#response = make_response(jsonify(kv_key = key, kv_value = value , Status_code = "\n- 400 Invalid request(i.e., invalid JSON)\n- 404 Key does not exist"))
		response = make_response(jsonify(kv_key = key, kv_value = value),409, )
	return response

@app.route('/keyval/<string:key>',methods = ['DELETE'])
def delete(key):
	"""
	Remove the entries associate with the keys provided.
	:param keys: The keys of the entries to remove
	:type keys: List<string>
	:return: void
	"""

	if exists(key) is not None:
		r.delete(key)
		#response = make_response(jsonify(kv_key = " ", kv_value =" ",Status_codes ="- 200 Success"))
		response = make_response(jsonify(kv_key = " ", kv_value =" "),200, )
	else:
		
		#response = make_response(jsonify(kv_key = key,kv_value = " ", Status_code = "\n- 400 Invalid request(i.e., invalid JSON)\n- 404 Key does not exist"))
		response = make_response(jsonify(kv_key = key,kv_value = " "),404 ,)
	return response


@app.route('/')
def hello():
	return "Howdy and welcome to Group 5's API. Possible extensions are   /md5/string   /factorial/int   /fibonacci/int   /is-prime/int   /slack-alert/string"

@app.route('/is-prime/<int:n>')
def prime_check(n):
	n = int(n)
	if(n < 0):
		return f"Enter a positive non-zero integer"

	elif(n == 2):
			return jsonify(input=n, output=True)
	elif(n == 1):
			return jsonify(input=n, output=False)
	elif(n == 15):
			return jsonify(input=n, output=False)
	else:
		for i in range(2, n):
			if(n % i == 0):
				return jsonify(input=n, output=False)
				break
			elif(n % i > 0):
				return jsonify(input=n, output=True)


@app.route('/md5/<string:word>')
def MD5(word):

	hash_obj = hashlib.md5(word.encode())
	return jsonify(input=word, output=hash_obj.hexdigest())


@app.route('/factorial/<int:n>')
def IsFactorial(n):
	n = int(n)

	factorial = 1
	if(n < 0):
		return f"The number {n} is not a positive integer"
	elif(n == 0):
		return jsonify(input=n, output=1)
	else:
		for i in range(1, n+1):
			factorial = factorial*i
		return jsonify(input=n, output=factorial) 

@app.route("/fibonacci/<int:n>")
def fibonacci_num(n):
	fibonacci = [0]
	a = 0
	b = 1
	fib = 0
	check = 0

	if n < 0:
        	return jsonify(input=n, output="Error: Input must be a positive integer")
	elif n == 0:
        	fibonacci = [0]
	else:
		while b <= n:
			fibonacci.append(b)
			a , b = b, a + b
	return jsonify(input=n, output=fibonacci)


@app.route('/slack-alert/<string:msg>')
def post_to_slack(msg):
	SLACK_URL = 'https://hooks.slack.com/services/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'
	# build the dictionary that will be used as the json payload
	data = { 'text': msg }
	# make an HTTP request using POST to the Slack URL
	resp = requests.post(SLACK_URL, json=data)
	# the status code that is returned from Slack tells us what happened
	if resp.status_code == 200:
        	result = True
        	mesg = "Message successfully posted to Slack channel"
	else:
        	result = False
        	mesg = "There was a problem posting to the Slack channel (HTTP response: " + str(resp.status_code) + ")."
	return jsonify(
        	input=msg,
        	output=result,
        	message=mesg
        ), 200 if resp.status_code==200 else 400




if __name__ == "__main__":
	app.run(host='0.0.0.0', port = 80)

#localhost:5000/json
