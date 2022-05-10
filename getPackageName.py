#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom
import pandas as pd


#xmlPath= '/home/zhangxu/下载/114/resources/res/xml/compatible_rule.xml'
#xmlPath= '/media/zhangxu/disk/LenovoPM/app/src/main/res/xml/compatible_rule.xml'
#xmlPath= '/home/zhangxu/下载/test/compatible_rule.xml'
xmlPath= '/media/zhangxu/disk/aosp-11-GSI/vendor/lenovo/productivity/service/res/xml/compatible_rule.xml'
path = '/home/zhangxu/下载/'
packageNames = []

# 使用minidom解析器打开 XML 文档
#DOMTree = xml.dom.minidom.parse(path+ 'compatible_rule_lgsi.xml')
DOMTree = xml.dom.minidom.parse(xmlPath)
collection = DOMTree.documentElement
# 在集合中获取所有package
packages = collection.getElementsByTagName('package')


file_handle=open('/home/zhangxu/下载/packageName.xlsx',mode='w')
for package in packages:
    packageName=package.getAttribute('app:packageName')
    #print ('\033[1;35m  包名:  ' + packageName)
    packageNames.append(packageName)
    file_handle.write(packageName +'\n')


	
file_handle.close()
print ('\033[1;35mcompatible_rule文件中配置包名数量:' + str(len(packages)))

#read_excel()用来读取excel文件，记得加文件后缀
data = pd.read_excel(path + 'P12 需要删除的应用.xlsx',sheet_name = 1)
for index, value in data.iterrows():
    pag = value.values
    packageName = pag[2]
    print (packageName)
    for parent_node in packages:
        if parent_node.getAttribute("app:packageName") == packageName:
            collection.removeChild(parent_node)

     #i = packageNames.index(packageName)
     #xmlDoc=loadXMLDoc(xmlPath)
     #y=DOMTree.getElementsByTagName("package")[i]
     #DOMTree.documentElement.removeChild(y)
     #print (i)
     
try:
     with open(xmlPath,'w') as fh:
        DOMTree.writexml(fh,indent='',addindent='\t',newl='\n',encoding='UTF-8')
        print('OK')
except Exception as err:
    print('错误：{err}'.format(err=err))
