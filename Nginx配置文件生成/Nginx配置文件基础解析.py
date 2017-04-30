from __future__ import ( absolute_import,
                        with_statement )
from collections import OrderedDict
import os 
import glob 
import socket

NGX_SERVER = ["events","http"]
NGX_SECTION = ["server","upstream"]
NGX_URI     = ["location",]

class NginxConfParse(object):
    def __init__(self, ngx_conf_path):
        self.ngx_conf_path = ngx_conf_path
        self.nginx_dir  = os.path.dirname(os.path.abspath(ngx_conf_path))
        self.parse()

    def parse(self):
        #解析日志文件成字典
        self._parse_sub_conf_file()

    def get_server(self):
        pass

    def get_upstream(self):
        pass

    def _parse_sub_conf_file(self):
        self.ngx_conf_files = [ self.ngx_conf_path ]
        ngx_cnf = OrderedDict()
        section_count = {"{": 0 }
        tmp = ''
        sever_info = {}
        with open(self.ngx_conf_path, 'r', encoding="utf-8") as fp:
            for line in fp:
                line = line.strip().strip("'")
                if line.startswith("#"): continue
                # 不存在{, 且不存在; , 当前行为多行数据,
                # 追加下一行数据到当前行, 知道遇见;
                if ("{" not in line and ";" not in line
                    and "}" not in line):
                    tmp += line
                    continue
                if tmp:
                    line = tmp + line
                    tmp = ''

                if line.lstrip('').startswith('}'):
                    section_count["{"] -= 1
                    continue
                if "}" in line:
                    section_count["{"] -= 1
                    line = line.rstrip("}")

                #存在{ , 但是不存在 ; , 属于新的段落
                if "{" in line:
                    section_count["{"] += 1
                    line = line.rstrip('{')


                # 第一层配置
                if section_count['{'] == 1:
                    print(line)
                #全局配置
                k,_,v = line.partition(" ")
                ngx_cnf[k] = v

if __name__ == "__main__":
    ngx = NginxConfParse("nginx.conf")
