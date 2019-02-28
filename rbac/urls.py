#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'zhangjingjun'
__mtime__ = '2018/7/25'
# ----------Dragon be here!----------
              ┏━┓      ┏━┓
            ┏━┛ ┻━━━━━━┛ ┻━━┓
            ┃       ━       ┃
            ┃  ━┳━┛   ┗━┳━  ┃
            ┃       ┻       ┃
            ┗━━━┓      ┏━━━━┛
                ┃      ┃神兽保佑
                ┃      ┃永无BUG！
                ┃      ┗━━━━━━━━━┓
                ┃                ┣━┓
                ┃                ┏━┛
                ┗━━┓ ┓ ┏━━━┳━┓ ┏━┛
                   ┃ ┫ ┫   ┃ ┫ ┫
                   ┗━┻━┛   ┗━┻━┛
"""
from . import views
from django.urls import path,re_path

urlpatterns = [
    re_path(r'^users/$', views.users),
    re_path(r'^users/new/$', views.users_new),
    re_path(r'^users/edit/(?P<id>\d+)/$', views.users_edit),
    re_path(r'^users/delete/(?P<id>\d+)/$', views.users_delete),

    re_path(r'^roles/$', views.roles),
    re_path(r'^roles/new/$', views.roles_new),
    re_path(r'^roles/edit/(?P<id>\d+)/$', views.roles_edit),
    re_path(r'^roles/delete/(?P<id>\d+)/$', views.roles_delete),

    re_path(r'^permissions/$', views.permissions),
    re_path(r'^permissions/new/$', views.permissions_new),
    re_path(r'^permissions/edit/(?P<id>\d+)/$', views.permissions_edit),
    re_path(r'^permissions/delete/(?P<id>\d+)/$', views.permissions_delete),

    re_path(r'^menus/$', views.menus),
    re_path(r'^menus/new/$', views.menus_new),
    re_path(r'^menus/edit/(?P<id>\d+)/$', views.menus_edit),
    re_path(r'^menus/delete/(?P<id>\d+)/$', views.menus_delete),

    re_path(r'^$', views.index)
]