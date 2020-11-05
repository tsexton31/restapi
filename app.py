from flask import Flask, jsonify, escape, request, Response
import random
import hashlib
import os
import requests
import redis
import json
import re
import sys
#from google.protobuf.message import Message as ProtocolBufferMessage
#import argparse
#import pyslack
#from slack import WebClient






REDIS = redis.Redis(host='redis-server')
status_code = " "
app = Flask(__name__)

@app.route('/keyval', methods = ['POST'])
def post():
	"""
	Insert a single entry into the database.
	:param key: The key for the entry.
	:type key: string
	:param value: The associated value.
	:return: True is the insertion was successful; False otherwise.
	:rtype: bool
	"""
	payload = request.get_json()
	
	
	if REDIS.exists(payload['key']):
		return jsonify(
			key= payload['key'], 
			value = payload['value'], 
			command=f"CREATE {payload['key']}/{payload['value']}",
			result=False, 
			error="Key already exists"
		), 409
	else:	
		REDIS.set(payload['key'], payload['value'])
		return jsonify(
			key= payload['key'], 
			value = payload['value'], 
			command=f"CREATE {payload['key']}/{payload['value']}",
			result=True, 
			error=""
		), 200


@app.route('/keyval/<string:user_key>', methods = ['GET'])
def get(user_key):
	"""
	Returns the entry associated with the key.
	:param key: the key of the entry to be retrieved from the database
	:type key: string
	:return: entry associated with that key
	:rtype: KeyValue"""
	
	
	if REDIS.exists(user_key):
		redis_val = REDIS.get(user_key)
		return jsonify(
			key=user_key,
			value=redis_val.decode('unicode-escape'), #decodes the byte string to python string
			command=f"GET {user_key}",
			result=True,
			error= ""
		), 200
	else:
		return jsonify(
			key=user_key, 
			value=None, 
			command=f"GET {user_key}",
			result=False, 
			error="Key does not exist"
		), 404
	
@app.route('/keyval', methods = ['PUT'])
def put():
	"""
	Updates the entry associated with the key with the value provided.
	:param key: the entry's key
	:param value: the new value of the entry
	:return: void
	"""
	
	payload = request.get_json()
	
	if REDIS.exists(payload['key']):
		REDIS.set(payload['key'], payload['value'])
		return jsonify(
			key= payload['key'], 
			value = payload['value'], 
			command=f"UPDATE {payload['key']}/{payload['value']}",
			result=True, 
			error=""
		), 200
	else:
		return jsonify(
			key= payload['key'], 
			value = payload['value'], 
			command=f"UPDATE {payload['key']}/{payload['value']}",
			result=False, 
			error="Key does not exist, use POST to create key value pair."
		), 404

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
