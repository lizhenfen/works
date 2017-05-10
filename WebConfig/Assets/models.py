#-*- coding: utf-8 -*-
from django.db import models

class Ip(models.Model):
    address_v4 = models.GenericIPAddressField('V4地址')
    ssh_port   = models.IntegerField('远程端口',default=22)
    ssh_user   = models.CharField('SSH用户', max_length=32)
    ssh_pass   = models.CharField('SSH密码', max_length=128, null=True, blank=True)
    ssh_pri_key= models.CharField('SSH秘钥',max_length=128,default='/root/.ssh/id_rsa')
    is_pass    = models.CharField('密码连接',choices=(('1','是'),('0','否')), default='1', max_length=2)
    is_used    = models.BooleanField('启用', default=True)
    comments   = models.CharField('备注', max_length=256, null=True, blank=True)
    update_time = models.DateTimeField('更新时间', auto_now_add=True)
    create_time = models.DateTimeField('创建时间', auto_now=True)

    class Meta:
        verbose_name = '管理地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address_v4

class DataCenter(models.Model):
    name = models.CharField('机房名称',max_length=32)
    location = models.CharField('机房位置', max_length=256,null=True, blank=True)
    manager  = models.CharField('管理人', max_length=32)
    mobile   = models.CharField('手机', max_length=11,null=True, blank=True)

    class Meta:
        verbose_name = "机房信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

class Host(models.Model):
    host_name  = models.CharField('主机名称',max_length=64)
    host_ip    = models.ManyToManyField(Ip,verbose_name='绑定地址')
    versions   = (
        ('1', 'Centos 6.8'),
        ('2', 'Centos 7.2'),
        ('3', 'Window Server 2003'),
        ('4', 'Window Server 2008'),
        ('5', 'Other System'),
    )
    sys_version = models.CharField('操作系统', choices=versions, max_length=32,default='1')
    comments = models.CharField('备注', max_length=256, null=True, blank=True)
    location = models.ForeignKey(DataCenter, verbose_name='机房')
    update_time = models.DateTimeField('更新时间',auto_now_add=True,)
    create_time = models.DateTimeField('创建时间',auto_now=True)

    class Meta:
        verbose_name = '主机信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.host_name