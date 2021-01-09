# 阿里云域名解析设置脚本



## 设置说明 

使用前需要设置 阿里云的AccessKey ，具体获取方法请访问 https://help.aliyun.com/knowledge_detail/38738.html

AccessKey_ID、Access_Key_Secret、region_id 请自行设置，不过多说明



DNS解析信息说明

| 设置项       | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| DomainName   | 你所购买的DNS域名（一级），比如 yourdimain.com               |
| RR           | 主机名，比如设置nas，即访问使用 nas.yourdimain.com           |
| DomainType   | 域名类型，'A' 表示IPV4， 'CNAME' 表示指向另一个域名, 'AAAA' 表示IPV6, 'MX'表示邮箱服务器，其他值请查看阿里云设置 |
| UpdateDomain | 因为是动态获取ip，所以此值设置成 'Auto_Lines' 即可           |
| update_time  | 多久查询一次ip信息，默认5分钟                                |



ip查询网址在 getlocalip.py 中定义，若里面网址无法进行查询ip，请自行修改添加




## 使用更说明
1. ##### 在需要做DDNS的Linux机器上先安装 docker 并 运行
```
$ sudo yum install docker-ce docker-ce-cli containerd.io 
$ sudo systemctl start docker.service
$ sudo systemctl enable docker.service
```

2. ##### 定位到AliDNS目录（存储repositorie目录）
```
$ chmod a+x build.sh 
$ sudo ./build.sh
```

这时候，docker就会进行打包images，需要等待时间较长（具体看网络情况）。正常完成以后日志如下：

```
Sending build context to Docker daemon  87.55kB
Step 1/6 : FROM python:3.6
3.6: Pulling from library/python
6c33745f49b4: Already exists 
ef072fc32a84: Already exists 
c0afb8e68e0b: Already exists 
d599c07d28e6: Already exists 
0e7ac7e3db3f: Pull complete 
dfd5461cd34f: Pull complete 
e6a2d3233da5: Pull complete 
099a5f6e48a0: Pull complete 
Digest: sha256:4c00d277e8c189175dc460419e17049b98d7d93dd3021700ddb8400646bbc50a
Status: Downloaded newer image for python:3.6
 ---> bd4a91d81d7e
Step 2/6 : RUN mkdir -p /home/worker
 ---> Running in bbefd175408d
Removing intermediate container bbefd175408d
 ---> 9c3a0dac0af3
Step 3/6 : WORKDIR /home/worker
 ---> Running in a176f2b37096
Removing intermediate container a176f2b37096
 ---> 4688fc04fae6
Step 4/6 : COPY ./src/ /home/worker
 ---> 87bd1abf9185
 Step 5/6 : RUN pip install --upgrade pip -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com -r /home/worker/requirements.txt
 ---> Running in 0b86cc9d6ee1
Looking in indexes: http://mirrors.aliyun.com/pypi/simple
Requirement already satisfied: pip in /usr/local/lib/python3.6/site-packages (20.3.3)
Collecting aliyun-python-sdk-alidns
 ..... 
 # 省略各种下载阿里云sdk的过程 
 .....
 Building wheels for collected packages: aliyun-python-sdk-core, pyyaml
  Building wheel for aliyun-python-sdk-core (setup.py): started
  Building wheel for aliyun-python-sdk-core (setup.py): finished with status 'done'
  Created wheel for aliyun-python-sdk-core: filename=aliyun_python_sdk_core-2.13.30-py3-none-any.whl size=532928 sha256=6017e33f8cac3cecf6d91631dbef1864edac56157b5966355adaca8f18a3854d
  Stored in directory: /root/.cache/pip/wheels/45/7f/17/c0e258c24212e1088e8fd74918b5d0f9a21c9aca128ee5a455
  Building wheel for pyyaml (setup.py): started
  Building wheel for pyyaml (setup.py): finished with status 'done'
  Created wheel for pyyaml: filename=PyYAML-5.3.1-cp36-cp36m-linux_x86_64.whl size=480521 sha256=56b937aeec37108c50365278439467513860ab0511e5dcb5df503eacf2f91958
  Stored in directory: /root/.cache/pip/wheels/ad/52/a5/edfc82397b33b9d8491ff1b014bbc2a7c757bbbb18cf15e13c
Successfully built aliyun-python-sdk-core pyyaml
Installing collected packages: pycparser, six, cffi, jmespath, cryptography, urllib3, idna, chardet, certifi, aliyun-python-sdk-core, requests, pyyaml, aliyun-python-sdk-alidns
Successfully installed aliyun-python-sdk-alidns-2.6.20 aliyun-python-sdk-core-2.13.30 certifi-2020.12.5 cffi-1.14.4 chardet-4.0.0 cryptography-3.2.1 idna-2.10 jmespath-0.10.0 pycparser-2.20 pyyaml-5.3.1 requests-2.25.1 six-1.15.0 urllib3-1.26.2
Removing intermediate container 0b86cc9d6ee1
 ---> 20a75a39dca2
Step 6/6 : CMD ["python", "/home/worker/UpdateDNS.py"]
 ---> Running in 0c00c583dea8
Removing intermediate container 0c00c583dea8
 ---> 8746a9891e94
Successfully built 8746a9891e94
Successfully tagged alidns:latest
```

注意最后提示：Successfully built 8746a9891e94 ， 也就是成功建立了ID为 8746a9891e94 的docker image

这时候可以用命令查看会发现多出两个image：

```
$ sudo docker images
REPOSITORY    TAG       IMAGE ID       CREATED         SIZE
alidns        latest    8746a9891e94   4 minutes ago   901MB
python        3.6       bd4a91d81d7e   3 weeks ago     874MB
```

3. ##### 启动运行 alidns 镜像
```
$ sudo docker run --restart=always -d alidns
```
