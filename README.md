# 阿里云域名解析设置脚本



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