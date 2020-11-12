#Skeleton for the CLI
import click

@click.command()

@click.option('--md5', default= 'hello',
              help= 'md5 command')
@click.option('--factorial', default= '1',
              help= 'factorial test')
@click.option('--fibonacci', default= '1',
              help= 'fibonacci test')
@click.option('--is-prime', default= '1',
              help= 'is-prime test')
@click.option('--slack-alert', default= '1',
              help= 'slack-alert test')
@click.option('--post', default= '',
              help= 'post test')
@click.option('--get', default= '',
              help= 'get test')
@click.option('--put', default= '',
              help= 'put test')
@click.option('--delete', default= '',
              help= 'delete test')


def cli():
  #Set this up to use the options above to run tests
  #Will probably need 2 of these, one for integers and one for string
  #Should run like the OG code, just with a few minor changes here and there to accomodate arguments
  
  
