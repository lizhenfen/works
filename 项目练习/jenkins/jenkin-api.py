#!/usr/bin/env python
# pip install python-jenkins

import jenkins

JENKIN_SERVER_URL = "http://192.168.15.36:8080/jenkins/login?from=/jenkins/"
JENKIN_USER_ID = "root"
JENKIN_PASSWORD= "rootad"

class JenkinApi(object):

    def __init__(self, url, user=None, pasword=None, token=None):
        self._server = self._login(url, user, pasword, token)
        self._id = None
        
    def _login(self, user, password, token):
        if token is not None:
            server = jenkins.Jenkins(url,token)
        if user is not None:
            server = jenkins.Jenkins(url, username=user, password=password)
        return server
     
    def get_version(self):
        return self._server.get_version()
        
    def get_current_user(self):
        return self._server.get_whoami()
    
    def get_job_num(self):
        return self._server.jobs_count()
        
    def get_jobs(self):
        jobs = self._server.get_jobs()
        for job in jobs:
            yield job

    def get_job_info(self, job_name):
        info = self._server.get_job_info(job_name)
        return info
      
    def build_job(self, job_name):
        self._server.build_job(job_name)
        queue_info = server.get_queue_info()
        self._id = queue_info[0].get('id')
        return 
        
    def cacel_job(id):
        self._server.cancel_queue(id)
   
