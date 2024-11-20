# 工具

import json
import os
from PyQt5.QtWidgets import *
from jinja2 import Environment,FileSystemLoader

# 从文件载入内容
def getFromFile(pathname):
    f = open(pathname,"r",encoding="UTF-8")
    outStr = f.read()
    f.close()
    return outStr

# 保存内容到文件
def saveToFile(pathname,content):
    f = open(pathname,"w",encoding="UTF-8")
    f.write(content)
    f.close()

# 寻找文件
def findFile(thedir,filename):
    pathname = None
    for root,dirs,files in os.walk(thedir):
        if filename in files:
            pathname = os.path.join(root,filename)
            break
    return pathname

# json解码
def jsonDecode(str1): return dict(json.loads(str1))

# json编码
def jsonEncode(dict1): return json.dumps(dict1,indent=4)

# json规范输出
def jsonFormatOut(data): return jsonEncode(jsonDecode(data))

# pyqt 子布局加到布局
def addPanelToParent(P:QLayout,parentP:QLayout):
    w = QWidget()
    w.setLayout(P)
    parentP.addWidget(w)

# jinja2 用模板引擎渲染并保存一个文档
def renderAndSaveDocs(pathname,savepathname,data:dict):
    env = Environment(loader=FileSystemLoader(searchpath="."))
    template = env.get_template(pathname)
    outDocs = template.render(data)
    saveToFile(savepathname,outDocs)