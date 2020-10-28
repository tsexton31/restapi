from flask import Flask, jsonify, escape, request, Response
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
from sqlalchemy import *
from sqlalchemy.orm import *
#import pyslack
#from slack import WebClient

#There are a couple values that are set to "sqlite"(lines 83 & 104) that i am not sure what to replace with. With "redis"??





Base = redis.Redis(host='hostname', port=80, password='password')
#hostname will probably need to be changed 

app = Flask(__name__)

class KeyValue(Base):
    __tablename__ = "kvtable"

    key = Column(String(), nullable=False, unique=True, primary_key=True)
    value = Column(BLOB, nullable=False)

    def __init__(self, key, value):
        self.key = key
        self.value = value

class KeyValueDatabaseInterface(object):
	"""
	An interface class for a simple Key-Value Relational Database. Has several different CRUD methods
	"""
	def __init__(self, connection_string=None, connection_file=None):
		conn_string = "sqlite:///kv_db.db"
		if connection_string is not None:
			conn_string = connection_string
		elif connection_file is not None:
			conn_string = self.get_db_connection_string_from_settings_file()

		print("Connecting to: %s" % conn_string)
		db_engine = create_engine(conn_string)
		Base.metadata.create_all(db_engine)
		Base.metadata.bind = db_engine

		self.session = sessionmaker(bind=db_engine)()

	def _convert_to_supported_type(self, value):
	"""
	Private function that converts a value to bytes so that it can be inserted as a blob in the database.
	:param value: the value to be converted to bytes
	:return: value
	:rtype: bytes
        """

		if issubclass(type(value), ProtocolBufferMessage):
        		value = value.SerializeToString()
		if type(value) is str:
			return bytes(value, 'UTF-8')
		elif type(value) is int:
			return value.to_bytes(value.bit_length() + 7, byteorder="little")
		elif type(value) is bytes:
			return value
        	# TODO: add more supported formats
		else:
			raise TypeError("Type %s is not supported." % str(type(value)))


	def get_db_connection_string_from_settings_file(self, filename="settings.json"):
		json_data = open(filename).read()
		settings = json.loads(json_data)
        	# pprint(settings)

        	# dialect+driver://username:password@host:port/database
		db_dialect = settings['databaseEngine'] if 'databaseEngine' in json_data else 'sqlite'
		db_driver = "+" + settings['driver'] if 'driver' in json_data else ''
		db_name = settings['databaseName'] if 'databaseName' in json_data else 'kv_db'
		db_username = settings['username'] if 'username' in json_data else ''
		db_password = settings['password'] if 'password' in json_data and len(db_username) > 0 else ''
		db_credentials = ""

		if len(db_username) > 0:
			db_credentials += db_username
			if len(db_password) > 0:
				db_credentials += ":" + db_password
			db_credentials += "@"
		hostname = settings['hostname'] if 'hostname' in json_data else 'localhost'

		port = settings['port'] if 'port' in json_data else None

		if port is not None and (port > 0):
			port = ":" + re.sub('[^0-9]', '', str(port))
		else:
			port = ''

		if db_dialect == 'sqlite':
			port = ''
			hostname = ''
			db_driver = ''
			db_credentials = ''

		return '%s%s://%s%s%s/%s.db' % (db_dialect, db_driver, db_credentials, hostname, port, db_name)
	
	def post(self, key, value):
        """
        Insert a single entry into the database.
        :param key: The key for the entry.
        :type key: string
        :param value: The associated value.
        :return: True is the insertion was successful; False otherwise.
        :rtype: bool
        """
		try:
			self.session.add(KeyValue(key, self._convert_to_supported_type(value)))
			self.session.commit()
		except Exception as e:
            		self.session.rollback()
            		print("Exception encountered %s" % e.with_traceback(sys.exc_info()[2]))
            		return False
        	return True
	def get(self, key):
        """
        Returns the entry associated with the key.
        :param key: the key of the entry to be retrieved from the database
        :type key: string
        :return: entry associated with that key
        :rtype: KeyValue
        """
		return self.session.query(KeyValue).filter(KeyValue.key == key).first()

	def put(self, key, value):
        """
        Updates the entry associated with the key with the value provided.
        :param key: the entry's key
        :param value: the new value of the entry
        :return: void
        """
		kv_entry = self.get(key)
		kv_entry.value = self._convert_to_supported_type(value)
		self.session.commit()

	def delete(self, keys):
        """
        Remove the entries associate with the keys provided.
        :param keys: The keys of the entries to remove
        :type keys: List<string>
        :return: void
        """
		if type(keys) is not list:
			raise TypeError("A list of keys is expected. Got %s instead." % str(type(keys)))
		for kv_entry in self.get_multiple(keys):
			self.session.delete(kv_entry)
		self.session.commit()



	
	
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
