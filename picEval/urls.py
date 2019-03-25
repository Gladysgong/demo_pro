#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import re_path
from . import views

app_name = 'picEval'
urlpatterns = [
    # re_path(r'^debug/$', views.post),
    re_path(r'^pic/$', views.post1),
    re_path(r'^pic/cancel', views.cancel),
    # re_path(r'^pic/detail_(?P<task_id>\d+).html$', views.detail),
    re_path(r'^pic/detail/$', views.detail),
    re_path(r'^pic/log_(?P<task_id>\d+).html$', views.log),
    # re_path(r'^debug/del', views.debug_del),
    # re_path(r'^debug/diff$', views.debug_diff),


]
