from django.conf.urls.defaults import *

urlpatterns = patterns('potbotadmin.Test.views',        
    (r'^stats$', 'stats'),
    (r'^nick/(?P<nick>[a-z0-9A-Z\.\-_]+)$', 'nick'),
    (r'^(?P<channel>[a-z\.]+)$', 'index'),
    (r'^(?P<channel>[a-z\.]+)/since/(?P<hash>[a-z0-9]+)/$', 'since'),
)
