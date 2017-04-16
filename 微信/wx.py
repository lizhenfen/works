#! /usr/bin/env python

import requests
import json


def get_token(appid, secure):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}'.format(appid, secure)
    req = requests.get(url)
    data = json.loads(req.text)
    print(data)
    return data["access_token"]


def send_msg(token, msg):
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(token)
    values = """{
   "touser": "lizhen",
   "toparty": "2",
   "totag": "",
   "msgtype": "text",
   "agentid": 2,
   "text": {
       "content": "%s"
   },
   "safe":0
    }""" % msg
    data = json.dumps(values)
    req = requests.post(url, values)


if __name__ == '__main__':
    values = {'appid': 'wxe94db0c2eaa455a1',
              'secure': 'jb9Yoejq4aLgrgO9ChQxgOEAtNWZ0zAgUSys6ni6EpsfDfBSCGsfOQw7Ne6363rr',
              }
    token = get_token(**values)
    send_msg(token, 'i love you')
