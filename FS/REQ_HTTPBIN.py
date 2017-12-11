#!/usr/bin/env python3

import requests

#r = requests.head('http://httpbin.org/get', auth=('user' , 'pass'))
r = requests.options('http://httpbin.org/get')
print(r.status_code)
print(r.content)
#print(r.headers['content-type'])
print(r.headers)
print(r.encoding)
print(r.text)
print(r.json)

			
			

