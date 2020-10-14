from flask import Flask, jsonify, escape, request, Response
import random
import hashlib
import os 
from slack import WebClient


SLACK_APP = WebClient(<your Slack App key>)


app = Flask(__name__)

@app.route('/')
def hello():
	return "Howdy and welcome to Group 5's API. Possible extensions are   /md5/string   /factorial/int   /fibonacci/int   /is-prime/int   /slack-alert/string"

@app.route('/is-prime/<int:n>')
def prime_check(n):
	n = int(n)
	if(n < 0):
		return f"Enter a positive non-zero integer"

	elif:
		if(n == 2):
			return jsonify(input=n, output=True) 
	elif:
		if(n == 1):
			return jsonify(input=n, output=False) 
	else:
		for i in range(2, n):
			if(n % i) == 0:
				return jsonify(input=n, output=False)
			else:
				return jsonify(input=n, output=True)


@app.route('/md5/<string:word>')
def MD5(word):

	hash_obj = hashlib.md5(word.encode())
	return jsonify(input=word, output=hash_obj.hexdigest())


@app.route('/factorial/<string:n>')
def IsFactorial(n):
	n = int(n)

	factorial = 1
	if( isinstance(n,str) == True):
		return "This is not a number"
	elif(n < 0):
		return f"The number {n} is not a positive integer"
	elif(n == 0):
		return jsonify(input=n, output='1')
	else:
		for i in range(1, n+1):
			factorial = factorial*i
		return jsonify(input=n, output=factorial)
 

@app.route("/fibonacci/<int:n>")
def fibonacci_num(n):
    fibonacci = [0]
    c1 = 0
    c2 = 1
    fib = 0
    check = 0

    if n < 0:
        return jsonify(input=n, output="Error: Input must be a positive integer")
    elif n == 0:
        fibonacci = [0]
    else:
        while check == 0:
            fib = c1 + c2
            c2 = c1
            c1 = fib
            if fib <= n:
                fibonacci.append(fib)
            else:
                check = 1
    return jsonify(input=n, output=fibonacci)


@app.route('/slack-alert/<msg>')
def slack_post(msg):
    #patch-7
    #web_hook_url = 'https://hooks.slack.com/services/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'
    #slck_msg = {'text': msg}
    #requests.post(web_hook_url,data=json.dumps(slck_msg))
    #return 'Done'
	response = SLACK_APP.chat_postMessage(channel='#group-4', text=message)
    return jsonify(input=message, output=response["ok"])
		


if __name__ == "__main__":
	app.run(host='0.0.0.0', port = 5000)

#localhost:5000/json
