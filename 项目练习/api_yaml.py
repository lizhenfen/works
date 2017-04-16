#!/usr/bin/env python
#-*- coding: utf8 -*-

import os
import sys

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.utils.display import log_file


#设置变量
Options = namedtuple('Options',['listtags','listtasks','listhosts',
                    'syntax','connection','module_path','forks','private_key_file',
                    'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args',
                    'become', 'become_method', 'become_user', 'verbosity', 'check'])
                    
variable_manager = VariableManager()
loader = DataLoader()
inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list="/etc/ansible/hosts")

options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False,
                  connection="ssh", module_path=None, forks=100, private_key_file=None,
                  ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None,
                  become=None, become_method=None, become_user=None, verbosity=None, check=False)
                  
#注入yaml
playbook_yaml = "tet.yaml"
variable_manager.extra_vars = {"aa": "xx"}
if not os.path.exists(playbook_yaml):
    print '[INFO] the playbook not exists'
    sys.exit()
#执行并打印结果
passwords = {}
pbex  = PlaybookExecutor(playbooks=[playbook_yaml], inventory=inventory,
                         variable_manager=variable_manager, loader=loader, options=options, passwords=passwords)
code = pbex.run()
stats = pbex._tqm._stats
hosts = sorted(stats.processed.keys())
result = [{h:stats.summarize(h)} for h in hosts]
results = {"code": code, "result": result, "playbook": playbook_yaml}
print(results)                         

