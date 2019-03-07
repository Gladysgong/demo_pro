import requests
import base64
import os, json
from picEval.models import ImageTaskInfo, ResultInfo


# ocr接口：http://10.143.52.35:10098/v4/ocr/json
# 参数：lang，image=base64串
# 英文：en
# 中文：zh-CHS
# 日文：ja
# 韩文：ko
# 俄文：ru
# 法文：fr
# 西班牙文：es
# 德文：de
# 葡萄牙：pt
# 意大利：it

# 翻译回帖接口：http://api.image.sogou/v1/open/ocr_translate.json
# 参数：from、to、image、result_type=image

def imageTobase64(path):
    with open(path, 'rb') as f:
        image = base64.b64encode(f.read())
        image = image.decode('utf-8')
        return image


def post_ocr(ImageTaskInfo_id, test_ocrip, base_ocrip, test_imgip, base_imgip, from_langs, to_langs):
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
    }

    origin_rootpath = r'/Users/apple/AnacondaProjects/demo_pro'
    origin_secpath = r'/static/origin/'

    sum_num = len(os.listdir(origin_rootpath + origin_secpath))

    failed = 0
    finished = 0

    ImageTaskInfo.objects.filter(id=ImageTaskInfo_id).update(sum_num=sum_num)

    for filename in os.listdir(origin_rootpath + origin_secpath):
        base64image = imageTobase64(origin_rootpath + origin_secpath + filename)
        params_ocr = {
            'lang': from_langs,
            'image': base64image,
        }
        resp_test = requests.post(test_ocrip, data=params_ocr, headers=headers)
        resp_base = requests.post(base_ocrip, data=params_ocr, headers=headers)

        ocr_test = resp_test.json()
        ocr_base = resp_base.json()

        test_issuccess = ocr_test['success']
        base_issuccess = ocr_base['success']

        if (test_issuccess == int(1) & base_issuccess == int(1)):
            finished += 1
            ImageTaskInfo.objects.filter(id=ImageTaskInfo_id).update(finished=finished)
            distance()

        else:
            failed += 1
            ImageTaskInfo.objects.filter(id=ImageTaskInfo_id).update(failed=failed)

        resp = ResultInfo.objects.create(taskid_id=int(ImageTaskInfo_id), testImg=origin_secpath + filename,
                                         test_status=test_issuccess, base_status=base_issuccess)
        ResultInfo_id = resp.id

        post_image(ResultInfo_id, from_langs, to_langs, base64image, test_imgip, filename, 'test')
        post_image(ResultInfo_id, from_langs, to_langs, base64image, base_imgip, filename, 'base')

        distance(ocr_test, ocr_base)

        # y = x['result']
        # for i in y:
        #     for k, v in i.items():
        #         print('k',k)
        #         print('v',v)

        # y = xx['result']['content']
        # print(y)
        # z=json.loads(y.join())
        # print(z['content'])
        # # print(json.dumps(x['result']))

    return sum_num


def post_image(ResultInfo_id, from_langs, to_langs, base64image, url, filename, type):
    # module_path = os.path.dirname(__file__)
    # print(module_path)
    # pic_path = r'/Users/apple/AnacondaProjects/demo_pro/image/'
    # sum_num = len(os.listdir(pic_path))
    # for filename in os.listdir(pic_path):
    #     image_base64 = imageTobase64(pic_path + filename)
    #     print(image_base64)
    # headers = {"Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary0COmad6TmBUZmkWm"}

    params_img = {
        'from': from_langs,
        'to': to_langs,
        'image': base64image,
        'result_type': 'image'
    }

    # resp = requests.post('http://api.image.sogou/v1/open/ocr_translate.json', data=params_img)
    resp = requests.post(url, data=params_img)
    result = resp.json()
    pic = result['pic']
    pic = base64.b64decode(pic)
    root_path = '/Users/apple/AnacondaProjects/demo_pro'
    sec_path = '/static/dest/'

    if not os.path.exists(root_path + sec_path):
        os.makedirs(root_path + sec_path)

    if result['success'] == int(1):
        filename = filename[:-4]
        if type == 'test':
            file = open(root_path + sec_path + filename + '_test.jpg', 'wb')
            path = sec_path + filename + '_test.jpg'
            file.write(pic)
            ResultInfo.objects.filter(id=ResultInfo_id).update(testpath=path)
            file.close()
        elif type == 'base':
            file = open(root_path + sec_path + filename + '_base.jpg', 'wb')
            path = sec_path + filename + '_base.jpg'
            file.write(pic)
            ResultInfo.objects.filter(id=ResultInfo_id).update(basepath=path)
            file.close()
        else:
            print('回帖图请求类型未知！')
    return 0


def distance(result_test, result_base):
    x = 1
    y = 2
    return x, y


if __name__ == '__main__':
    # post_ocr('http://api.image.sogou/v1/ocr/basic.json', 'http://api.image.sogou/v1/ocr/basic.json', 'zh-CHS')
    # post_image('en', 'zh-CHS', base64, filename, url, type)
    pass
