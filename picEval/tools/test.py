import requests
import base64
import os, json, sys, time
import pymysql
from datetime import datetime
import logging
from Editdistance import *

# 数据库配置
database_host = "10.141.21.129"
database_db = "evalplatform"
database_image = "picEval_imagetaskinfo"
database_result = "picEval_resultinfo"
database_user = "root"
database_pass = "noSafeNoWork@2019"

# 图片路径配置
# rootpath = r'/Users/apple/AnacondaProjects/demo_pro'
rootpath = r'/search/odin/daemon'
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

# ImageTaskInfo_id = int(sys.argv[1])
mission_id = int(sys.argv[1])
port_testocrip = sys.argv[2]
port_baseocrip = sys.argv[3]
port_testimgip = sys.argv[4]
port_baseimgip = sys.argv[5]
from_langs = sys.argv[6]
to_langs = sys.argv[7]
# status = int(sys.argv[8])

db = pymysql.connect(database_host, database_user, database_pass, database_db)
cursor = db.cursor()


class logutil():
    fname = ''

    def __init__(self, id):
        self.fname = datetime.now().strftime('%m%d%H%M%S') + '-' + str(id)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s : %(levelname)s  %(message)s',
            datefmt='%Y-%m-%d %A %H:%M:%S',
            filename='log/log-' + self.fname,
            filemode='a')

    def log_info(self, loginfo):
        logging.info(loginfo)

    def log_debug(self, loginfo):
        logging.debug(loginfo)

    def log_warning(self, loginfo):
        logging.warning(loginfo)

    def log_error(self, loginfo):
        logging.error(loginfo)

    def log_critical(self, loginfo):
        logging.critical(loginfo)


def get_now_time():
    timeArray = time.localtime()
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def update_errorlog(log):
    logstr = logutil(mission_id)
    # print(log.replace('\n', ''))
    log = log.replace("'", "\\'")

    sql = "UPDATE %s set errorlog=CONCAT(errorlog, '%s') where id=%d;" % (database_image, log, mission_id)

    cursor.execute(sql)
    data = cursor.fetchone()
    logstr.log_info(str(mission_id) + "\t" + log)
    try:
        db.commit()
    except:
        logstr.log_debug("update_errorlog failed.")
    return data


def get_imagetaskinfo():
    sql = "SELECT svIp, langs, env_type, status ,svPath FROM %s where id='%d'" % (database_image, mission_id)
    cursor.execute(sql)
    data = cursor.fetchone()
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        update_errorlog("[%s] Query table imagetaskinfo failed. \n" % (get_now_time()))

    return data

def update_imageTaskInfo(sum_num,finished,failed,img_diff_count,text_diff_count,text_base_count,path):
    sql_image = "UPDATE %s set end_time='%s', sum_num='%d',finished='%d',failed = '%d',img_diff_count='%d',text_diff_count = '%d',text_base_count = '%d' ,path='%s' where id=%d" % (
        database_image, get_now_time(), sum_num, finished, failed, img_diff_count, text_diff_count,text_base_count, path,mission_id)

    try:
        cursor.execute(sql_image)
        db.commit()
    except Exception as e:
        pass
    return 0

def insert_resultInfo(rankInfo,result,test_Img1,basepath,testpath,test_issuccess,base_issuccess,filename):
    sql_result = "INSERT INTO  %s(taskid_id,rankInfo,result,testImg,basepath,testpath,test_status,base_status,filename) values('%d','%d','%s','%s','%s','%s','%d','%d','%s')" % (
                            database_result, mission_id, rankInfo, pymysql.escape_string(result), test_Img1, basepath,
                            testpath, test_issuccess, base_issuccess, filename)
    try:
        cursor.execute(sql_result)
        db.commit()
    except Exception as e:
        pass
    return 0


def set_startStatus(sum_num, status):
    sql = "UPDATE %s set start_time='%s', sum_num='%d', status='%d' where id=%d" % (database_image, get_now_time(),sum_num, status, mission_id)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        update_errorlog("[%s] Update status [%d] failed. \n" % (get_now_time(), status))
    return 0

def set_endStatus(status):
    sql = "UPDATE %s set end_time='%s', status='%d' where id=%d" % (database_image, get_now_time(), status, mission_id)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        update_errorlog("[%s] Update status [%d] failed. \n" % (get_now_time(), status))
    return 0


def set_pid(pid):
    sql = "UPDATE %s set pid='%s' where id=%d" % (database_image,pid,mission_id)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        update_errorlog("[%s] Insert pid failed. \n" % (get_now_time()))
    return 0


def imageTobase64(path):
    with open(path, 'rb') as f:
        image = base64.b64encode(f.read())
        image = image.decode('utf-8')
        return image


