# coding=utf-8
# tool lib
import os
import subprocess
import logging
import glog
import sys


def check_log(file_name, key_word):
    glog.info("check log file for : " + file_name)
    if not os.path.exists(file_name):
        glog.error("There is not such file : " + file_name)
        return False
    try:
        with open(file_name, 'r') as fr:
            lines = fr.readlines()
            for line in lines:
                if key_word.upper() in line.upper():
                    glog.info("find key word : < " + key_word + " > in file : < " + file_name + " >")
                    return True
    except IOError:
        glog.error("Open error for file : " + file_name)
        return False
    else:
        glog.error("can not find normal end in : " + file_name)
        return False


def run_sh_cmd(cmd_id="", bin_dir="", cmd_bin="", cmd_par="", log_dir="./", cmd_log="cmd_log"):
    glog.info("start sh cmd : " + cmd_bin + " " + cmd_par)
    cmd_bin = os.path.join(bin_dir, cmd_bin)
    cmd_log = os.path.join(log_dir, cmd_log)

    logger = logging.getLogger()
    try:
        if not os.path.exists(log_dir):
            glog.warn("no dir : " + log_dir + " , create it!")
            os.mkdir(log_dir)
    except OSError:
        glog.error("can not create the dir :" + log_dir)
        sys.exit()
        return False

    cmd_pearl = cmd_bin + " " + cmd_par
    cmd = cmd_bin + " " + cmd_par + " > " + cmd_log
    try:
        result = subprocess.getstatusoutput(cmd)
    except OSError:
        glog.error("run failed for throw except.")
        sys.exit()

    if int(result[0]) is not 0:
        glog.error("id : " + cmd_pearl + " run failed, result is : " + result[1])
        sys.exit()
        return False
    else:
        glog.info("id : " + cmd_pearl + " run over ")
        return True


def run_cp_cmd(cp_dir="./", cp_file="", dst_dir="", cp_post="_save"):
    glog.info("start cp cmd : " + cp_file + " " + dst_dir)
    dst_file = cp_file + cp_post
    file = os.path.join(cp_dir, cp_file)
    dst = os.path.join(dst_dir, dst_file)

    if not os.path.exists(cp_dir):
        pwd = os.getcwd()
        glog.error("no such file : " + cp_file + " in dir : " + cp_dir)
        sys.exit()
        return False
    if not os.path.exists(dst_dir):
        try:
            os.mkdir(dst_dir)
        except OSError:
            glog.error("can not mkdir for throw except : " + dst_dir)
            sys.exit()
            return False
    if not os.path.exists(file):
        glog.error("no such file : " + file)
        sys.exit()
        return False

    cmd = "cp " + file + " " + dst
    try:
        result = subprocess.getstatusoutput(cmd)
    except OSError:
        glog.error("run failed for throw except.")

    if int(result[0]) is not 0:
        glog.error(" run failed : " + cmd + " , result is : " + result[1])
        sys.exit()
        return False
    else:
        glog.info(" run over : " + cmd)
        # glog.info(" run over : " + cmd + " , result is : " + result[1])
        return True


def run_py_cmd(python_version, python_name, log_dir="./", log_name="./py.log", **kwargs):

    glog.info("start python : " + python_name)
    cmd = python_version + " " + python_name

    tmp = " "
    for key in kwargs:
        tmp = tmp + "--" + key + "=" + str(kwargs[key]) + " "

    log_name = os.path.join(log_dir, log_name)

    cmd_pearl = cmd + tmp
    cmd = cmd + tmp + " > " + log_name
    try:
        glog.info("run cmd : " + cmd)
        result = subprocess.getstatusoutput(cmd)
    except OSError:
        glog.error("run failed for throw except.")

    if int(result[0]) is not 0:
        glog.error(" run failed : " + cmd_pearl + " , result is : " + result[1])
        sys.exit()
        return False
    else:
        glog.info(" run over   : " + cmd_pearl)
        return True


def run_grt_cmd(app_dir, app_name, xml_path, log_dir="./", log_name="./py.log", **kwargs):
    glog.info("start grt_cmd : " + app_name)
    cmd_log = os.path.join(log_dir, log_name)
    app_log = os.path.join("./", app_name + ".app_log")
    app_bin = os.path.join(app_dir, app_name)

    cmd = app_bin + " -x " + xml_path
    tmp = " "
    for key in kwargs:
        tmp = tmp + "-" + key + " " + str(kwargs[key]) + " "

    cmd_pearl = cmd + tmp
    cmd = cmd + tmp + " > " + cmd_log
    glog.info("cmd is : " + cmd_pearl)
    try:
        result = subprocess.getstatusoutput(cmd)
    except OSError:
        glog.error("run failed for throw except.")
        sys.exit()

    if int(result[0]) is not 0:
        glog.error(" run failed : " + cmd_pearl + " , result is : " + result[1])
        sys.exit()
        return False
    else:
        # print(os.getcwd())
        # mv_cmd = "mv ./" + app_name + ".app_log " + app_log
        # os.system(mv_cmd)
        # subprocess.check_call(mv_cmd)
        success = True
        if not check_log(app_log, "normal end") and not check_log(cmd_log, "normal end"):
            success = False
            glog.error("cmd: " + cmd_pearl + " failed while checking log file.")
            sys.exit()
        glog.info(" run over   : " + cmd_pearl)
        return True


def check_path(path="./"):
    try:
        if not os.path.exists(path):
            glog.info(path + " not exist, we make it.")
            os.mkdir(path)
        else:
            glog.info(path + " exist.")
    except OSError:
        glog.error("throw while check path : " + path)
        sys.exit()
