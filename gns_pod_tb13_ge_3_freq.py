# coding=utf-8
# brief : 用来创建 preedit app 的xml文件
import argparse
import os
import gns_pod_tool as tool
import sys
import glog
import gns_sum_orbdif as sum_dif

parser = argparse.ArgumentParser(description="Demo of argparse")
parser.add_argument('--year', '-yr', '-yyyy', default='2018')
parser.add_argument('--idoy', default='001')
parser.add_argument('--bin',  default='001')
parser.add_argument('--xml',  default='001')
parser.add_argument('--dir',  default='001')

args = parser.parse_args()
print(args)

glog.setLevel("ERROR")

doy_xml = ""
xml_dir = args.xml                      # xml file for each day, format is yyyydoy.xml
log_dir = args.dir
bin_dir = args.bin
grt_bin = "/project/jdhuang/GNSS_software/GREAT/great_pco_L3/build/Bin/"
scp_dir = "/workfs/jdhuang/great_projects/e_all/scripts/great"                              # scripts dir
mod_xml = "/workfs/jdhuang/great_projects/e_all/scripts/great/gnss_tb_ge_3_freq.xml"        # model xml
python_version = "python3.7"                                                                # python version

year ='%04s' % args.year
idoy ='%03s' % args.idoy

yeardoy = "%04s%03s" % (year, idoy)

# create the xml file
glog.fatal("==========> beg tb.")
doy_xml = os.path.join(xml_dir, "gns_tb_%4s%03d.xml" % (args.year, int(args.idoy)))
create_xml_py = os.path.join(scp_dir, "gns_xml_create_xml.py")
tool.run_py_cmd(python_version=python_version, python_name=create_xml_py, log_dir=log_dir,log_name="create_xml.cmd_log", year=year, idoy=idoy, ilen=1, idst=mod_xml, odst=doy_xml)


print(grt_bin)
print(doy_xml)
print(log_dir)
print(bin_dir)

work_dir = os.path.join(log_dir,year,idoy)
os.system("mkdir -p " + work_dir)
os.chdir(work_dir)

tool.run_grt_cmd(app_dir=grt_bin, app_name="great_tbedit", xml_path=doy_xml, log_dir="./", log_name="great_tbedit.cmd_log", snx="", sys="GE",L13="",dir=log_dir, bin=bin_dir)
