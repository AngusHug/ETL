#!/usr/bin/python
#coding:utf-8
import requests
import re
import json
class CarAttribution:
    def get_web(self, web_url, headers):
        request_url = web_url
        headers = headers
        response = requests.get(web_url, headers).content.decode("utf-8", errors='ignore')
        # print(response)
        return response
    
    def get_pro_city(self, text):
        info_tab = re.search('<div class="coninfo">([.\n]+?)coninfo-->', text)
        return info_tab
    
def test():
    test = CarAttribution()
    request_url = 'http://tool.webmasterhome.cn/chepai.asp'
    headers = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    text = test.get_web(web_url=request_url, headers=headers)
    info_tab = test.get_pro_city(text)
    print(info_tab)
if __name__ == '__main__':
    test()