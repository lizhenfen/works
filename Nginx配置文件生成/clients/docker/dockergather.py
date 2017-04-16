try:
    import commands
except ImportError:
    import subprocess as commands
import requests
import json

import socket
import fcntl
import struct

import urllib
PYTHON3 = 0
try:
    import urllib2
except ImportError as e:
    PYTHON3 = 1

def get_net_interface(path="/proc/net/dev"):
    interfaces = []
    with open(path) as fp:
        for line in fp:
            if ":" not in line: continue
            interfaces.append(line.split(":")[0].strip())
    return interfaces        
 
def get_net_ip(ifname='eth0'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ipaddr = socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s',ifname[:15])
    )[20:24])
    return ipaddr


status,res = commands.getstatusoutput('sh dockerinfo.sh')
if not status:
    docker_uri = "http://192.168.17.106:9999/api/docker"
    res = json.dumps(res)
    res["ip"] = get_net_ip() 
    requests.post(docker_uri, json=res)
    
    if not PYTHON3:
        res = urllib.urlencode(res)
        req = urllib2.Request(docker_uri,res)
        response = urllib2.urlopen(req)
    else:
        res = urllib.parse.urlencode(res)
        req = urllib.request.Request(docker_uri,res)
        response = urllib.request.urlopen(req)