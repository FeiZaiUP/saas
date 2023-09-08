from django.contrib import admin
from django.urls import path, re_path,include
from web.views import account, project

app_name = 'web'

urlpatterns = [
    path('',account.index,name='index'),
    path('web/register/',account.register, name='register'),
    path('web/send_sms/',account.send_sms, name='send_sms'),
    path('web/login_sms/',account.login_sms, name='login_sms'),
    path('web/login_pwd/',account.login_pwd, name='login_pwd'),
    path('web/image_code/',account.image_code, name='image_code'),
    path('web/logout/',account.logout, name='logout'),
    path('project/list/', project.project_list, name='project_list'),
    #   我的星标项目：/project/star/my/1
    #   参与星标项目：/project/star/join/3
    re_path(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_star, name='project_star'),
    re_path(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_unstar, name='project_unstar'),
]
