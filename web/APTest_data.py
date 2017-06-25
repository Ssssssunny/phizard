# -*-coding:utf-8-*-
import os
import hashlib
import httplib,urllib
import json
import requests
from base64 import b64encode

host = '172.11.30.21'
port = 8006


def gettest(host, port, method, token=None):
    try:
        if not token:
            m = hashlib.md5()
            m.update('123')
            pwd = m.hexdigest()
            userAndPass = b64encode("amy" + pwd).decode("ascii")
        else:
            userAndPass = b64encode(token + ":").decode("ascii")

        header = {"Authorization": 'Basic %s' % userAndPass, 'content-type': 'application/json',
                  'Accept': 'text/plain'}
        httpclient = httplib.HTTPConnection(host, port)
        httpclient.request("GET", method, headers=header)

        response = httpclient.getresponse()
        return response

    except Exception, e:
        print e


def get_token(url):
    resp = gettest(host, port, url, token=None)
    token = eval(resp.read())['token']
    return token



# def get_users_followd(url):
#     resp = gettest(host, port, url, token=None)
#     return resp.read()


if __name__ == '__main__':

    print "-" * 10 + "get token" + "-" * 10

    token = get_token("/auth/token")
    print token
