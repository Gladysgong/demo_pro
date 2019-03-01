import requests
import base64
import os, json


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

def base64_image(path):
    with open(path, 'rb') as f:
        image = base64.b64encode(f.read())
        image = image.decode('utf-8')
        return image

def post_ocr():
    module_path = os.path.dirname(__file__) + '/image/timg.jpg'
    image_base64 = base64_image(module_path)
    print(image_base64)
    headers = {
        # "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryUxMCPMZA6DRSoTyO",
        'Content-Type': "application/x-www-form-urlencoded",

    }

    # session = requests.session()

    params = {
        'lang': 'ja',
        'image': image_base64,
    }
    timeout=20000
    resp2 = requests.post('http://api.image.sogou/v1/ocr/basic.json', data=params, headers=headers,timeout=int(timeout))
    # resp2 = session.post('http://10.143.52.35:10098/v4/ocr/json', data=json.dumps(params), headers=headers,timeout=float(timeout))
    # resp = requests.post('http://api.image.sogou/v1/ocr/basic.json', data=params,headers=headers)
    print("ocr", resp2.text)


def post_image():

    # module_path = os.path.dirname(__file__) + '/image/timg.jpg'
    module_path = os.path.dirname(__file__)+'/image'
    # os.mkdir(module_path)
    print(module_path)
    pic_path = r'/Users/apple/AnacondaProjects/demo_pro/image/'


    for filename in os.listdir(pic_path):
        print(filename)
        image_base64 = base64_image(pic_path+filename)
        print(image_base64)
        # headers = {"Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary0COmad6TmBUZmkWm"}

        params = {
            'from': 'zh-CHS',
            'to': 'en',
            'image': image_base64,
            'result_type': 'image'
        }
        # resp = requests.post('http://10.143.52.35:10098/v4/ocr/json', data=params,headers=headers)
        resp = requests.post('http://api.image.sogou/v1/open/ocr_translate.json', data=params)
        result = resp.json()
        print("image", result)

        # result=json.dumps(resp.text)
        # print(result)
        pic = result['pic']
        pic = base64.b64decode(pic)
        print("pic", pic)
        dd='/Users/apple/AnacondaProjects/demo_pro/result/'

        if not os.path.exists(dd):
            os.makedirs(dd)
            file = open(dd+'timg_dest.jpg', 'wb')
            file.write(pic)
            file.close()


if __name__ == '__main__':
    # post_ocr()
    post_image()
