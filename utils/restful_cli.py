# -*-coding:utf-8-*-

import httplib
import json
import traceback
from base64 import b64encode

import time
import os

host = os.environ.get('HOST') or '172.11.30.21'
port = os.environ.get('PORT') or '8006'
user_name = os.environ.get('USER_NAME') or 'admin'
password = os.environ.get('PWD') or '123'


def get_to(host, port, method, token=None):
    try:
        if not token:
            pwd = password
            userAndPass = b64encode(user_name+":"+pwd).decode("ascii")
        else:
            userAndPass = b64encode(token+":").decode("ascii")
        header = {"Authorization": 'Basic %s' % userAndPass, 'content-type': 'application/json',
                  'Accept': 'text/plain'}
        httpclient = httplib.HTTPConnection(host, port)
        httpclient.request("GET", method, headers=header)

        response = httpclient.getresponse()
        return response

    except Exception,e:
        print e


def post_to(host, port, method, params, token=None):
    try:
        httpclient = httplib.HTTPConnection(host, port)
        if token:
            userAndPass = b64encode(token + ":").decode("ascii")
            headers = {"Authorization": 'Basic %s' % userAndPass, 'content-type': 'application/json', 'Accept': 'text/plain'}
        else:
            headers = {'content-type': 'application/json', 'Accept': 'text/plain'}
        httpclient.request("POST", method, body=json.dumps(params), headers=headers)

        response = httpclient.getresponse()
        return response
    except Exception,e:
        print traceback.format_exc()


def send_to_server(method, endpoint, params):
    res = get_to(host, port, '/api/token')
    res = json.loads(res.read())
    token = res['token']
    print 'token:',token
    if token:
        if method=='POST':
            res = post_to(host, port, endpoint, params, token)
            res = eval(res.read())
            if res['code']==200:
                return {'code':1, 'content':res['data']}
            else:
                return {'code':0}
        elif method=='GET':
            res = get_to(host, port, endpoint, token)
            res = eval(res.read())
            if res['code']==200:
                return {'code': 1, 'content': res['data']}
            else:
                return {'code': 0}
    else:
        print 2


if __name__=='__main__':
    # print send_to_server('POST','/pattern', {'status':1,'employe_id':2,'time':'2017-06-24:15:35:55','emotion_score':{"anger":2.4181656E-05,"contempt":0.0008225598,"disgust":2.96614016E-05,"fear":3.406367E-07,"happiness":0.8373931,
    #                                                                                                            "neutral":0.1616748,"sadness":4.79113369E-05,"surprise":7.413448E-06}})
    start_time = time.strftime('%Y-%m-%d:%H:%M:%S', time.localtime(time.time() - 3600))
    end_time = time.strftime('%Y-%m-%d:%H:%M:%S', time.localtime(time.time()))
    params = {"employ_id": 1, "timeline": {"start": start_time, "end": end_time}}
    result = send_to_server('POST', '/personal_pattern', params)
    print '1:',result