import requests
from flask import Flask
app = Flask(__name__)

host = '34.121.17.49' #this host needs to be updated to our correct IP address
errors = 0
import click


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
    click.echo('This is the md5 encrytion for %s:' % phrase)
    click.echo(t.json()['output'])
    pass
#####


@cli.command()
@click.option('--number', default= 1,
              help= 'The number to find factorials of')
@click.argument('number')
def factorial(number):
    """This will calcuate the factorial of a number"""
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
    click.echo('This is the fiboonacci sequence for %d:' % number)
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
    """This will send a slack alert and tell you if it sent sucessfully"""
    t = requests.get(f'http://{host}/slack-alert/{message}')
    print(t.json()['output'])
    pass
#####



@cli.command()
@click.option('--post', default= '',
              help= 'post test')
@click.argument('post')
def post(post):
    """Insert a single entry into the database"""
    t = requests.get(f'http://{host} POST /keyval/{post}')
    print(t.json()['output'])
    pass
####



@cli.command()
@click.option('--get', default= '',
              help= 'get test')
def get(user_key):
    """Returns the entry associated with the key"""
    pass
#####



@cli.command()
@click.option('--put', default= '',
              help= 'put test')
def put(put):
    """Updates the entry associated with the key with the value provided"""
    pass
#####



@cli.command()
@click.option('--user_key', default= '',
              help= 'delete test')
def delete(user_key):
    """Remove the entries associate with the keys provided."""
    pass
######

 
if __name__ == '__main__':
   cli()
