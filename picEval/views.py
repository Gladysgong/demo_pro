from django.shortcuts import render
from picEval.models import ResultInfo, ImageTaskInfo
from rbac.models import UserInfo
import requests
import base64
import os, json
from picEval.tools.test import post_ocr


# Create your views here.
# def picEval_detail():

def post1(request):
    if request.method == 'GET':
        data = ImageTaskInfo.objects.all()
        return render(request, 'picEval/post.html', {'result_image': data})
    elif request.method == 'POST':
        ret = {
            'status': True,
            'error': None,
            'data': None
        }
        env_type = request.POST.get('env_type')
        if env_type == '2':

            port_testocrip = request.POST.get('port_testocrip')
            port_baseocrip = request.POST.get('port_baseocrip')
            port_testimgip = request.POST.get('port_testimgip')
            port_baseimgip = request.POST.get('port_baseimgip')
            port_langs = request.POST.get('port_langs')
            port_tag = request.POST.get('port_tag')
            port_status = 7

            user = UserInfo.objects.get(username='gongyanli')
            resp = ImageTaskInfo.objects.create(username=user, env_type=env_type, status=port_status, langs=port_langs,
                                                test_ocrip=port_testocrip, base_ocrip=port_baseocrip,
                                                test_imgip=port_testimgip,
                                                base_imgip=port_baseimgip, testtag=port_tag)
            ImageTaskInfo_id = resp.id
            langs = port_langs.split('_')
            from_langs = langs[0]
            to_langs = langs[1]
            post_ocr(ImageTaskInfo_id, port_testocrip, port_baseocrip, port_testimgip, port_baseimgip, from_langs,
                     to_langs)
        elif env_type == '1':
            deploy_ip = '10.141.177.27'
            deploy_path = request.POST.get('deploy_path')
            deploy_check = request.POST.get('deploy_check')
            deploy_tag = request.POST.get('deploy_tag')

            user = UserInfo.objects.get(username='gongyanli')
            resp = ImageTaskInfo.objects.create(username=user, env_type=env_type, langs=deploy_check,
                                                svIp=deploy_ip, svPath=deploy_path,
                                                testtag=deploy_tag)

            ImageTaskInfo_id = resp.id
            print('deploy_check', deploy_check)

            # langs = port_langs.split('_')
            # from_langs = langs[0]
            # print(from_langs)
            # to_langs = langs[1]
            # post_ocr(ImageTaskInfo_id, port_testocrip, port_baseocrip, port_testimgip, port_baseimgip, from_langs,
            #          to_langs)
        else:
            print('未知评测类型！')

        return render(request, 'picEval/post.html')


def detail(request, task_id):
    if request.method == 'GET':
        result = ResultInfo.objects.filter(taskid_id=task_id)

        imageTask = ImageTaskInfo.objects.filter(id=task_id)

        # distance = []
        # for e in result:
        #     print(type(e.result))
        #     x = json.loads(e.result)
        #     for i in x:
        #         for k, v in i.items():
        #             print('k', k)
        #             print('v', v)
        #             distance.append(v)
        # print(distance)

        return render(request, 'picEval/detail.html', {'Result': result, 'ImageTask': imageTask})


def log(request, task_id):
    if request.method == 'GET':
        xx = ImageTaskInfo.objects.filter(id=task_id)
        print('tt',xx)

    return render(request, 'picEval/log.html',{'ImageTask': xx })
# def base64_image(path):
# with open(path, 'rb') as f:
#         image = base64.b64encode(f.read())
#         image = image.decode('utf-8')
#         return image
#
#
# def post_ocr():
#     module_path = os.path.dirname(__file__) + '/image/timg.jpg'
#     image_base64 = base64_image(module_path)
#     print(image_base64)
#     headers = {
#         # "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryUxMCPMZA6DRSoTyO",
#         'Content-Type': "application/x-www-form-urlencoded",
#
#     }
#
#     params = {
#         'lang': 'ja',
#         'image': image_base64,
#     }
#     timeout = 20000
#     resp2 = requests.post('http://api.image.sogou/v1/ocr/basic.json', data=params, headers=headers,
#                           timeout=int(timeout))
#     # resp2 = session.post('http://10.143.52.35:10098/v4/ocr/json', data=json.dumps(params), headers=headers,timeout=float(timeout))
#     # resp = requests.post('http://api.image.sogou/v1/ocr/basic.json', data=params,headers=headers)
#     print("ocr", resp2.text)
#
#
# def post_image():
#     module_path = os.path.dirname(__file__) + '/image/timg.jpg'
#     # print(module_path)
#     # image_base64 = base64_image(module_path)
#     # print(image_base64)
#     # # headers = {"Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary0COmad6TmBUZmkWm"}
#     #
#     # params = {
#     #     'from': 'zh-CHS',
#     #     'to': 'en',
#     #     'image': image_base64,
#     #     'result_type': 'image'
#     # }
#     # # resp = requests.post('http://10.143.52.35:10098/v4/ocr/json', data=params,headers=headers)
#     # resp = requests.post('http://api.image.sogou/v1/open/ocr_translate.json', data=params)
#     # result = resp.json()
#     # print("image", result)
#     #
#     # # result=json.dumps(resp.text)
#     # # print(result)
#     # pic = result['pic']
#     # pic = base64.b64decode(pic)
#     # print("pic", pic)
#     # file = open('timg_dest.jpg', 'wb')
#     # file.write(pic)
#     # file.close()
#     print(module_path)
#
#
# post_image()
