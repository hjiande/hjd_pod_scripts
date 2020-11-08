# coding=utf-8
# brief : 用来创建 preedit app 的xml文件
import argparse
import os
import gns_pod_tool as tool
import gns_sum_orbdif as sum_dif
import sys
import glog

parser = argparse.ArgumentParser(description="Demo of argparse")
parser.add_argument('--year', '-yr', '-yyyy', default='2018')
parser.add_argument('--idoy', default='001')
parser.add_argument('--ilen', default='001') # 只测试过1天解

args = parser.parse_args()
print(args) # 输出传入参数

glog.setLevel("ERROR")  # 只输出错误信息和提示信息

doy_xml = ""
mod_xml = "/workfs/jdhuang/great_projects/e_all/scripts/great/gnss_pod_e_15_if_ecom2_merge.xml"  # model xml
scp_dir = "/workfs/jdhuang/great_projects/e_all/scripts/great"                                   # scripts dir
prj_dir = "/workfs/jdhuang/great_projects/e_all/if_15_ecom2_merge"                               # project dir
xml_dir = "/workfs/jdhuang/great_projects/e_all/if_15_ecom2_merge/xml"                           # xml file for each day, format is yyyydoy.xml
prj_log = "/workfs/jdhuang/great_projects/e_all/log_12"                                          # 周跳探测的log文件
bin_dir = "/project/jdhuang/GNSS_software/GREAT/pod_edit_gnss/build/Bin"                         # bin dir for great or other app
prd_dir = "./result"                                                                             # result dir for saving products
log_dir = "./logInfo"                                                                            # log dir for app and cmd log file
python_version = "python3.7"                                                                     # python version

year ='%04s' % args.year    # 打印为yyyy的格式
idoy ='%03s' % args.idoy    # 打印为doy的格式,右对齐补零
ilen = args.ilen

yeardoy = "%04s%03s" % (year, idoy)
ics = "grt" + yeardoy + ".ics"
car = "grt" + yeardoy + ".car"
cas = "grt" + yeardoy + ".cas"
orb = "grt" + yeardoy + ".orb"
ion = "grt" + yeardoy + ".ion"
con = "grt" + yeardoy + ".con"
rcv = "grt" + yeardoy + ".rcv"
dif = "orbdif" + yeardoy
pre_app_log = "great_preedit.app_log"
int_app_log = "great_oi.app_log"
lsq_app_log = "great_podlsq.app_log"
pos_app_log = "great_editres.app_log"
fit_app_log = "great_orbfit.app_log"
dif_app_log = "great_orbdif.app_log"
con_app_log = "great_ambfixDd.app_log"

# change dir
tool.check_path(xml_dir)
tool.check_path(prj_dir)
tool.check_path(prj_log)
prj_dir = os.path.join(prj_dir, '%4s' % args.year)
prj_log = os.path.join(prj_log, '%4s' % args.year)
tool.check_path(prj_dir)
tool.check_path(prj_log)
prj_dir = os.path.join(prj_dir, '%03s' % args.idoy)
prj_log = os.path.join(prj_log, '%03s' % args.idoy)
tool.check_path(prj_dir)
tool.check_path(prj_log)

os.chdir(prj_dir)
os.system("rm -r ./*")
os.system("mkdir ./log_tb")
os.system("cp -rf %s/* ./log_tb" % prj_log) # 将统一存放的log文件粘贴到prj路径下
tool.check_path(prd_dir)
tool.check_path(log_dir)
glog.fatal("crt dir is : " + os.getcwd())

# create the xml file
glog.fatal("=========>  beg GNS POD IF.")
glog.fatal("==========> beg create the xml file.")
doy_xml = os.path.join(xml_dir, "gns_pod_%4s%03d.xml" % (args.year, int(args.idoy)))
create_xml_py = os.path.join(scp_dir, "gns_xml_create_xml.py")
update_xml_py = os.path.join(scp_dir, "gns_xml_update_editres.py")
update_ambfix_xml_py = os.path.join(scp_dir, "gns_xml_update_ambfix.py")
os.system("chmod +x " + create_xml_py)
os.system("chmod +x " + update_xml_py)
os.system("chmod +x " + update_ambfix_xml_py)

glog.fatal("==========> creat xml.")
tool.run_py_cmd(python_version=python_version, python_name=create_xml_py, log_dir=log_dir, log_name="create_xml.cmd_log", year=year, idoy=idoy, ilen=1, idst=mod_xml, odst=doy_xml)
# first, check out the src and bin, if not bin, we cmake and make it

# second, preedit
glog.fatal("==========> beg preedit.")
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_preedit", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_preedit.cmd_log")
tool.run_cp_cmd(prj_dir, ics, prd_dir, "_pre")
tool.run_cp_cmd(prj_dir, pre_app_log, log_dir, "_pre")

