#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom
import pandas as pd


xmlPath='/media/zhangxu/disk/LGSI/LenovoPM/service/res/xml/compatible_rule.xml'
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
    file_handle.write(packageName +'\t')
    compatibilitys = package.getElementsByTagName('compatibility')
    for compat in compatibilitys:
       flag = compat.getAttribute('app:flag')
       file_handle.write( flag + '\t')
    file_handle.write('\n' )


	
file_handle.close()
print ('\033[1;35mcompatible_rule文件中配置包名数量:' + str(len(packages)))