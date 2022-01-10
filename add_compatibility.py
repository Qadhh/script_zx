#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import pandas as pd
from xml.dom.minidom import parse
import xml.dom.minidom
import os, sys,time,os.path,shutil,argparse
from collections import Counter

path = '/home/zhangxu/下载/'
xmlPath= '/media/zhangxu/disk/aosp-11-GSI/vendor/lenovo/productivity/service/res/xml/compatible_rule.xml'
findPackages = []
excleRepeatPackages = []
flag512 = 0
flag128 = 0
newPackage = 0
repeat = 0 
newrepeat = 0
excleRepeatPackage = 0


# 使用minidom解析器打开 XML 文档
DOMTree = xml.dom.minidom.parse(xmlPath)
collection = DOMTree.documentElement
# 在集合中获取所有package
packages = collection.getElementsByTagName('package')

for package in packages:
   packageName=package.getAttribute('app:packageName')
   if packageName in findPackages :
       repeat = repeat + 1
       print('\033[1;31m compatible_rule重复设置兼容性：' + packageName + ': 存在' +  '\033[0m')
       continue
   findPackages.append(packageName)
   compatibilitys = package.getElementsByTagName('compatibility')
   for compat in compatibilitys:
       flag = compat.getAttribute('app:flag')
       if flag == '512':
           flag512 = flag512 + 1
       if flag == '128':
           flag128 = flag128 + 1
print ('\033[1;35mcompatible_rule文件中重复配置数量:' + str(repeat))
print ('\033[1;32mcompatible_rule文件中配置的512数量:' + str(flag512))
print ('compatible_rule文件中配置的128数量:' + str(flag128)+ '\033[0m ')

#在内存中创建一个空的文档
doc = xml.dom.minidom.Document()
#创建一个根节点compatibleRuleList对象
root = doc.createElement('compatibleRuleList')
doc.appendChild(root)
#read_excel()用来读取excel文件，记得加文件后缀
data = pd.read_excel(path + 'p12-pro_207.xlsx',sheet_name = 0)
#列数
ncols = data.columns.size
print('列数:' +str(ncols))
#行数
nrows = data.shape[0]
print('行数:' +str(nrows))
#print(data)
#print(data.columns.tolist())
for index, value in data.iterrows():
    #index 是行号，value是一行数据的列表
    #print(index, value)
    pag = value.values
    #print(pag[2])
    if pag[2] in excleRepeatPackages :
        print ('excle 重复的包名为 + :'+ pag[2] )
        excleRepeatPackage = excleRepeatPackage + 1
        continue
    excleRepeatPackages.append(pag[2])
    if pag[2] in findPackages :
        #print('\033[1;31m' + pag[0] + ':  存在' + '\033[0m ')
        newPackage = newPackage + 1
        continue
    elif pag[3] == 0 :
        continue
    #创建package子节点
    package=doc.createElement('package')
    #添加到更节点
    root.appendChild(package)
    #设置子节点内容
    #print(pag[2])
    package.setAttribute('app:packageName', pag[2])
    com_node1=doc.createElement('compatibility')
    com_node1.setAttribute('app:flag','1024')
    com_node1.setAttribute('app:versioinRestrict','0')
    com_node1.setAttribute('app:version','0')
    package.appendChild(com_node1)
    #print('pag[5] :' + pag[5])
    if pag[3] == '默认全屏':
        com_node2=doc.createElement('compatibility')
        com_node2.setAttribute('app:flag','512')
        com_node2.setAttribute('app:versioinRestrict','0')
        com_node2.setAttribute('app:version','0')
        package.appendChild(com_node2)
        continue
   
    if pag[5] == '否' :
        com_node4=doc.createElement('compatibility')
        com_node4.setAttribute('app:flag','2048')
        com_node4.setAttribute('app:versioinRestrict','0')
        com_node4.setAttribute('app:version','0')
        package.appendChild(com_node4)
    if pag[6] == '否' :
        com_node3=doc.createElement('compatibility')
        com_node3.setAttribute('app:flag','128')
        com_node3.setAttribute('app:versioinRestrict','0')
        com_node3.setAttribute('app:version','0')
        package.appendChild(com_node3)
    
try:
    with open( path + 'test.xml','w') as fh:
        doc.writexml(fh,indent='',addindent='\t',newl='\n',encoding='UTF-8')
        print('OK')
        print('\033[1;35mexcle 重复的包名数量为为： ' + str(excleRepeatPackage) + '\033[0m ')
        print('\033[1;35m已经配置过兼容性的数量为： ' + str(newPackage) + '\033[0m ')
        print('\033[1;33m新增包名重复数量为： ' + str(nrows - newPackage) + '\033[0m ')
except Exception as err:
    print('错误：{err}'.format(err=err))
