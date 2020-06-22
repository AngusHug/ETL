import requests
import json
import sys
import os
class DingTalkWarn:
    # 获取发送内容,接收人@对象,
    def msg_context(self, robot_url, text, title, msg_url):
        Headers = {"Content-type":"application/json;charset=utf-8"}
        string_msg = \
            { \
                "msgtype": "link",
                "link": {"text": text,
                "title":title,
                "picUrl":"",
                "messageUrl": msg_url}
            }
        string_context_message = json.dumps(string_msg)
        print(string_context_message)
        req = requests.post(robot_url, data=string_context_message, headers = Headers)
test = DingTalkWarn()
text = "tomorrow ,our company will listing"
title = "tomorrow is another day"
msg_url = "https://mp.weixin.qq.com/s/4GErqVEoYIlCGFG11Mo_JA"
test.msg_context('https://oapi.dingtalk.com/robot/send?access_token=fdf7d705ae7cd8d8ef7e6dfc6591407916b841f621f3c734d52c82928c4212b5'
                 , text, title, msg_url)
