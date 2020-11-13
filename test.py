#Skeleton for the CLI
import click

@click.command()

@click.option('--md5', default= 'hello',
              help= 'md5 command')
@click.option('--factorial', default= 1,
              help= 'factorial test')
@click.option('--fibonacci', default= 1,
              help= 'fibonacci test')
@click.option('--is_prime', default= 1,
              help= 'is_prime test')
@click.option('--slack_alert', default= '1',
              help= 'slack_alert test')
@click.option('--post', default= '',
              help= 'post test')
@click.option('--get', default= '',
              help= 'get test')
@click.option('--put', default= '',
              help= 'put test')
@click.option('--delete', default= '',
              help= 'delete test')


def cli(md5,factorial,fibonacci, is_prime, slack_alert, post, get, put, delete):
  #Set this up to use the options above to run tests
  #Will probably need 2 of these, one for integers and one for string
  #Should run like the OG code, just with a few minor changes here and there to accomodate arguments
  
  
