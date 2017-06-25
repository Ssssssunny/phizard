# -*-coding:utf-8-*-
import os
import traceback

import oss2
from itertools import islice

endpoint = 'oss-cn-shanghai.aliyuncs.com'
access_key_id = os.environ.get('ACCESS_KEY_ID') or 'LTAIaWTzNvIyDJgG'
access_key_secret = os.environ.get('ACCESS_KEY_SECRET') or  'HqooyWcmYGlovhuqxVoSb8ka3VBCZh'
bucket_name = os.environ.get('BUCKET_NAME') or 'hateam2'

auth = oss2.Auth(access_key_id, access_key_secret)
service = oss2.Service(auth, endpoint)
bucket = oss2.Bucket(auth, endpoint, bucket_name)


def list_all():
    file_list = []
    for b in islice(oss2.ObjectIterator(bucket), 100):
        file_list.append(b.key)
    return file_list


def is_exist(name):
    exist = bucket.object_exists('images/'+name)
    if exist:
        return True
    else:
        return False


def upload(file_name, file_path):
    file_name = 'images/'+file_name
    if is_exist(file_name):
        return {'result_code':2}            # file_name exist
    try:
        result = bucket.put_object_from_file(file_name, file_path)
        return {'result_code':1, 'http_status':result.status, 'request_id':result.request_id,
                'ETag':result.etag, 'date':result.headers['date']}
    except Exception:
        print traceback.format_exc()
        return {'result_code':0}            # upload failed


def get_sign_url(file_name, timeout=600):
    return bucket.sign_url('GET', 'images/'+file_name, timeout)

# if __name__=="__main__":
#     print list_all()