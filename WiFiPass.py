import subprocess
import re

command_output = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True).stdout.decode('gbk')

profile_names = re.findall('所有用户配置文件 : (.*)\r', command_output)

wifi_list = []
if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = {}
        profile_info = subprocess.run(['netsh', 'wlan', 'show', 'profile', name], capture_output=True).stdout.decode('gbk', 'ignore')
        if re.search('安全密钥               : 存在', profile_info):
            wifi_profile['ssid'] = name
            profile_info_pass = subprocess.run(['netsh', 'wlan', 'show', 'profile', name, 'key=clear'], capture_output=True).stdout.decode('gbk', 'ignore')
            password = re.search('关键内容            : (.*)\r', profile_info_pass)
            if password == '不存在':
                wifi_profile['password'] = None
            else:
                wifi_profile['password'] = password[1]
            wifi_list.append(wifi_profile)
            
for wifi in wifi_list:
    print(wifi)