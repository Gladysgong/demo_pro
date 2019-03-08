#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from celery import shared_task, task
from celery import Celery
from demo_pro import celery_app
import os, traceback, time


@celery_app.task
def get_pic_ocr(ImageTaskInfo_id, port_testocrip, port_baseocrip, port_testimgip, port_baseimgip,
                from_langs, to_langs):
    try:
        # task_status = os.system('/root/anaconda3/bin/python3 /search/odin/pypro/webqa/utils/getdiff_byxml.py %d &' % task_id)
        task_status = os.system(
            '/Users/apple/AnacondaProjects/demo_pro/.env/bin/python /Users/apple/AnacondaProjects/demo_pro/picEval/tools/test.py %d %s %s %s %s %s %s&' % (
                int(ImageTaskInfo_id), port_testocrip, port_baseocrip, port_testimgip, port_baseimgip,
                from_langs, to_langs))

        # task_status = os.system('/Users/apple/AnacondaProjects/demo_pro/.env/bin/python /Users/apple/AnacondaProjects/demo_pro/picEval/tools/test.py')


    except Exception as e:
        print(e)
        traceback.print_exc()
        pass
    return task_status

# @celery_app.task
# def get_gpu_detail(runningid, req_id):
#     try:
#         task_status = os.system('python3 /search/odin/pypro/webqa/utils/monitor.py %s %s &' % (str(runningid), req_id))
#
#
#         # task_status = os.system('python3 /Users/zhangjingjun/work/code/webqa/utils/monitor.py %s %s &' % (str(runningid), req_id))
#     except Exception as e:
#         traceback.print_exc()
#         pass
#     return task_status