def post_ocr(mission_id, test_ocrip, base_ocrip, test_imgip, base_imgip, from_langs, to_langs):
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
    }

    PATH=rootpath + origin_secpath + from_langs + '/'

    sum_num = len(os.listdir(PATH))

    failed = 0
    finished = 0
    img_diff_count = 0
    text_diff_count = 0
    text_base_count = 0

    status_data=get_imagetaskinfo()

    parameters = json.loads(status_data[4])
    for k, v in parameters.items():
        update_errorlog("[%s] send parameters: [%s]---[%s]. \n" % (get_now_time(), k, v))

    if status_data[3] == int(7):
        set_startStatus(sum_num, status=8)
        update_errorlog("[%s] Port deploy: Post is running. \n" % (get_now_time()))

        path = rootpath + dest_secpath + str(mission_id)
        for filename in os.listdir(PATH):
            isStorePathExists = path + '/'+from_langs+'_'+to_langs +'/' + filename + '/'
            storePath = dest_secpath + str(mission_id)  + '/'+from_langs+'_'+to_langs+'/' + filename + '/'

            base64image = imageTobase64(PATH + filename)
            params_ocr = {
                'lang': from_langs,
                'image': base64image,
                'direction_detect': 'true'
            }
            resp_test = requests.post(test_ocrip, data=params_ocr, headers=headers)
            resp_base = requests.post(base_ocrip, data=params_ocr, headers=headers)

            ocr_test = resp_test.json()
            ocr_base = resp_base.json()

            if not os.path.exists(isStorePathExists):
                os.makedirs(isStorePathExists)

            with open(isStorePathExists + 'base_ocr.json', 'w') as store_base, open(isStorePathExists + 'test_ocr.json','w') as store_test:
                store_base.write(json.dumps(ocr_base))
                store_test.write(json.dumps(ocr_test))
                update_errorlog("[%s] insert success. \n" % (get_now_time()))

            test_issuccess = ocr_test['success']
            base_issuccess = ocr_base['success']

            if (test_issuccess == int(1) & base_issuccess == int(1)):
                finished += 1

                # 计算距离
                distance_data = json.loads(ReturnRes(ocr_test, ocr_base))

                if distance_data['img_diff_count'] != int(0):
                    img_diff_count += 1

                text_diff_count += distance_data['text_diff_count']
                text_base_count += distance_data['text_base_count']

                rankInfo = distance_data['sum_distance']
                result = json.dumps(distance_data['result'])

                test_Img1, testpath = post_image(from_langs, to_langs, base64image, test_imgip, filename, 'test',isStorePathExists,storePath)
                test_Img2, basepath = post_image(from_langs, to_langs, base64image, base_imgip, filename, 'base',isStorePathExists,storePath)

                # sql_result = "INSERT INTO  %s(taskid_id,rankInfo,result,testImg,basepath,testpath,test_status,base_status,filename) values('%d','%d','%s','%s','%s','%s','%d','%d','%s')" % (
                #     database_result, mission_id, rankInfo, pymysql.escape_string(result), test_Img1, basepath,
                #     testpath, test_issuccess, base_issuccess, filename)
                #
                # cursor.execute(sql_result)
                # db.commit()

                insert_resultInfo(rankInfo, result, test_Img1, basepath, testpath, test_issuccess, base_issuccess,filename)
                update_imageTaskInfo(sum_num, finished, failed, img_diff_count, text_diff_count, text_base_count, path)

            else:
                failed += 1
                insert_resultInfo(rankInfo=0, result='null', test_Img1=origin_secpath + from_langs + '/' + filename,basepath='null', testpath='null', test_issuccess=0,
                                  base_issuccess=0, filename=filename)

        set_endStatus(status=9)

        status_data = get_imagetaskinfo()
        if status_data[3] == 9:
            update_errorlog("[%s] Port deploy: The post [%s] to [%s] has been completed. \n" % (get_now_time(), from_langs, to_langs))
        return 1
    else:
        update_errorlog("[%s] Port deploy: Status is not assigned. \n" % (get_now_time()))
        set_endStatus(status=10)
        return 0


def post_image(from_langs, to_langs, base64image, url, filename, type, isStorePathExists, storePath):
    params_img = {
        'from': from_langs,
        'to': to_langs,
        'image': base64image,
        'result_type': 'text_image'
    }

    resp = requests.post(url, data=params_img)
    result = resp.json()

    testImg = origin_secpath + from_langs + '/' + filename
    path = ''

    if result['success'] == int(1):
        pic = result['pic']
        pic = base64.b64decode(pic)

        # filename = filename[:-4]
        #
        # isPath = rootpath + dest_secpath + from_langs + '_' + to_langs + '/' + filename + '/'
        # storePath = dest_secpath + from_langs + '_' + to_langs + '/' + filename + '/'
        # if not os.path.exists(isPath):
        #     os.makedirs(isPath)

        if type == 'test':
            with open(isStorePathExists + 'test_imgtrans.json', 'w') as store_test:
                store_test.write(json.dumps(result))

            file = open(isStorePathExists + 'test.jpg', 'wb')
            path = storePath + 'test.jpg'
            file.write(pic)
            # ResultInfo.objects.filter(id=ResultInfo_id).update(testpath=path)
            file.close()
        elif type == 'base':
            with open(isStorePathExists + 'base_imgtrans.json', 'w') as store_base:
                store_base.write(json.dumps(result))

            file = open(isStorePathExists + 'base.jpg', 'wb')
            path = storePath + 'base.jpg'
            file.write(pic)
            # ResultInfo.objects.filter(id=ResultInfo_id).update(basepath=path)
            file.close()
        else:
            update_errorlog("[%s] [%s] of the image don't belong to base or test. \n" % (get_now_time(), filename))

        return testImg, path
    else:
        update_errorlog("[%s] [%s] of the image api [%s] failed. \n" % (get_now_time(), filename, type))
        return testImg, path

if __name__ == '__main__':
    # post_ocr('http://api.image.sogou/v1/ocr/basic.json', 'http://api.image.sogou/v1/ocr/basic.json', 'zh-CHS')
    # post_image('en', 'zh-CHS', base64, filename, url, type)
    pid=os.getpid()
    set_pid(pid)
    post_ocr(mission_id, port_testocrip, port_baseocrip, port_testimgip, port_baseimgip, from_langs, to_langs)