# third, oi with the preedit ics
glog.fatal("==========> beg oi pre.") 
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_oi", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_oi_pre.cmd_log")
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_orbdif", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_orbdif_pre.cmd_log")
tool.run_cp_cmd(prj_dir, orb, prd_dir, "_pre")
tool.run_cp_cmd(prj_dir, dif, prd_dir, "_pre")
tool.run_cp_cmd(prj_dir, int_app_log, log_dir, "_pre")
tool.run_cp_cmd(prj_dir, dif_app_log, log_dir, "_pre")

# forth, orbfit the orb file with the brdm file
glog.fatal("==========> beg orbfit")
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_orbfit", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_orbfit.cmd_log")
tool.run_cp_cmd(prj_dir, ics, prd_dir, "_fit")
tool.run_cp_cmd(prj_dir, fit_app_log, prj_dir, "_fit")

# fifth, oi with the orbfit ics
glog.fatal("==========> beg oi fit.")
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_oi", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_oi_fit.cmd_log")
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_orbdif", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_orbdif_fit.cmd_log")
tool.run_cp_cmd(prj_dir, orb, prd_dir, "_fit")
tool.run_cp_cmd(prj_dir, dif, prd_dir, "_fit")
tool.run_cp_cmd(prj_dir, int_app_log, log_dir, "_fit")
tool.run_cp_cmd(prj_dir, dif_app_log, log_dir, "_fit")

# sixth, lsq and oi there thimes
# ========================================== 1st
# glog.fatal("==========> beg pod lsq pre.")
# tool.run_grt_cmd(app_dir=bin_dir, app_name="great_podlsq", xml_path=doy_xml, log_dir=log_dir,
                 # log_name="great_podlsq_flt.cmd_log", brdm="")
# glog.fatal("==========> beg oi pod lsq pre.")
# tool.run_grt_cmd(app_dir=bin_dir, app_name="great_oi", xml_path=doy_xml, log_dir=log_dir,
                 # log_name="great_oi_flt.cmd_log")
# glog.fatal("==========> beg orbdif after pod lsq")
# tool.run_grt_cmd(app_dir=bin_dir, app_name="great_orbdif", xml_path=doy_xml, log_dir=log_dir,
                 # log_name="great_orbdif_flt.cmd_log")

# ========================================== check orbdif to smooth
glog.fatal("==========> beg pod lsq 1st.")
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_podlsq", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_podlsq_lsq1.cmd_log", brdm="")
glog.fatal("==========> beg oi.")
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_oi", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_oi_lsq1.cmd_log")
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_orbdif", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_orbdif_lsq1.cmd_log")

tool.run_cp_cmd(prj_dir, ics, prd_dir, "_lsq1")
tool.run_cp_cmd(prj_dir, orb, prd_dir, "_lsq1")
tool.run_cp_cmd(prj_dir, rcv, prd_dir, "_lsq1")
tool.run_cp_cmd(prj_dir, car, prd_dir, "_lsq1")
tool.run_cp_cmd(prj_dir, cas, prd_dir, "_lsq1")
tool.run_cp_cmd(prj_dir, dif, prd_dir, "_lsq1")
tool.run_cp_cmd(prj_dir, lsq_app_log, log_dir, "_lsq1")
tool.run_cp_cmd(prj_dir, int_app_log, log_dir, "_lsq1")
tool.run_cp_cmd(prj_dir, dif_app_log, log_dir, "_lsq1")

# update editres
glog.fatal("==========> beg editres.")
tool.run_py_cmd(python_version=python_version, python_name=update_xml_py, log_dir=log_dir,
                log_name="gns_xml_update_xml_lsq1.cmd_log", idst=doy_xml, freq="LC", short=600, jump=80, bad=80)
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_editres", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_editres_lsq1.cmd_log")
tool.run_cp_cmd(prj_dir, pos_app_log, log_dir, "_lsq1")

# ========================================== 2nd
glog.fatal("==========> beg podlsq 2nd.")
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_podlsq", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_podlsq_lsq2.cmd_log")
glog.fatal("==========> beg oi.")
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_oi", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_oi_lsq2.cmd_log")
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_orbdif", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_orbdif_lsq2.cmd_log")
tool.run_cp_cmd(prj_dir, ics, prd_dir, "_lsq2")
tool.run_cp_cmd(prj_dir, orb, prd_dir, "_lsq2")
tool.run_cp_cmd(prj_dir, rcv, prd_dir, "_lsq2")
tool.run_cp_cmd(prj_dir, car, prd_dir, "_lsq2")
tool.run_cp_cmd(prj_dir, cas, prd_dir, "_lsq2")
tool.run_cp_cmd(prj_dir, dif, prd_dir, "_lsq2")
tool.run_cp_cmd(prj_dir, lsq_app_log, log_dir, "_lsq2")
tool.run_cp_cmd(prj_dir, int_app_log, log_dir, "_lsq2")
tool.run_cp_cmd(prj_dir, dif_app_log, log_dir, "_lsq2")

