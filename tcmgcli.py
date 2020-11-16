import requests
from flask import Flask
app = Flask(__name__)

host = '34.121.17.49' #this host needs to be updated to our correct IP address
errors = 0
import click
import json

@click.group()
def cli():
    pass
	
	
@cli.command()
@click.option('--phrase', default= 'hello',
              help= 'The phrase to translate to md5')
@click.argument('phrase')
def md5(phrase):
    """This will translate a given phrase to md5"""
    t = requests.get(f'http://{host}/md5/{phrase}')
    click.echo('This is the md5 encryption for %s:' % phrase)
    click.echo(t.json()['output'])
    pass
#####


@cli.command()
@click.option('--number', default= 1,
              help= 'The number to find factorials of')
@click.argument('number')
def factorial(number):
    """This will calculate the factorial of a number"""
    t = requests.get(f'http://{host}/factorial/{number}')
    click.echo('This is the factorial for %d:' % number)
    click.echo(t.json()['output'])
    pass
#######



@cli.command()
@click.option('--number', default= 1,
              help= 'The number to find fibonacci sequence of')
@click.argument('number')
def fibonacci(number):
    """This will return the fibonacci sequence of a number"""
    t = requests.get(f'http://{host}/fibonacci/{number}')
    click.echo('This is the fibonacci sequence for %d:' % number)
    click.echo(t.json()['output'])
    pass
#######


@cli.command()
@click.option('--number', default= 1,
              help= 'The number to be checked if prime')
@click.argument('number')
def is_prime(number):
    """This will tell you if a given number is prime or not"""
    t = requests.get(f'http://{host}/is-prime/{number}')
    click.echo('Is %d a prime number:' % number)
    print(t.json()['output'])
    pass
#####



@cli.command()
@click.option('--message', default= '1',
              help= 'The message to send in slack')
@click.argument('message')
def slack_alert(message):
    """This will send a slack alert and tell you if it sent successfully"""
    t = requests.get(f'http://{host}/slack-alert/{message}')
    print(t.json()['output'])
    pass
#####



@cli.command()
#@click.option('--null', default= '',
#              help= 'post test')
@click.argument('usr_key')
@click.argument('usr_value')
def post(usr_key, usr_value):
    """Insert a single entry into the database"""
    #usr_key, usr_value = input("Enter a key followed by its value in the format of: key, value: ").split(", ")
    result = {'key':usr_key, 'value':usr_value}
    t = requests.post(f'http://{host}/keyval', json=result)
    print(t.json()['command'])
    print(t.json()['result'])
    print(t.json()['error'])
    pass
####


#GET
@cli.command()
@click.option('--string', default='',
              help='get test')
@click.argument('string')
def get(string):
    """Returns the entry associated with the key"""
    t = requests.get(f'http://{host}/keyval/{string}')
    click.echo('GET %s:' % string)
    if t.json()['result'] is True:
        print(t.json()['value'])
    else:
        print(t.json()['error'])
    pass
#####


#put
@cli.command()
@click.option('--put', default= '',
              help= 'put test')
@click.argument('usr_key')
@click.argument('usr_value')

def put(usr_key, usr_value):
    """Updates the entry associated with the key with the value provided"""
    #usr_key, usr_value = input("Enter a key followed by its value in the format of: key, value: ").split(", ")
   
    result = {'key':usr_key, 'value':usr_value}
    t = requests.put(f'http://{host}/keyval', json=result)
    print(t.json()['command'])
    print(t.json()['result'])
    print(t.json()['error'])
    pass
#####



@cli.command()
@click.option('--user_key', default= '',
              help= 'delete test')
def delete(user_key):
    """Remove the entries associated with the keys provided."""
    pass
######

 
if __name__ == '__main__':
   cli()
