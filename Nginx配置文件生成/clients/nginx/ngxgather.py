import os 
import glob 
import socket

class NginxConfParse(object):
    def __init__(self, ngxpath):
        self.ngxpath = ngxpath
        self.dirpath = os.path.dirname(ngxpath)
        self.dir  = os.path.dirname(ngxpath)
        self._subconffile()

    def get_upsetream(self):
        return self.parseconf('upstream',"server",
                              filter=("server_tokens","server_name"))

    def get_server(self):
        return self.parseconf("listen","proxy_pass")

    def _upstream(self, upname):
        return upname[7:]

    def _gethost(self):
        name = socket.gethostname()
        localip = socket.gethostbyname(name)
        return localip


    def res_report(self, server, upstream):
        res_list = []
        for s in server:

            '''
                res = {
                    "port": {'upname': ip}
                }
            '''
            for upnames in server[s]:

                res = {
                    "port": s,
                    "upstream": self._upstream(upnames),
                    "ip": upstream.get(self._upstream(upnames))
                }
                res_list.append(res)
        return self._gethost(),res_list

    def parseconf(self,keyword, subkey=None, filter=None):
        if not subkey: subkey = keyword
        if filter is None: filter = tuple()
        count_config = {
            "{": 0
        }
        keyword_dict = {}
        for ngpath in self.ngx_all_path:
            with open(ngpath) as fp:
                tmp_dict = {}
                for line in fp:
                    line = line.strip()
                    if "{" in line:
                        count_config["{"] += 1
                    if keyword in line  and line.startswith(keyword):
                        keyword_name = line.split()[1].strip(";")
                        tmp_dict[keyword_name] = []
                        continue
                    if count_config.get("{") > 0:
                        if line.startswith(subkey) and "{" not in line:
                            key_w   = line.strip(";\n").split()[0]
                            keyline = line.strip(";\n").split()[1]
                            if key_w in filter: continue
                            tmp_dict[keyword_name].append(keyline)

                    if "}" in line:
                        count_config["{"] -= 1
            res = self._addict(keyword_dict, tmp_dict)
        return res

    def _addict(self, inidict, tmdict):
        if len(tmdict) == 0: pass
        for i in tmdict:
            if inidict.get(i):
                for j in tmdict[i]:
                    if j not in inidict[i]:
                        inidict[i] += tmdict[i]
            else:
                inidict[i] = tmdict[i]
        return inidict

    def _subconffile(self):
        self.ngx_all_path = [self.ngxpath]
        tmp_files = []
        tp_name   = []
        with open(self.ngxpath) as fp:
            for line in fp:
                line = line.strip()
                if line.startswith("include"):
                    fnames = line.strip(";\n").split()[-1]
                    tmp_files.append(fnames)
        for f in tmp_files:
            f = self.dir + os.sep + f
            f_name = glob.glob(f)
            for t in f_name:
                tp_name.append(t)
                self.ngx_all_path.extend(tp_name)
        return tp_name
		
if __name__ == "__main__":
    import requests
    import json
    data = {}
    t = NginxConfParse(r'C:\Users\vats\Desktop\untitled\Nginx配置文件生成\nginx.conf')
    upstream = t.get_upsetream()
    server_name = t.get_server()
    res  = t.res_report(server_name, upstream)
    data[res[0]] = res[1]
    print(upstream)

    jdata = json.dumps(data,ensure_ascii=False)
    requests.post('http://127.0.0.1:9999/api/web', json=data)
