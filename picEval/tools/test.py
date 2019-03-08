import requests
import base64
import os, json, sys,time
import pymysql

# from picEval.models import ImageTaskInfo, ResultInfo
# from picEval.tools.conf import *

# 数据库配置
database_host = "10.134.120.30"
database_db = "demo_pro"
database_image = "picEval_imagetaskinfo"
database_result = "picEval_resultinfo"
database_user = "root"
database_pass = "Websearch@qa66"

# 图片路径配置
rootpath = r'/Users/apple/AnacondaProjects/demo_pro'
origin_secpath = r'/static/origin/'
dest_secpath = r'/static/dest/port/'

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

ImageTaskInfo_id = int(sys.argv[1])
port_testocrip = sys.argv[2]
port_baseocrip = sys.argv[3]
port_testimgip = sys.argv[4]
port_baseimgip = sys.argv[5]
from_langs = sys.argv[6]
to_langs = sys.argv[7]

db = pymysql.connect(database_host, database_user, database_pass, database_db)
cursor = db.cursor()


def get_now_time():
    timeArray = time.localtime()
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def imageTobase64(path):
    with open(path, 'rb') as f:
        image = base64.b64encode(f.read())
        image = image.decode('utf-8')
        return image


def post_ocr(mission_id, test_ocrip, base_ocrip, test_imgip, base_imgip, from_langs, to_langs):
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
    }

    origin_path = rootpath + origin_secpath + from_langs + '_' + to_langs + '/'
    ori_stroePaht = origin_secpath + from_langs + '_' + to_langs + '/'
    sum_num = len(os.listdir(origin_path))

    failed = 0
    finished = 0
    img_diff_count = 0
    text_diff_count = 0
    text_base_count = 0
    print('sum',sum_num)

    sql_sum = "UPDATE %s set sum_num='%d', status=8 where id=%d" % (database_image, sum_num, mission_id)
    cursor.execute(sql_sum)
    db.commit()
    # ImageTaskInfo.objects.filter(id=ImageTaskInfo_id).update(sum_num=sum_num)

    for filename in os.listdir(origin_path):
        base64image = imageTobase64(origin_path + filename)
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

            distance_data = distance(ocr_test, ocr_base)

            img_diff_count += distance_data['img_diff_count']
            text_diff_count += distance_data['text_diff_count']
            text_base_count += distance_data['text_base_count']

            rankInfo = distance_data['sum_distance']
            result = json.dumps(distance_data['result'])

            # resp = ResultInfo.objects.create(taskid_id=int(ImageTaskInfo_id), testImg=ori_stroePaht + filename,
            #                                  rankInfo=rankInfo, result=result, filename=filename,
            #                                  test_status=test_issuccess, base_status=base_issuccess)
            # ResultInfo_id = resp.id

            test_Img1, testpath = post_image(from_langs, to_langs, base64image, test_imgip, filename, 'test')
            test_Img2, basepath = post_image(from_langs, to_langs, base64image, base_imgip, filename, 'base')

            sql_result = "INSERT INTO  %s(taskid_id,rankInfo,result,testImg,basepath,testpath,test_status,base_status,filename) values('%d','%d','%s','%s','%s','%s','%d','%d','%s')" % (
                database_result, mission_id, rankInfo, pymysql.escape_string(result), test_Img1, basepath,
                testpath, test_issuccess, base_issuccess, filename)

            cursor.execute(sql_result)
            db.commit()

        else:
            failed += 1
            # ImageTaskInfo.objects.filter(id=ImageTaskInfo_id).update(failed=failed)

    # ImageTaskInfo.objects.filter(id=ImageTaskInfo_id).update(finished=finished, img_diff_count=img_diff_count,
    #                                                          text_diff_count=text_diff_count,
    #                                                          text_base_count=text_base_count,
    #                                                          status=8)

    sql_image = "UPDATE %s set end_time='%s', sum_num='%d',finished='%d',failed = '%d',img_diff_count='%d',text_diff_count = '%d',text_base_count = '%d',status=9 where id=%d" % (
        database_image, get_now_time(), sum_num, finished, failed, img_diff_count, text_diff_count,
        text_base_count,
        mission_id)

    cursor.execute(sql_image)
    db.commit()

    return sum_num


def post_image(from_langs, to_langs, base64image, url, filename, type):
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
    path = ''

    isPath = rootpath + dest_secpath + from_langs + '_' + to_langs + '/' + filename + '/'
    storePath = dest_secpath + from_langs + '_' + to_langs + '/' + filename + '/'

    if not os.path.exists(isPath):
        os.makedirs(isPath)

    if result['success'] == int(1):

        testImg = origin_secpath + from_langs + '_' + to_langs + '/' + filename
        filename = filename[:-4]

        if type == 'test':
            file = open(isPath + filename + '_test.jpg', 'wb')
            path = storePath + filename + '_test.jpg'
            file.write(pic)
            # ResultInfo.objects.filter(id=ResultInfo_id).update(testpath=path)
            file.close()
        elif type == 'base':
            file = open(isPath + filename + '_base.jpg', 'wb')
            path = storePath + filename + '_base.jpg'
            file.write(pic)
            # ResultInfo.objects.filter(id=ResultInfo_id).update(basepath=path)
            file.close()
        else:
            print('回帖图请求类型未知！')
        return testImg, path
    else:
        return 0


def distance(result_test, result_base):
    json = {
        'img_diff_count': 1,
        'text_diff_count': 4,
        'text_base_count': 5,
        'sum_distance': 1,
        'rankInfo': 2,
        'result': [
            {
                "basecontent": "aaa",
                "testcontent": "bbb",
                "distance": "ccc",
            }, {
                "basecontent": "ddd",
                "testcontent": "eee",
                "distance": "fff",
            }
        ]
    }

    return json


def a():
    print('test!')


if __name__ == '__main__':
    # post_ocr('http://api.image.sogou/v1/ocr/basic.json', 'http://api.image.sogou/v1/ocr/basic.json', 'zh-CHS')
    # post_image('en', 'zh-CHS', base64, filename, url, type)
    post_ocr(ImageTaskInfo_id, port_testocrip, port_baseocrip, port_testimgip, port_baseimgip, from_langs, to_langs)
    # a()
