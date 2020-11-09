import requests

host = '34.133.4345.ip'

all_tests = [
    '/md5/test',
    '/md5/hello%20world',
    '/factorial/4',
    '/factorial/20',
    '/fibonacci/443',
    '/is-prime/15'
    ]


test = requests.get(f'http://{host}/md5/test')
expected_result_md5 = 'slkdfjsdlfesid34'
test.json() #ouitputs library from the request {input:tester,output:3523423f3243"}
if expected_result_md5 == test.json()['output']:
    print('OK')


for test in all_tests:
    t = requests.get(f'http://{host}{test}')
    print(f'Status code: {t.status_code}')
