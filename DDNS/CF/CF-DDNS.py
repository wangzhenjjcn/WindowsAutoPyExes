import configparser
import os
import requests

# 检查配置文件是否存在，如果不存在则创建新文件
if not os.path.exists('config.ini'):
    config = configparser.ConfigParser()
    config['Cloudflare'] = {'zone_id': '',
                            'api_key': '',
                            'email': ''}
    config['DNS'] = {'record_name': '',
                     'record_type': '',
                     'proxied': '',
                     'ttl': ''}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# 从配置文件中获取必要的配置信息
config = configparser.ConfigParser()
config.read('config.ini')

zone_id = config.get('Cloudflare', 'zone_id')
api_key = config.get('Cloudflare', 'api_key')
email = config.get('Cloudflare', 'email')
record_name = config.get('DNS', 'record_name')
record_type = config.get('DNS', 'record_type')
proxied = config.get('DNS', 'proxied')
ttl = config.get('DNS', 'ttl')

# 获取当前的公共IP地址
public_ip = requests.get('https://api.ipify.org').text

# 使用Cloudflare API更新DNS记录
url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
params = {
    "name": record_name,
    "type": record_type,
    "content": public_ip,
    "ttl": ttl,
    "proxied": proxied
}
response = requests.post(url, headers=headers, json=params).json()

# 输出更新结果
if response['success']:
    print(f"DNS record updated with IP address: {public_ip}")
else:
    print(f"Failed to update DNS record: {response['errors'][0]['message']}")
