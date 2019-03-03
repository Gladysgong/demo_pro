#! /usr/bin/env python
# coding=utf-8

import os,time
import pexpect
from picEval.tools import logUtils


# def scp_data(file_path, newconfip, newconfuser, newconfpassw, newconfpath):
def scp_data(source_ip, source_path, source_user, source_pwd, deploy_path):
    # update_errorlog("[%s] try scp rd longdiff_query to test enviroment\n" % get_now_time())
    # if os.path.exists(file_path + "/longdiff/longdiff_query"):
    #     # update_errorlog("[%s] %s\n" % (get_now_time(), "long_diffquery  exists, del it"))
    #     os.popen("rm -rf " + file_path + "/longdiff/longdiff_query")

    passwd_key = '.*assword.*'

    cmdline = 'scp -r %s@%s:%s %s/' % (source_user, source_ip, source_path, deploy_path)
    try:
        child = pexpect.spawn(cmdline)
        expect_result = child.expect([r'assword:', r'yes/no'], timeout=30)
        if expect_result == 0:
            child.sendline(source_pwd)
            print('111')
        elif expect_result == 1:
            child.sendline('yes')
            child.expect(passwd_key, timeout=30)
            child.sendline(source_pwd)
            print('222')
        child.expect(pexpect.EOF)
    except Exception as e:
        update_errorlog("[%s] %s, scp rd long_diff failed \n" % (get_now_time(), e))
    update_errorlog("[%s] try scp rd longdiff_query to test enviroment success\n" % get_now_time())
    return 0

def get_now_time():
    timeArray = time.localtime()
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

def update_errorlog(log):
    # logstr = logUtils.logutil(mission_id)
    # # print(log.replace('\n', ''))
    # log = log.replace("'", "\\'")
    # sql = "UPDATE %s set errorlog=CONCAT(errorlog, '%s') where id=%d;" % (database_table, log, mission_id)
    # cursor.execute(sql)
    # data = cursor.fetchone()
    # logstr.log_info(str(mission_id) + "\t" + log)
    # try:
    #     db.commit()
    # except:
    #     logstr.log_debug("error")
    # return data
    pass


if __name__ == '__main__':
    scp_diff_conf("/search/a", "10.148.10.72", "root", "sogourank@2016", "")
    scp_diff_conf("/Users/apple/AnacondaProjects", "10.148.10.72", "root", "sogourank@2016", "/search/a")

