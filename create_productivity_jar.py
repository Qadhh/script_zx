#!/usr/bin/python
# -*- coding: UTF-8 -*-

import zipfile
import os, sys,time,os.path,shutil,argparse
NUM_COUNT = 0
NUM_COUNTA = 0
#GSI路径
gsiPath="/media/zhangxu/disk/aosp-11-GSI/"


#以日期为文件夹名称保存jar包
currentTimeStr=time.strftime('%m-%d')

#jar包存放位置
#获取桌面路径
JARpath=os.path.join(os.path.expanduser('~'), "Desktop")+"/JAR/"+currentTimeStr+"/"

#jar包名称
selectCreateJar=""

#二进制编码存放位置
classPath="out/target/common/obj/JAVA_LIBRARIES/"

#源码存放位置
javaPath="vendor/lenovo/productivity/"

#解压后文件夹名称
unzip_file =''

javaPath = ''
#sys_framework_path='/home/zhangxu/disk/aosp-11-GSI/vendor/lenovo/productivity/sys-framework/java'


javaDirPath = 'vendor/lenovo/productivity/'
classDirPath= 'out/target/common/obj/JAVA_LIBRARIES/'
lib = ''

#帮助信息
parser = argparse.ArgumentParser(description='create prebuild jar')
parser.add_argument('--select', help='1 for framework jar ,2 for services jar,default 1')
parser.add_argument('--path', help='gsi path')
args = parser.parse_args()





#解压文件
def un_zip(file_name):
#print"解压 classes.jar"
 """unzip zip file"""
 
 zip_file = zipfile.ZipFile(file_name)
 global unzip_file
 unzip_file=file_name + "_files"
 if os.path.isdir(file_name + "_files"):
  pass
 else:
  
  os.mkdir(unzip_file)
 for names in zip_file.namelist():
  zip_file.extract(names,unzip_file + "/")
 zip_file.close()
 
def listdir(path, list_name):  # 传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)
            
def getSimplePath(listpath,path,list_name_simple_java):
    for file in listpath:
            file=file.replace(path,"")
            file=file.replace(".java","")
            #print(file)
            list_name_simple_java.append(file)
            
def deleteFile(list_name_class,classPath,list_name_simple_java):
    for classFile in list_name_class:
    	tmpFile=classFile
        classFile=classFile.replace(classPath,"")
        if '$' in classFile:
            classFile=classFile.split('$')[0]
        if '.class' in classFile:
            classFile=classFile.replace(".class","")
        classFile="/"+classFile
        #print('lastFile:   '+classFile)
        if  classFile  in list_name_simple_java:
            #print('classFile not delete------------')
            print(classFile)
        else:
            #print('+++++++++++++++++need delete file+++++++++++')
           # print(tmpFile)
            os.remove(tmpFile)
    #print(list_name_simple_java)
    
#移出空目录
def delete_gap_dir(dir):
	if os.path.isdir(dir):
		for d in os.listdir(dir):
			delete_gap_dir(os.path.join(dir, d))
		if not os.listdir(dir):
			os.rmdir(dir)
			#global NUM_COUNT
			#NUM_COUNT = NUM_COUNT + 1
			#print('移除空目录: ' + dir)
		
#删除指定文件夹意外的文件夹
def DeleteFiles(path,remainDirsList,dirsList):
	dirsList = []
  	dirsList = os.listdir(path)
  	for f in dirsList:
		if f not in remainDirsList:
			filePath = os.path.join(path,f)
			if os.path.isdir(filePath):						
				shutil.rmtree(filePath, True)
				if f in filesList:
					filePath = os.path.join(path,f)
					os.remove(f)
 
#压缩指定文件			
def zip_dir(dirname,zipfilename):
  filelist = []
  if os.path.isfile(dirname):
    filelist.append(dirname)
  else :
    for root, dirs, files in os.walk(dirname):
      for name in files:
        filelist.append(os.path.join(root, name))
  zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
  for tar in filelist:
    arcname = tar[len(dirname):]
    #print arcname
    zf.write(tar,arcname)

  zf.close()

#选择器 
#if __name__ == '__main__': 
if args.select is "2":
    print("begin create services jar")
    selectCreateJar="productivity-services-prebuilt"
    lib =gsiPath+classDirPath+"services_intermediates/"
    javaPath = gsiPath+javaDirPath+"sys-services/src/main/java"
    classPath=gsiPath+classDirPath+"services_intermediates/classes.jar"
else:
    print("begin create framework jar")
    selectCreateJar="productivity-framework-prebuilt"
    lib =gsiPath+classDirPath+"framework-minus-apex_intermediates/"
    javaPath = gsiPath+javaDirPath+"sys-framework/src/main/java"
    classPath=gsiPath+classDirPath+"framework-minus-apex_intermediates/classes.jar"

print("当前时间为："+currentTimeStr)
time1 = time.time()

#创建目录 
if os.path.isdir(JARpath):
    print("JARpath:"+JARpath+"已经存在")
else:
    os.makedirs(JARpath)
    print("创建目录："+JARpath)
#解压
un_zip(classPath)

# 列出clas print("JARpath:"+JARpath+"已经存在")s文件夹 
list_name_class=[]
#unzip_file_path= lib+'classes.jar_files/'
#listdir(unzip_file+"/"+"com/",list_name_class)
print("unzip_file="+unzip_file)
listdir(unzip_file+"/",list_name_class)
#print("list_name_class="+list_name_class)


# 列出Java文件夹
list_name_java=[]
#listdir(javaPath+"/com",list_name_java)
print("javaPath="+javaPath)
listdir(javaPath+"/",list_name_java)

## 将java数组去除后缀名和父路径
list_name_simple_java=[]
getSimplePath(list_name_java,javaPath,list_name_simple_java)

## 循环class数组，去掉在java数组中没有对应的文件
deleteFile(list_name_class,unzip_file+"/",list_name_simple_java)

#移出空目录
delete_gap_dir(unzip_file+"/")

#删除指定文件夹以外的文件夹 unzip_file_path
filesList=['com',"android"]
#当前目录中需要保留的文件夹
dirsList=[]
DeleteFiles(unzip_file+"/",filesList,dirsList)

#压缩指定文件 unzip_file_path	
zip_dir(unzip_file+"/",JARpath+selectCreateJar+".jar")
print("\033[1;32m create jar successful:"+JARpath+selectCreateJar+".jar\033[0m")

time2 = time.time() - time1
print'\033[1;32m 用时:', time2,'s\033[0m '
#print'删除文件夹个数:',NUM_COUNT
#print('删除完毕')



