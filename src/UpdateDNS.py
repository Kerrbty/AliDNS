#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import yaml
import sys
import time
import _thread
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from getlocalip import GetRealAddr

last_update_time = 0  # 秒数  
exit_flags = False 

def logger(*nums):
    print(time.strftime("[%Y-%m-%d][%H:%M:%S] ", time.localtime()), end="")
    for argv in nums:
        print(argv, end=" ")
    print()
    sys.stdout.flush()

def AliAccessKey(id,Secret,region):
    try:
        client = AcsClient(id, Secret, region)
        return client
    except Exception as e:
        logger("验证aliyun key失败")
        logger(e)
        exit_flags = True
        sys.exit(-1)

def read_yaml(filename):
    try:
        yaml_file = open(filename, "rb")
        yaml_data = yaml.safe_load(yaml_file)
        yaml_file.close()
        return yaml_data
    except Exception as e:
        logger("读取配置文件错误")
        logger(e)
        exit_flags = True
        sys.exit(-1)

def GetDNSRecordId(yaml_data, client, DomainName):
    try:
        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(DomainName)
        response = client.do_action_with_exception(request)
        json_data = json.loads(str(response, encoding='utf-8'))

        for RecordId in json_data['DomainRecords']['Record']:
            if yaml_data['UserData']['RR'] == RecordId['RR']:
                return RecordId['RecordId'],RecordId['Value']

    except Exception as e:
        logger("获取RecordId失败")
        logger(e)
        exit_flags = True
        sys.exit(-1)
    return '','' # 不存在 

def AddOrUpdateDomainRecord(client, DomainName, yaml_data, RecordId, ipAddr):
    try:
        if len(RecordId)>0:
            request = UpdateDomainRecordRequest()
            request.set_RecordId(RecordId)
        else:
            request = AddDomainRecordRequest()
            request.set_DomainName(DomainName)

        request.set_accept_format('json')

        if 'Auto_Lines' == yaml_data['UserData']['UpdateDomain']:
            DomainValue,cid = GetRealAddr()
        else :
            DomainValue = yaml_data['UserData']['UpdateDomain']
           
        if DomainValue == ipAddr:
            return RecordId,DomainValue
        
        # 跟设置的不同才需要更新，如果已经设置一样则不用 
        request.set_Value(DomainValue)
        request.set_Type(yaml_data['UserData']['DomainType'])
        request.set_RR(yaml_data['UserData']['RR']) 
        response = client.do_action_with_exception(request)
        
        json_data = json.loads(str(response, encoding='utf-8'))
        logger("更新域名解析成功: ", "(", cid, "): ", DomainValue)
        # logger("域名:" + yaml_data['UserData']['DomainName'] + " 主机:" + yaml_data['UserData']['RR'] + " 记录类型:" +  yaml_data['UserData']['DomainType'] + " 记录值:" +  DomainValue)
        
        return json_data['RecordId'],DomainValue
    except Exception as e:
        logger("更新域名解析失败")
        logger(e)
        return RecordId,ipAddr
        
def watch_dog():
    global exit_flags
    global last_update_time
    while True:
        time.sleep(30)
        if last_update_time+16*60<int(time.time()):
            # 长时间卡住,直接退出,让supervisor重启服务 
            logger("看门狗超时,重启ddns服务")
            exit_flags = True

def ddns_thread():
    global exit_flags
    global last_update_time
    last_update_time = int(time.time())
    yaml_data = read_yaml('./conf.yaml')
    client = AliAccessKey(yaml_data['AliyunData']['AccessKey_ID'],yaml_data['AliyunData']['Access_Key_Secret'],yaml_data['AliyunData']['region_id'])
    RecordId,CurrentSetIP = GetDNSRecordId(yaml_data,client,yaml_data['UserData']['DomainName'])
    while not exit_flags:
        TmpRecordId,CurrentSetIP = AddOrUpdateDomainRecord(client, yaml_data['UserData']['DomainName'], yaml_data, RecordId, CurrentSetIP)
        # logger(TmpRecordId, CurrentSetIP)
        last_update_time = int(time.time())
        time.sleep(5*60) # 5分钟去查询一次 
    # 不知道什么原因到这里,需要重启 
    exit_flags = True

if __name__ == "__main__" :
    try:
        _thread.start_new_thread( watch_dog, () )
        _thread.start_new_thread( ddns_thread, () )
    except:
        exit(0)
    # 等待线程异常，再主线程退出(子线程里面exit无效)   
    while not exit_flags:
        time.sleep(10)
    exit(0)
