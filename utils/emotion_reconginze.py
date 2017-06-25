# -*-coding:utf-8-*-

import httplib
import urllib
import os

key = os.environ.get('Ocp-Apim-Subscription-Key')

headers = {
    # Request headers. Replace the placeholder key below with your subscription key.
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': key,
}

params = urllib.urlencode({
})


def reconginze(url):
    try:
        print 'e url:',url
        body = str({ 'url': url })
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))