try:
    import commands
except ImportError:
    import subprocess as commands
import requests
import json

status,res = commands.getstatusoutput('sh dockerinfo.sh')
if status:
    jdata = json.dumps(res)
    requests.post('http://127.0.0.1:9999/api/docker', json=jdata)
