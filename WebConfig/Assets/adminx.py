#-*- coding: utf-8 -*-
import xadmin
from xadmin import views
from .models import (Ip,Host,
                    DataCenter)

from utils import passwd

class GlobalSettings(object):
    site_title = "信息中心"
    site_footer= "金东资本"
    menu_style = "accordion"
xadmin.site.register(views.CommAdminView, GlobalSettings)

class IpAdmin(object):
    list_display = ('address_v4','ssh_port','ssh_user','ssh_pass','ssh_pri_key','is_used','update_time')
    search_fields = ['address_v4','is_used']
    list_filter  = ['update_time']
    #此函数用来自定义保存的数据
    def save_models(self):
        obj = self.new_obj
        obj.ssh_pass = passwd.encrypt(119,obj.ssh_pass)
        obj.save()


class HostAdmin(object):
    list_display =('host_name', 'host_ip','sys_version','location','comments','update_time')
    #下面实现了相同的样式, 多对多关系 filter_horizontal = ('host_ip',)
    style_fields = {'host_ip': 'm2m_transfer'}


class DataCenterAdmin(object):
    pass

xadmin.sites.site.register(Ip, IpAdmin)
xadmin.sites.site.register(Host, HostAdmin)
xadmin.site.register(DataCenter, DataCenterAdmin)