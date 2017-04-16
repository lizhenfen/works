#!/usr/bin/env python
import json
import paramiko

class ConnSSH(object):
    def __init__(self,host,port=22,username=None, password=None, allow_agent=True):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.allow_agnet = allow_agent
        self._conn()

    def exec_cmd(self, cmd):
        stdin,stdout,stderr = self.ssh.exec_command(cmd)
        if stdout:
            res = stdout.read()
        else:
            res = stderr.read()
        return res

    def trans_file(self, inpath, outpath):
        ftp = self.ssh.open_sftp()
        ftp.put(inpath,outpath)
        ftp.close()
        return outpath

    def _conn(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.host,port=self.port,
                        username=self.username,
                        password=self.password,
                        allow_agent=self.allow_agnet)
        except Exception as e:
            err_msg = "ssh conn error: %s" % str(e)
            return err_msg
        return self.ssh

class ConnSFTP(object):
    def __init__(self,host,port=22,username=None, password=None, allow_agent=True):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self._con()

    def put(self, inpath, outpath):
        self.sftp.put(inpath, outpath)

    def _con(self):
        t = paramiko.Transport((self.host,self.port))
        t.connect(username=self.username, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(t)

if __name__ == '__main__':

    #m = ConnSFTP("192.168.15.39",username="root", password="vats@password")
    #m.put(r"G:\work\Nginx配置文件生成\配置文件解析.py","/tmp/pt.py")
    t = ConnSSH("192.168.15.39", username="root", password="vats@password")
    t.trans_file(r"G:\work\Nginx配置文件生成\配置文件解析.py","/tmp/pt1.py")
    d = t.exec_cmd('ls -l /tmp').decode()
    d= json.dumps(d, indent=4, sort_keys=True)
    print(d)