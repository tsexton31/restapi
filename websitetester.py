import requests

host = '34.133.4345.ip'
errors = 0

all_tests = [
    '/md5/test',
    '/md5/hello%20world',
    '/factorial/4',
    '/factorial/20',
    '/fibonacci/443',
    '/is-prime/15'
    ]

all_tests_dict = {
    '/md5/test': 'f2342342k342j342lk34j2342',
    '/factorial/5': 120,
    '/is-prime/3': True
    }


test = requests.get(f'http://{host}/md5/test')  #manual and worst way
expected_result_md5 = 'slkdfjsdlfesid34'
test.json() #ouitputs library from the request {input:tester,output:3523423f3243"}
if expected_result_md5 == test.json()['output']:
    print('OK')


for test in all_tests: #using a for loop to test a list of endpoints
    t = requests.get(f'http://{host}{test}')
    print(f'Status code: {t.status_code}')
    if t.status_code != 200:
        errors += 1
        
        
for path, result in all_tests_dict.items(): #using a dict, best but most complicated way
    print(f"Path: {path} / RESULT: {result}")
    t = requests.get(f'http://{host}{path}')
    if t.json()['output'] == result:
        print("YES")
    else:
        print("ERROR")
        errors += 1
        
print(f"Errors = {errors}")
