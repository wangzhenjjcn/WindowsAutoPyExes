import configparser
import os
import requests
import re

# 检查配置文件是否存在，如果不存在则创建新文件
if not os.path.exists('config.ini'):
    config = configparser.ConfigParser()
    config['Oray'] = {'user': '',
                      'password': '',
                      'hostname': ''}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# 从配置文件中获取必要的配置信息
config = configparser.ConfigParser()
config.read('config.ini')

user = config.get('Oray', 'user')
password = config.get('Oray', 'password')
hostname = config.get('Oray', 'hostname')

# 获取当前的公共IP地址
public_ip = requests.get('https://api.ipify.org').text

# 发送请求更新DNS记录
update_url = f"http://ddns.oray.com/ph/update?hostname={hostname}&myip={public_ip}"
response = requests.get(update_url, auth=(user, password)).text

# 解析返回结果，判断是否更新成功
match_obj = re.match(r'\w+ (\d+)', response)
if match_obj and match_obj.group(1) == '0':
    print(f"DNS record updated with IP address: {public_ip}")
else:
    print(f"Failed to update DNS record: {response}")
