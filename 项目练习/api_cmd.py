#!/usr/bin/env python
#-*- coding: utf8 -*-

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.module_utils._text import to_bytes
from ansible.plugins.callback import CallbackBase

import json

#日志记录
import os
import time

#callback
# github: https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/callback/log_plays.py
# blog: http://www.cnblogs.com/ivictor/p/6235420.html
# shencan:  http://www.shencan.net/index.php/2014/07/17/ansible-%E6%8F%92%E4%BB%B6%E4%B9%8Bcallback_plugins-%EF%BC%88%E5%AE%9E%E6%88%98%EF%BC%89/
# api:  http://docs.ansible.com/ansible/dev_guide/developing_api.html
#获取setup返回值
class ResultCallBack(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'log_plays'
    CALLBACK_NEEDS_WHITELIST = True

    TIME_FORMAT="%b %d %Y %H:%M:%S"
    MSG_FORMAT="%(now)s - %(category)s - %(data)s\n\n"
    
    def __init__(self):
        super(ResultCallBack, self).__init__()
        if not os.path.exists("/var/log/ansible/hosts"):
            os.makedirs("/var/log/ansible/hosts")
            
    def log(self, host, category, data):
        if type(data) == dict:
            if '_ansible_verbose_override' in data:
                # avoid logging extraneous data
                data = 'omitted'
            else:
                data = data.copy()
                invocation = data.pop('invocation', None)
                data = json.dumps(data)
                if invocation is not None:
                    data = json.dumps(invocation) + " => %s " % data

        path = os.path.join("/var/log/ansible/hosts", host)
        now = time.strftime(self.TIME_FORMAT, time.localtime())

        msg = to_bytes(self.MSG_FORMAT % dict(now=now, category=category, data=data))
        with open(path, "ab") as fd:
            fd.write(msg)
    
    def runner_on_ok(self, host, res):
        self.log(host, 'OK', res)
    '''   
    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        res = json.dumps({host.name: result._result}, indent=4)
        print(res)
        
        #self.log(host, 'FAILED', res)
    '''    
resultcallback = ResultCallBack()

Options = namedtuple('Options',['listtags','listtasks','listhosts',
                    'syntax','connection','module_path','forks','private_key_file',
                    'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args',
                    'become', 'become_method', 'become_user', 'verbosity', 'check'])
                    
variable_manager = VariableManager()
loader = DataLoader()

options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False,
                  connection="ssh", module_path=None, forks=100, private_key_file=None,
                  ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None,
                  become=None, become_method=None, become_user=None, verbosity=None, check=False)
                  
passwords = {}
inventory = Inventory(loader=loader, variable_manager=variable_manager)
variable_manager.set_inventory(inventory)

#组装执行命令
play_source = dict(
                name = "Ansible Play",
                hosts= 'localhost',
                gather_facts = "no",
                tasks = [
                    dict(action=dict(module="shell", args="ls"), register="shell_out"),
                    dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
                    ]
                )
play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
#加入执行队列
#stdout_callback="default"
qm = None
try:
    tqm = TaskQueueManager(
            inventory = inventory,
            variable_manager = variable_manager,
            loader = loader,
            options = options,
            passwords = passwords,
            stdout_callback = resultcallback,
            )
    tqm.run(play)
finally:
    if tqm is not None:
            tqm.cleanup()
            
            