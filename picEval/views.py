from django.shortcuts import render, HttpResponse
from picEval.models import ResultInfo, ImageTaskInfo
# from rbac.models import UserInfo
import requests
import base64
import os, json,signal,time
from django.core import serializers
# from picEval.tools.test import post_ocr
from picEval.tools import pagination
from picEval.task import get_pic_ocr


# Create your views here.
# def picEval_detail():

def post1(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        curent_page = 1
        if page:
            curent_page = int(page)
        try:
            result_list = ImageTaskInfo.objects.order_by('-id')
            page_obj = pagination.Page(curent_page, len(result_list), 15, 5)
            data = result_list[page_obj.start:page_obj.end]
            page_str = page_obj.page_str("/picEval/pic?page=")
        except Exception as e:
            pass
        return render(request, 'picEval/post.html', {'result_image': data, 'page_str': page_str})
    elif request.method == 'POST':
        ret = {
            'status': True,
            'error': None,
            'data': None
        }
        env_type = request.POST.get('env_type')
        try:
            if env_type == '2':

                port_testocrip = request.POST.get('port_testocrip')
                port_baseocrip = request.POST.get('port_baseocrip')
                port_testimgip = request.POST.get('port_testimgip')
                port_baseimgip = request.POST.get('port_baseimgip')
                port_langs = request.POST.get('port_langs')
                port_tag = request.POST.get('port_tag')
                port_status = 7

                resp = ImageTaskInfo.objects.create(env_type=env_type, status=port_status,
                                                    langs=port_langs,
                                                    test_ocrip=port_testocrip, base_ocrip=port_baseocrip,
                                                    test_imgip=port_testimgip,
                                                    base_imgip=port_baseimgip, testtag=port_tag)
                ImageTaskInfo_id = resp.id
                langs = port_langs.split('_')
                from_langs = langs[0]
                to_langs = langs[1]

                r = get_pic_ocr.delay(ImageTaskInfo_id, port_testocrip, port_baseocrip, port_testimgip, port_baseimgip,
                                      from_langs, to_langs)

                return HttpResponse(json.dumps(ret))

            elif env_type == '1':
                deploy_ip = '10.141.21.129'
                deploy_path = request.POST.get('deploy_path')
                deploy_check = request.POST.getlist('deploy_check')
                deploy_tag = request.POST.get('deploy_tag')

                deploy_check=','.join(deploy_check)

                resp = ImageTaskInfo.objects.create(env_type=env_type, langs=deploy_check,
                                                    svIP=deploy_ip, svPath=deploy_path,
                                                    testtag=deploy_tag)

                return HttpResponse(json.dumps(ret))
            else:
                print('未知评测类型！')
        except Exception as e:
            ret['error'] = "Error:" + str(e)
            ret['status'] = False
        return HttpResponse(json.dumps(ret))


# def detail(request, task_id):
#     if request.method == 'GET':
#         result = ResultInfo.objects.filter(taskid_id=task_id)
#
#         imageTask = ImageTaskInfo.objects.filter(id=task_id)
#
#         # distance = []
#         # for e in result:
#         #     print(type(e.result))
#         #     x = json.loads(e.result)
#         #     for i in x:
#         #         for k, v in i.items():
#         #             print('k', k)
#         #             print('v', v)
#         #             distance.append(v)
#         # print(distance)
#
#         return render(request, 'picEval/detail.html', {'Result': result, 'ImageTask': imageTask})

def cancel(request):
    ret = {'status': True, 'error': None, 'data': None}
    try:
        task_id = request.POST.get('task_id')
        data=ImageTaskInfo.objects.get(id=task_id)
        if data.env_type==int(2):
            print()
            os.kill(int(data.pid),signal.SIGTERM)
            ImageTaskInfo.objects.filter(id=task_id).update(end_time=get_now_time(),status=6)

        else:
            ImageTaskInfo.objects.filter(id=task_id).update(status=6)
    except Exception as e:
        ret['error'] = 'error:' + str(e)
        ret['status'] = False
    return HttpResponse(json.dumps(ret))

def detail(request, task_id):
    if request.method == 'GET':
        data = dict()
        imageTask = ImageTaskInfo.objects.filter(id=task_id)
        image=ImageTaskInfo.objects.get(id=task_id)
        if image.finished==int(0) or image.failed==int(0):
            errorRate=0
        else:
            errorRate=round(float(image.failed/image.finished),2)
        if image.text_base_count==int(0) or image.text_diff_count==int(0):
            rowRate=0
        else:
            rowRate=round(float(image.text_diff_count/image.text_base_count),2)
        result = ResultInfo.objects.filter(taskid_id=task_id)
        data['reslut_lst'] = json.loads(serializers.serialize("json", result))
        print(data)
        for e in result:
            print(json.loads(e.result))
            x = json.loads(e.result)

            # for i in x:
            #     for k, v in i.items():
            #         print('k', k)
            #         print('v', v)

        # print('result',result)
        return render(request, 'picEval/detail.html',
                      {'data': data['reslut_lst'], 'Result': result, 'ImageTask': imageTask,'error':errorRate,'row':rowRate})


def log(request, task_id):
    if request.method == 'GET':
        result = ImageTaskInfo.objects.filter(id=task_id)
        return render(request, 'picEval/log.html', {'ImageTask': result})

def get_now_time():
    timeArray = time.localtime()
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
