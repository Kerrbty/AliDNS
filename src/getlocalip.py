#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sys
import re

http_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}

iCurId = 1

def GetCurrentIp1():
    try: 
        ip138url = 'https://2021.ip138.com/'
        http = requests.session()
        http.keep_alive = False
        html = http.get(ip138url, headers=http_headers)
        findip = re.findall("ip=([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})", html.text)
        return findip[0]
    except Exception:
        return None

def GetCurrentIp2():
    try: 
        sohuurl = 'http://pv.sohu.com/cityjson?ie=utf-8'
        http = requests.session()
        http.keep_alive = False
        html = http.get(sohuurl, headers=http_headers)
        findip = re.findall("({.+})", html.text)
        jvdata = json.loads(findip[0])
        return jvdata['cip']
    except Exception:
        return None

def GetCurrentIp3():
    try: 
        ipurl = 'https://www.ip.cn/api/index?ip=&type=0'
        http = requests.session()
        http.keep_alive = False
        html = http.get(ipurl, headers=http_headers)
        jvdata = json.loads(html.text)
        return jvdata['ip']
    except Exception:
        return None

def GetCurrentIp4():
    try: 
        webmasterhome = 'http://ip.webmasterhome.cn/'
        http = requests.session()
        http.keep_alive = False
        html = http.get(webmasterhome, headers=http_headers)
        findip = re.findall("<strong>([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})</strong>", html.text)
        return findip[0]
    except Exception:
        return None

def GetCurrentIp5():
    try: 
        iptoolurl = 'http://ip.tool.chinaz.com/'
        http = requests.session()
        http.keep_alive = False
        html = http.get(iptoolurl, headers=http_headers)
        findip = re.findall('<span id="IpValue">([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})</span>', html.text)
        return findip[0]
    except Exception:
        return None

def GetCurrentIp6():
    try: 
        hao7188 = 'https://www.hao7188.com/'
        http = requests.session()
        http.keep_alive = False
        html = http.get(hao7188, headers=http_headers)
        delspace = html.text.replace(' ','').replace('\r', '').replace('\n', '')
        findip = re.findall('您的iP地址是：<ahref="ip/([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\.html"', delspace)
        return findip[0]
    except Exception:
        return None

def GetCurrentIp7():
    try: 
        ip123cha = 'https://www.123cha.com/ip/'
        http = requests.session()
        http.keep_alive = False
        html = http.get(ip123cha, headers=http_headers)
        findip = re.findall('ip/\?q=([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', html.text)
        return findip[0]
    except Exception:
        return None

def GetCurrentIp8():
    try: 
        ipify = 'https://api.ipify.org/?format=jsonp&callback=user'
        http = requests.session()
        http.keep_alive = False
        html = http.get(ipify, headers=http_headers)
        findip = re.findall("\(({.+})\)", html.text)
        jvdata = json.loads(findip[0])
        return jvdata['ip']
    except Exception:
        return None

def GetCurrentIp9():
    try: 
        ipapiurl = 'http://ip-api.com/json/?lang=zh-CN'
        http = requests.session()
        http.keep_alive = False
        html = http.get(ipapiurl, headers=http_headers)
        jvdata = json.loads(html.text)
        return jvdata['query']
    except Exception:
        return None

def GetCurrentIp10():
    try: 
        ip138url = 'http://www.ip38.com/'
        http = requests.session()
        http.keep_alive = False
        html = http.get(ip138url, headers=http_headers)
        findip = re.findall("ip=([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})", html.text)
        return findip[0]
    except Exception:
        return None

def GetCurrentIp11():
    try: 
        icanhazip = 'http://icanhazip.com/'
        http = requests.session()
        http.keep_alive = False
        html = http.get(icanhazip, headers=http_headers)
        findip = re.findall("([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})", html.text)
        return findip[0]
    except Exception:
        return None

def GetCurrentIp12():
    try:
        yqie = 'http://ip.yqie.com/clientip.aspx'
        http = requests.session()
        http.keep_alive = False
        html = http.get(yqie, headers=http_headers)
        findip = re.findall("ip=([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})", html.text)
        return findip[0]
    except Exception:
        return None

def GetCurrentIp13():
    try:
        pconline = 'http://whois.pconline.com.cn/ipJson.jsp?json=true'
        http = requests.session()
        http.keep_alive = False
        html = http.post(pconline, headers=http_headers, data="ip=myip")
        findip = re.findall('ip":"([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})"', html.text)
        return findip[0]
    except Exception:
        return None
        
def GetCurrentIp14():
    try:
        jq99 = 'http://members.3322.org/dyndns/getip'
        http = requests.session()
        http.keep_alive = False
        html = http.get(jq99, headers=http_headers)
        findip = re.findall('([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', html.text)
        return findip[0]
    except Exception:
        return None

switch={
    1:GetCurrentIp1, 
    2:GetCurrentIp2, 
    3:GetCurrentIp3, 
    4:GetCurrentIp4, 
    5:GetCurrentIp5, 
    6:GetCurrentIp6, 
    7:GetCurrentIp7, 
    8:GetCurrentIp8, 
    9:GetCurrentIp9, 
    10:GetCurrentIp10, 
    11:GetCurrentIp11, 
    12:GetCurrentIp12, 
    13:GetCurrentIp13, 
    14:GetCurrentIp14, 
}

def GetRealAddr():
    while True:
        global iCurId
        ipAddr = switch[iCurId]()
        iCurId = iCurId + 1  # 下次用下一个查询 
        if iCurId > len(switch):
            iCurId = 1
        if ipAddr:
            break
    return ipAddr, iCurId-1

if __name__ == "__main__":
    for i in range(1, len(switch)+1):
        print( i, switch[i]())
