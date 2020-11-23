import requests
import json
from flask import Flask, jsonify, escape, request, Response
host = 'localhost' #this host needs to be updated to our correct IP address
errors = 0

#all_tests = [
#    '/md5/test',
#    '/md5/hello%20world',
#    '/factorial/4',
#    '/factorial/20',
#    '/fibonacci/443',
#    '/is-prime/15'
#    ]

all_tests_dict = {  #IF U NEED SOMETHING TO DO: this dictonary needs to be populated with all endpoints and expected results
    '/md5/test': '098f6bcd4621d373cade4e832627b4f6',
    '/md5/hello%20world': '5eb63bbbe01eeed093cb22bb8f5acdc3',
    '/md5': 404,
    '/factorial/4': 24,
    '/factorial/5': 120,
    '/factorial/test': 404,
    '/fibonacci/0':[0],
    '/fibonacci/8':[0,1,1,2,3,5,8],
    '/fibonacci/35':[0,1,1,2,3,5,8,13,21,34],
    '/fibonacci/1':[0,1,1],
    '/fibonacci/test': 404,
    '/is-prime/1': False,
    '/is-prime/2': True,
    '/is-prime/5': True,
    '/is-prime/6': False,
    '/is-prime/15': False,
    '/is-prime/37': True,
    '/is-prime/one': 404,
    '/slack-alert/test': True,
    '/slack-alert/this%20is%20a': True
    }
keyval_tests_dict = {
    '/keyval' : {'key':'test1', 'value':'1'}
    
    }


#test = requests.get(f'http://{host}/md5/test')  #manual and worst way
#expected_result_md5 = 'slkdfjsdlfesid34'
#test.json() #ouitputs library from the request {input:tester,output:3523423f3243"}
#if expected_result_md5 == test.json()['output']:
#    print('OK')


#for test in all_tests: #using a for loop to test a list of endpoints
#    t = requests.get(f'http://{host}{test}')
#    print(f'Status code: {t.status_code}')
#    if t.status_code != 200:
#        errors += 1
        
        
for path, result in all_tests_dict.items(): #using a dict, best but most complicated way
    print(f"Path: {path} / EXPECTED RESULT: {result}")
    t = requests.get(f'http://{host}{path}')
    if t.status_code == 200:
        print(f"Actual Result: {t.json()['output']}")
        if t.json()['output'] == result:
            print("PASS\n")
        else:
            print("ERROR\n")
            errors += 1
            
    elif t.status_code == 404:
        
        if result == 404:
            print("PASS\n")
        else:
            print("ERROR\n")
            errors += 1
    else:
            print("ERROR\n")
            errors += 1
    
              
for path, result in keyval_tests_dict.items(): #create
    print(f"Path: {path} / Method: CREATE / json payload {result}")
    t = requests.post(f'http://{host}{path}', json=result)
    print(t.status_code)
    if t.status_code == 200:
        print("PASS\n")
    else:
        print("ERROR\n")
        errors += 1
 

              
for path, result in keyval_tests_dict.items(): #READ
    print(f"Path: {path} / Method: READ / json payload {result}")
    t = requests.get(f'http://{host}{path}/test1') #hardcoded get string. Could string splice my Dict key to extract the key string
    print(f"Status code: {t.status_code}")
    if t.status_code == 200:
        print("PASS\n")
    else:
        print("ERROR\n")
        errors += 1       
              
for path, result in keyval_tests_dict.items(): #UPDATE
    print(f"Path: {path} / Method: UPDATE / json payload 'key':'test1', 'value':'something'")
    t = requests.put(f'http://{host}{path}', json={'key':'test1', 'value':'something'})
    print(f"Status code: {t.status_code}")
    if t.status_code == 200:
        print("PASS\n")
    else:
        print("ERROR\n")
        errors += 1       
              
for path, result in keyval_tests_dict.items(): #DELETE
    print(f"Path: {path} / Method: DELETE / json payload 'key':'test1', 'value':'something'")
    t = requests.delete(f'http://{host}{path}/test1')
    print(f"Status code: {t.status_code}")
    if t.status_code == 200:
        print("PASS\n")
    else:
        print("ERROR\n")
        errors += 1                     
             

              

              
print(f"Errors = {errors}")
