from django.conf.urls import patterns, include, url
import xadmin
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
#from xadmin.plugins import xversion
#xversion.register_models()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Web.views.home', name='home'),
    # url(r'^Web/', include('Web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'admin/', include(xadmin.site.urls))
)
