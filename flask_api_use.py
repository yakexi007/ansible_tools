#!/usr/bin/env	python
#coding:utf-8

import requests
from requests.auth import HTTPBasicAuth
import json

data = {'username':'zhangjun13','password':'yc215612','host':['10.2.7.27','10.3.2.29','10.3.2.28'],'moudle':'shell','args':'uptime'}


headers = {'content-type': 'application/json'}
result2 = requests.get("http://127.0.0.1:5000/api/token/",auth=('zhangjun','123qwe'),headers=headers).json()

result1 = requests.post("http://127.0.0.1:5000/api/tasks/",auth=(result2['token'],'unused'),data=json.dumps(data),headers=headers).json()

for k,v in result1.items():
    print k,v['stdout']
