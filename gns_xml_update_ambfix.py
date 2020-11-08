# coding=utf-8
import argparse
import os
import xml.etree.ElementTree as etree
import pretty_xml

parser = argparse.ArgumentParser(description="Demo of argparse")
parser.add_argument('--idst',  default="podlsq.xml")
parser.add_argument('--int',   default="300")

args = parser.parse_args()
print(args)

crt_path = os.getcwd()
inp_path = os.path.join(args.idst)
out_path = os.path.join(args.idst)

# 获取tree 对象
tree = etree.parse(inp_path)
# 获取根节点
config = tree.getroot()

gen = config.find("gen")
gen.find("int").text = args.int

# ===================================  creat gen node ====================================
#config = pretty_xml.prettyXml(config, '\t', '\n')
# 回写xml数据
tree.write(inp_path, encoding='utf-8', xml_declaration=True)
