#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import yaml
import sys
import time
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from getlocalip import GetRealAddr

def AliAccessKey(id,Secret,region):
    try:
        client = AcsClient(id, Secret, region)
        return client
    except Exception as e:
        print("验证aliyun key失败")
        print(e)
        sys.exit(-1)

def read_yaml(filename):
    try:
        yaml_file = open(filename,"rb")
        yaml_data = yaml.safe_load(yaml_file)
        yaml_file.close()
        return yaml_data
    except Exception as e:
        print("读取配置文件错误")
        print(e)
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
        print("获取RecordId失败")
        print(e)
        sys.exit(-1)
    return '','' # 不存在 

def AddOrUpdateDomainRecord(client, DomainName, yaml_data, RecordId, ipAddr):
    try:
        # 查看是更新还是添加记录 
        if len(RecordId)>0:
            request = UpdateDomainRecordRequest()
            request.set_RecordId(RecordId)
            print("更新", RecordId, len(RecordId))
        else:
            request = AddDomainRecordRequest()
            request.set_DomainName(DomainName)
            print("添加")
            
            
        request.set_accept_format('json')

        if 'Auto_Lines' == yaml_data['UserData']['UpdateDomain']:
            DomainValue = GetRealAddr()
        else :
            DomainValue = yaml_data['UserData']['UpdateDomain']
            
        # 如果跟已有设置是一致的，则直接返回 
        if DomainValue == ipAddr:
            return RecordId,DomainValue
            
        # 跟设置的不同才需要更新，如果已经设置一样则不用 
        request.set_Value(DomainValue)
        request.set_Type(yaml_data['UserData']['DomainType'])
        request.set_RR(yaml_data['UserData']['RR']) 
        response = client.do_action_with_exception(request)
        
        json_data = json.loads(str(response, encoding='utf-8'))
        # print("更新域名解析成功")
        # print("域名:" + yaml_data['UserData']['DomainName'] + " 主机:" + yaml_data['UserData']['RR'] + " 记录类型:" +  yaml_data['UserData']['DomainType'] + " 记录值:" +  DomainValue)
        
        return json_data['RecordId'],DomainValue
    except Exception as e:
        print("更新域名解析失败")
        print(e)
        return RecordId,ipAddr


def main():
    yaml_data = read_yaml('./conf.yaml')
    client = AliAccessKey(yaml_data['AliyunData']['AccessKey_ID'],yaml_data['AliyunData']['Access_Key_Secret'],yaml_data['AliyunData']['region_id'])
    RecordId,CurrentSetIP = GetDNSRecordId(yaml_data,client,yaml_data['UserData']['DomainName'])
    while True:
        TmpRecordId,CurrentSetIP = AddOrUpdateDomainRecord(client, yaml_data['UserData']['DomainName'], yaml_data, RecordId, CurrentSetIP)
        time.sleep(yaml_data['UserData']['update_time']) 

if __name__ == "__main__" :
    main()
