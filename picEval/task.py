#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from celery import shared_task, task
from celery import Celery
from demo_pro import celery_app
import os, traceback, time


@celery_app.task
def get_pic_ocr(ImageTaskInfo_id, port_testocrip, port_baseocrip, port_testimgip, port_baseimgip,from_langs, to_langs):

    task_status=''
    try:
        # task_status = os.system(
        #     '/Users/apple/AnacondaProjects/demo_pro/.env/bin/python /Users/apple/AnacondaProjects/demo_pro/picEval/tools/test.py %d %s %s %s %s %s %s&' % (
        #     int(ImageTaskInfo_id), port_testocrip, port_baseocrip, port_testimgip, port_baseimgip, from_langs, to_langs))
        task_status = os.system(
            '/usr/bin/python /search/odin/daemon/evalpaltform/demo_pro/picEval/tools/test.py %d %s %s %s %s %s %s&' % (
                int(ImageTaskInfo_id), port_testocrip, port_baseocrip, port_testimgip, port_baseimgip, from_langs,to_langs))

    except Exception as e:
        print(e)
        traceback.print_exc()
        pass
    return task_status
