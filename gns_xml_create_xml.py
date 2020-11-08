# coding=utf-8
# brief : 用来创建 preedit app 的xml文件
import argparse
import os
import glog
import xml.etree.ElementTree as etree

import grt_norm_file_name as norm_name
import pretty_xml
import timeLib

parser = argparse.ArgumentParser(description="Demo of argparse")
parser.add_argument('--year', '-yr', '-yyyy', default='2019')
parser.add_argument('--idoy', default='001')
parser.add_argument('--ilen', default='001')
parser.add_argument('--idst', default="./gnss_pod.xml")
parser.add_argument('--odst', default="./podlsq.xml")

args = parser.parse_args()
print(args)

crt_path = os.getcwd()
inp_path = os.path.join(args.idst)
out_path = os.path.join(args.odst)

year = int(args.year)
idoy = int(args.idoy)
ilen = int(args.ilen)
beg_mm = timeLib.mm(year, idoy)
beg_dd = timeLib.dd(year, idoy)
end_mm = timeLib.mm(year, idoy + ilen - 1)
end_dd = timeLib.dd(year, idoy + ilen - 1)

print("read inp xml file")
# 获取tree 对象
tree = etree.parse(inp_path)
# 获取根节点
config = tree.getroot()

# ===================================  creat gen node ====================================
# Element(标签名):创建标签节点对象
print("rewrite gen node")
gen = config.find('gen')
gen_beg = gen.find('beg')
gen_end = gen.find('end')

# 添加gen标签值
# 2018-01-01 00:00:00
gen_beg.text = '%4s-%2s-%2s 00:00:00' % (year, beg_mm, beg_dd)
gen_end.text = '%4s-%2s-%2s 23:55:00' % (year, end_mm, end_dd)

# ===================================  creat outputs node ====================================
# 添加outputs标签值
print("rewrite outputs node")
outputs = config.find('outputs')
for child in outputs:
    child.text = norm_name.norm(child.text, year, idoy)

# ===================================  creat inputs node ====================================
# 添加inputs标签值
print("rewrite inputs node")
inputs = config.find('inputs')
for child in inputs:
    # brdm file
    if child.tag == "rnn" or child.tag == "sp3":
        tmp_rnn = child.text
        child.text = ""
        for tmp in range(int(idoy) - 1, int(idoy) + int(ilen) + 1):
            child.text = child.text + " " + (norm_name.norm(tmp_rnn, year, tmp)).strip()
    elif child.tag == "rno" or child.tag == "flg" or child.tag == "flg13":
        format_name = child.text
        recs = config.find("gen").find("rec").text.split()
        child.text = "\n\t\t\t"
        line_count = 0
        line_format = 2 if len(format_name) < 15 else 5
        for rec in recs:
            rec = rec.lower()
            line_count = line_count + 1
            name = format_name.replace('-CEN-', rec)
            name = norm_name.norm(name, year, idoy).strip()
            child.text = child.text + " " + name
            if line_count % line_format == 0:
                child.text = child.text + "\n\t\t\t"
        child.text = child.text + "\n\t\t\t"
    else:
        child.text = norm_name.norm(child.text, year, idoy)

# ===================================  creat gen node ====================================
print("rewrite xml file")
config = pretty_xml.prettyXml(config, '\t', '\n')
# 回写xml数据
tree.write(out_path, encoding='utf-8', xml_declaration=True)
glog.info("creat xml finish : " + out_path)
