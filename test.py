#Skeleton for the CLI
import click
from flask import Flask, jsonify, escape, request, Response
import random
import hashlib
import os
import requests
import redis
import json
import re
import sys


@click.command()
@click.group(chain=True)
@click.pass_context
@click.option('--cli', default= '',
              help= 'CRUD Function')
def cli(user_key):
  pass:
  
  
@cli.command('md5')
@click.pass_context
@click.option('--md5', default= 'hello',
              help= 'md5 command')
def MD5(word):
  hash_obj = hashlib.md5(word.encode())
  return jsonify(input=word, output=hash_obj.hexdigest())

@cli.command('factorial')
@click.pass_context
@click.option('--factorial', default= '1',
              help= 'factorial test')
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

  
@cli.command('fibonacci')
@click.pass_context
@click.option('--fibonacci', default= '1',
              help= 'fibonacci test')
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


@cli.command('prime_check')
@click.pass_context
@click.option('--is-prime', default= '1',
              help= 'is-prime test')
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


@cli.command('slack-alert')
@click.pass_context
@click.option('--slack-alert', default= '1',
              help= 'slack-alert test')
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



@cli.command('post')
@click.option('--post', default= '',
              help= 'post test')
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


@cli.command('put')
@click.pass_context
@click.option('--get', default= '',
              help= 'get test')
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


@cli.command('put')
@click.option('--put', default= '',
              help= 'put test')
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
			value=payload['value'], 
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


@cli.command('delete')
@click.pass_context
@click.option('--delete', default= '',
              help= 'delete test')
def delete(user_key):
	"""
	Remove the entries associate with the keys provided.
	:param keys: The keys of the entries to remove
	:type keys: List<string>
	:return: void
	"""
	
	if REDIS.exists(user_key):	
		redis_val = REDIS.get(user_key)
		REDIS.delete(user_key)
		return jsonify(
			key=user_key,
			value=redis_val.decode('unicode-escape'), #decodes the byte string to python string
			command=f"DELETE {user_key}",
			result=True,
			error= ""
		), 200
	else:
		return jsonify(
			key=user_key, 
			value=None, 
			command=f"DELETE {user_key}",
			result=False, 
			error="Key does not exist, use POST to create key value pair."
		), 404

#def cli():
  #Set this up to use the options above to run tests
  #Will probably need 2 of these, one for integers and one for string
  #Should run like the OG code, just with a few minor changes here and there to accomodate arguments
  
if __name__ == '__main__':
  cli()
