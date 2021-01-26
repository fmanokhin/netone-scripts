#!/usr/bin/env python3
# -*- coding: koi8-r -*-

from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
import threading
import xml.etree.ElementTree as ET
import os

try:
    os.remove("dump.xml")
except:
    pass

client = SSHClient()
client.set_missing_host_key_policy(AutoAddPolicy())
client.connect('192.168.1.1', port=33, username='username', password='password')

getdump = SCPClient(client.get_transport())
getdump.get('/app/reductor/var/lib/reductor/rkn/dump.xml')

tree = ET.parse('dump.xml')
root = tree.getroot()

ip_list = set()
ipsubnet_list = set()

for content in root.iter('content'):
    for ip in content.findall('ip'):
        ip_list.add(ip.text+'/32')

for content in root.iter('content'):
    for ipsubnet in content.findall('ipSubnet'):
        ipsubnet_list.add(ipsubnet.text)

ip_uniq = list(ip_list)
ipsubnet_uniq = list(ipsubnet_list)
itog = ip_uniq + ipsubnet_uniq


route = os.system('ip route flush all')
route = os.system('ip route add 192.168.128.120/30 dev eth0')
route = os.system('ip route add 192.168.128.148/30 dev eth1')
route = os.system('ip route add default via 192.168.128.121')
route = os.system('iptables -A INPUT -i eth1 -s 192.168.128.150 -p tcp -m multiport --dport 80,443 -j REJECT')


def Blackhole(blackholelist):
    for i in blackholelist:
        os.system('ip route add blackhole '+str(i))

if __name__ == '__main__':
    thread = threading.Thread(target=Blackhole, args=(itog,))
    thread.start()

route = os.system('iptables -D INPUT -i eth1 -s 192.168.128.150 -p tcp -m multiport --dport 80,443 -j REJECT')

exit()
