# coding=utf-8
import argparse
import os
import xml.etree.ElementTree as etree
import pretty_xml

parser = argparse.ArgumentParser(description="Demo of argparse")
parser.add_argument('--idst',  default="podlsq.xml")
parser.add_argument('--freq',  default="LC")
parser.add_argument('--mode',  default="L12")
parser.add_argument('--short', default="600")
parser.add_argument('--jump',  default="80")
parser.add_argument('--bad',   default="80")

args = parser.parse_args()
print(args)

crt_path = os.getcwd()
inp_path = os.path.join(args.idst)
out_path = os.path.join(args.idst)

# 获取tree 对象
tree = etree.parse(inp_path)
# 获取根节点
config = tree.getroot()

#<editres>
#	<freq>        L2  </freq>       <!-->  LC / L1 / L2 / L3 / L4 / L5 <!-->
#   <mode>        L12 </mode>       L12,L13
#   <short_elisp> 600 </short_elisp>
#   <jump_elisp>  80  </jump_elisp> <!--> 80 / 40 <!-->
#   <bad_elisp>   80  </bad_elisp>  <!--> 80 / 40 <!-->
#</editres>

editres = config.find("editres")
editres.find("freq").text = args.freq
editres.find("short_elisp").text = args.short
editres.find("jump_elisp").text = args.jump
editres.find("bad_elisp").text = args.bad
editres.find("mode").text = args.mode

# ===================================  creat gen node ====================================
#config = pretty_xml.prettyXml(config, '\t', '\n')
# 回写xml数据
tree.write(inp_path, encoding='utf-8', xml_declaration=True)
