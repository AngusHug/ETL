import requests
import json
import sys
import os
class DingTalkWarn:
# 获取发送内容,接收人@对象,
    def msg_context(self, robot_url, text,title, mobiles, isAt):
        Headers = {"Content-type":"application/json;charset=utf-8"}
        string_msg = \
           {
           "actionCard": { \
            "text": text,
               "title":title,
               "hideAvatar": "0",
        "btnOrientation": "0",
        "btns": [
            {
                "title": "内容不错",
                "actionURL": "https://www.dingtalk.com/"
            },
            {
                "title": "不感兴趣",
                "actionURL": "https://www.dingtalk.com/"
            }
        ]
           },
               "msgtype": "actionCard"
           }
        string_context_message = json.dumps(string_msg)
        print(string_context_message)
        req = requests.post(robot_url, data=string_context_message, headers = Headers)
text = '![screenshot](serverapi2/@lADOpwk3K80C0M0FoA) \### 乔布斯 20 年前想打造的苹果咖啡厅 \
        Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划'
test = DingTalkWarn()

robot_url = 'https://oapi.dingtalk.com/robot/send?access_token=fdf7d705ae7cd8d8ef7e6dfc6591407916b841f621f3c734d52c82928c4212b5'
test.msg_context(robot_url, text, '乔布斯 20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身','17816875837', 1)