glog.fatal("=========> beg check orbdif")
sum_dif.smooth_with_orbdif(prj_dir, xml_dir, year, idoy)

# update editres
glog.fatal("==========> beg editres.")
tool.run_py_cmd(python_version=python_version, python_name=update_xml_py, log_dir=log_dir,
                log_name="gns_xml_update_xml_lsq2.cmd_log", idst=doy_xml, freq="LC", short=600, jump=40, bad=40)
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_editres", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_editres_lsq2.cmd_log")
tool.run_cp_cmd(prj_dir, pos_app_log, log_dir, "_lsq2")

# ========================================== 3rd
glog.fatal("==========> beg podlsq 3rd.")
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_podlsq", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_podlsq_lsq3.cmd_log")
glog.fatal("==========> beg oi.")
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_oi", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_oi_lsq3.cmd_log")
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_orbdif", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_orbdif_lsq3.cmd_log")
tool.run_cp_cmd(prj_dir, ics, prd_dir, "_lsq3")
tool.run_cp_cmd(prj_dir, orb, prd_dir, "_lsq3")
tool.run_cp_cmd(prj_dir, rcv, prd_dir, "_lsq3")
tool.run_cp_cmd(prj_dir, car, prd_dir, "_lsq3")
tool.run_cp_cmd(prj_dir, cas, prd_dir, "_lsq3")
tool.run_cp_cmd(prj_dir, dif, prd_dir, "_lsq3")
tool.run_cp_cmd(prj_dir, lsq_app_log, log_dir, "_lsq3")
tool.run_cp_cmd(prj_dir, int_app_log, log_dir, "_lsq3")
tool.run_cp_cmd(prj_dir, dif_app_log, log_dir, "_lsq3")

# update editres
glog.fatal("==========> beg editres.")
tool.run_py_cmd(python_version=python_version, python_name=update_xml_py, log_dir=log_dir,
                log_name="gns_xml_update_xml_lsq3.cmd_log", idst=doy_xml, freq="LC", short=600, jump=40, bad=40)
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_editres", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_editres_lsq3.cmd_log")
tool.run_cp_cmd(prj_dir, pos_app_log, log_dir, "_lsq3")

# seventh, ambfix
# glog.fatal("==========> beg podlsq fix.")
# glog.fatal("==========> beg podlsq to get amb.")
# tool.run_grt_cmd(app_dir=bin_dir, app_name="great_podlsq", xml_path=doy_xml, log_dir=log_dir,
                 # log_name="great_podlsq_lsq4.cmd_log")
# tool.run_cp_cmd(prj_dir, lsq_app_log, log_dir, "_lsq4")

glog.fatal("==========> beg update xml to 30.")
tool.run_py_cmd(python_version=python_version, python_name=update_ambfix_xml_py, log_dir=log_dir,
                log_name="gns_xml_update_ambfix_30.cmd_log", idst=doy_xml, int=30)

glog.fatal("==========> beg ambfixDd.")
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_ambfixDd", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_ambfixDd.cmd_log")

glog.fatal("==========> beg update xml to 300.")
tool.run_py_cmd(python_version=python_version, python_name=update_ambfix_xml_py, log_dir=log_dir,
                log_name="gns_xml_update_ambfix_300.cmd_log", idst=doy_xml, int=300)

glog.fatal("==========> beg podlsq fix with ambcon.")
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_podlsq", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_podlsq_fix.cmd_log", ambfix="")
glog.fatal("==========> beg oi.")
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_oi", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_oi_fix.cmd_log")
tool.run_cp_cmd(prj_dir, ics, prd_dir, "_fix")
tool.run_cp_cmd(prj_dir, orb, prd_dir, "_fix")
tool.run_cp_cmd(prj_dir, rcv, prd_dir, "_fix")
tool.run_cp_cmd(prj_dir, car, prd_dir, "_fix")
tool.run_cp_cmd(prj_dir, cas, prd_dir, "_fix")
tool.run_cp_cmd(prj_dir, con, prd_dir, "_fix")
tool.run_cp_cmd(prj_dir, con_app_log, log_dir, "_fix")
tool.run_cp_cmd(prj_dir, lsq_app_log, log_dir, "_fix")
tool.run_cp_cmd(prj_dir, int_app_log, log_dir, "_fix")


# eighth, lsq with ambfix, the oi and orbdif
glog.fatal("==========> beg orbdif.")
tool.run_grt_cmd(app_dir=bin_dir, app_name="great_orbdif", xml_path=doy_xml, log_dir=log_dir,
                 log_name="great_orbdif_fix.cmd_log")
tool.run_cp_cmd(prj_dir, dif, prd_dir, "_fix")
tool.run_cp_cmd(prj_dir, dif_app_log, log_dir, "_fix")
# plot and check result
glog.fatal("==========> run finshed for " + yeardoy + " ===================================")
