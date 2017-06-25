#!/usr/bin/env python
# encoding: utf-8

import cv2
import os
import hashlib
import random
import datetime
import time
import traceback
from phizard.utils.ali_client import upload, get_sign_url
from phizard.utils.emotion_reconginze import reconginze
from phizard.utils.restful_cli import send_to_server


def take_pic(save_path='./pics'):
    '''Take one shot and save the picture to the save_path
    '''

    cam = cv2.VideoCapture(0)
    counter = 0
    while(counter < 10):
        counter += 1
        retval, frame = cam.read() 
        #cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    #cv2.imshow('frame', frame) 
    filename = str(datetime.datetime.now()) + str(random.uniform(0, 20))
    filename = hashlib.md5(filename).hexdigest()+'.bmp'
    cv2.imwrite(save_path+filename, frame)

    return filename, save_path

def recognize_pic(filename, save_path):
    res = upload(filename, save_path+filename)
    if res['result_code']==1:       # upload success
        url = get_sign_url(filename)
        if url:
            emotion = reconginze(url)
            emotion = eval(emotion)
            if isinstance(emotion, list) and len(emotion)==1:
                scores = emotion[0]['scores']
                taken_time = time.strftime('%Y-%m-%d:%H:%M:%S', time.localtime(time.time()))
                status = send_to_server('POST','/pattern',{'status':1,'employe_id':1,'time':taken_time,'emotion_score':scores})
                if status['code']==0:
                    print 'save failed'
                elif status['code']==1:
                    print 'save success'
                else:
                    print 'authenticated failed'
            else:
                print 'invalid pictures'
    elif res['result_code']==2:     # file name already used
        print 'file name already used'
    else:                           # upload failed
        print 'upload failed'

if __name__ == '__main__':
    counter = 0
    while True:
        counter += 1
        filename, save_path = take_pic()
        recognize_pic(filename, save_path)
        try:
            os.remove(save_path+filename)
            file_state = 'removed'
        except Exception, e:
            traceback.print_exc()
            print e
            file_state = 'remove failed'
        print "%d: %s (%s)" % (counter, filename, file_state)
        time.sleep(10)

