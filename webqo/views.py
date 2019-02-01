from django.shortcuts import render, HttpResponse
import time, json
import requests
from bs4 import BeautifulSoup
import difflib




def debug(request):
    if request.method == 'GET':
        return render(request, 'webqo/debug.html')

    elif request.method == 'POST':
        ret = {
            'status': True,
            'error': None,
            'data': None
        }
        inputHost = request.POST.get('inputHost')
        inputExpId = request.POST.get('inputExpId')
        query_from = request.POST.get('query_from')
        query = request.POST.get('query')

        if inputExpId == '':
            inputExpId = 0
        else:
            inputExpId = inputExpId

        if query_from == '':
            query_from = 0
        else:
            query_from = query_from

        query_from = hex(int(query_from)).split('0x')[1] + "^0^0^0^0^0^0^0^0"
        query_from = query_from.encode('utf-16LE')

        exp_id = hex(int(inputExpId)).split('0x')[1] + "^0^0^0^0^0^0^0^0"
        exp_id = exp_id.encode('utf-16LE')

        utf16_query = query.encode('utf-16LE', 'ignore')

        params = {
            'queryString': utf16_query,
            'queryFrom': query_from,
            'exp_id': exp_id
        }

        headers = {"Content-type": "application/x-www-form-urlencoded;charset=UTF-16LE"}

        try:
            resp = requests.post(inputHost, data=params, headers=headers)
            status = resp.reason
            if status != 'OK':
                ret['error'] = 'Error:未知的请求类型'
                ret['status'] = False
                return ret
            data = BeautifulSoup(resp.text,"html.parser")
            ret['data'] = data.prettify()

        except Exception as e:
            ret['error'] = "Error:" + str(e)
            ret['status'] = False
        return HttpResponse(json.dumps(ret))


def debug_diff(request):
    ret = {
        'status': True,
        'error': None,
        'data': None
    }
    inputHost = request.POST.get('inputHost')
    inputExpId = request.POST.get('inputExpId')
    query_from = request.POST.get('query_from')
    inputHost_diff = request.POST.get('inputHost_diff')
    inputExpId_diff = request.POST.get('inputExpId_diff')
    query_from_diff = request.POST.get('query_from_diff')
    query = request.POST.get('query')

    if inputExpId == '':
        inputExpId = 0
    else:
        inputExpId = inputExpId

    if inputExpId_diff == '':
        inputExpId_diff = 0
    else:
        inputExpId_diff = inputExpId_diff

    if query_from == '':
        query_from = 0
    else:
        query_from = query_from

    if query_from_diff == '':
        query_from_diff = 0
    else:
        query_from_diff = query_from_diff

    query_from = hex(int(query_from)).split('0x')[1] + "^0^0^0^0^0^0^0^0"
    query_from = query_from.encode('utf-16LE')

    query_from_diff = hex(int(query_from_diff)).split('0x')[1] + "^0^0^0^0^0^0^0^0"
    query_from_diff = query_from_diff.encode('utf-16LE')

    exp_id = hex(int(inputExpId)).split('0x')[1] + "^0^0^0^0^0^0^0^0"
    exp_id = exp_id.encode('utf-16LE')

    exp_id_diff = hex(int(inputExpId_diff)).split('0x')[1] + "^0^0^0^0^0^0^0^0"
    exp_id_diff = exp_id_diff.encode('utf-16LE')

    utf16_query = query.encode('utf-16LE', 'ignore')

    params = {
        'queryString': utf16_query,
        'queryFrom': query_from,
        'exp_id': exp_id
    }

    params_diff = {
        'queryString': utf16_query,
        'queryFrom': query_from_diff,
        'exp_id': exp_id_diff
    }

    headers = {"Content-type": "application/x-www-form-urlencoded;charset=UTF-16LE"}

    try:
        resp = requests.post(inputHost, data=params, headers=headers)
        resp_diff = requests.post(inputHost_diff, data=params_diff, headers=headers)
        status = resp.reason
        status_diff = resp_diff.reason
        if status != 'OK' or status_diff != 'OK':
            ret['error'] = 'Error:未知的请求类型'
            ret['status'] = False
            return ret
        data = BeautifulSoup(resp.text,"html.parser")
        data_diff = BeautifulSoup(resp_diff.text,"html.parser")
        diff = difflib.HtmlDiff()
        ret['data'] = diff.make_table(data.prettify().splitlines(), data_diff.prettify().splitlines()).replace('nowrap="nowrap"', '')
    except Exception as e:
        ret['error'] = "Error:" + str(e)
        ret['status'] = False
    return HttpResponse(json.dumps(ret))


def get_now_time():
    timeArray = time.localtime()
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


def str_dos2unix(input):
    return input.replace('\r\n', '\n').replace(' ', '')
