#!/usr/bin/python
#coding:utf-8
import urllib
import requests as re
class IpQuery:
    def get_ip_info(self, ip):
        request_url = 'http://ip.taobao.com/service/getIpInfo2.php?ip=%s' %ip
        city = '未知'
        result = re.get(request_url)
        if result.json()['code'] != 0:
            city = '未知'
        else:
            data = result.json()['data']
            city = data['city']
        print(result)
        print('request_url', request_url)
        return city
test = IpQuery()
print(test.get_ip_info('112.31.253.65'))