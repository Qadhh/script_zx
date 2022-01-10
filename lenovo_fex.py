#!/usr/bin/env python3
# coding=utf-8
# Lenovo FEX 工具 (Python3版本)
# 修改者：  iRayle
# 版  本： 20201111

import os
import sys
import json
import getpass
import requests
from lxml import etree
from optparse import OptionParser
from requests_toolbelt import MultipartEncoderMonitor


def progress(size, progress):
    done = int(100 * progress / size)
    if done > 100:
        done = 100
    sys.stdout.write("\r[%s%s] %d%%, %sM / %sM\r" % ('=' * int((done / 2)), ' '*(50 - int((done / 2))), done, '%.2f' % (progress / 1024.0 / 1024.0), '%.2f' % (size / 1024.0 / 1024.0)))
    sys.stdout.flush()


class Fex():
    def __init__(self):
        self.url = 'http://tbbjfex.lenovo.com'
        self.url_login = self.url + '/login'
        self.url_islogin = self.url + '/islogin'
        self.url_down_file = self.url + '/downfile'
        self.url_file_list = self.url + '/filelist'
        self.path = os.path.join(os.path.expanduser('~'), '.fexconf')
        self.configs = {}
        self.cookies = {}
        try:
            with open(self.path, 'r') as f:
                self.configs = json.load(f)
                self.cookies = self.configs['cookies']
        except:
            print('请登录后使用！')
            return

    def login(self):
        cookie_count = 0
        while cookie_count == 0:
            username = input('用户名:')
            password = getpass.getpass('密码:')
            data = {'username': username,
                    'password': password, 'rememberme': 'on'}
            requests_session = requests.Session()
            requests_session.post(self.url_login, data)
            for k, v in requests_session.cookies.items():
                self.cookies[k] = v
            cookie_count = len(self.cookies)
            if 0 == cookie_count:
                print('登录出错，请重新尝试!')
            self.configs['cookies'] = self.cookies
        print(username, '登录成功！')
        try:
            with open(self.path, 'w') as f:
                import json
                json.dump(self.configs, f)
        except:
            print('登录系统出错！')
            return

    def checklogin(self):
        if len(self.cookies) == 0:
            self.login()
        r = requests.get(self.url_islogin, cookies=self.cookies,
                         allow_redirects=False)
        if isinstance(r.json, dict):
            login_msg = r.json['result']
        else:
            login_msg = r.json()['result']
        if 'true' != login_msg:
            print('login', self.url_login, 'time out')
            self.login()

    def filelist(self):

        res = requests.get(self.url, cookies=self.cookies).content
        html = etree.HTML(res)
        user = html.xpath(
            '//table[@class="table table-striped"]/tbody/tr/td[2]/text()')[0]
        times = html.xpath(
            '//table[@class="table table-striped"]/tbody/tr/td[3]/text()')
        ips = html.xpath(
            '//table[@class="table table-striped"]/tbody/tr/td[4]//text()')
        files = html.xpath(
            '//table[@class="table table-striped"]/tbody/tr/td[5]')
        print('当前用户为', user)
        index = 0
        for index in range(len(ips)):
            fileStatus = files[index].xpath('string(.)').split(':')[1]
            if files[index].text.split(':')[1] != '':
                fileStatus += " (已失效)"
            print('{:>2}'.format(index), '|',
                  times[index], '|', ips[index], '|', fileStatus)
            index += 1

    def download_file(self, save_path='.', index='0'):
        url_file_index = self.url_down_file + '/' + index
        r = requests.get(url_file_index, cookies=self.cookies, stream=True)
        file_name = r.headers.get('Content-Disposition')
        if None == file_name:
            print(
                "Get download filename failed. May be a source file or you didn't upload file")
            return
        file_name = file_name[file_name.find('UTF-8') + 7:]
        from urllib.request import unquote
        file_name = unquote(file_name)
        file_name = os.path.join(save_path, file_name)
        file_length = int(r.headers.get('Content-Length'))
        print("Downloading %s(%sM)" %
              (file_name, '%.2f' % (file_length / 1024.0 / 1024.0)))
        download = 0
        try:
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(1024*1024):
                    download += len(chunk)
                    f.write(chunk)
                    progress(file_length, download)
        except Exception as e:
            print('\rDownload file exception:', e)
            return
        print('\nDownload success:', file_name)
        return file_name

    def upload_file(self, uploadfile):
        data = {}
        if not os.path.exists(uploadfile):
            print('uploadfile not exist')
            return
        filename = uploadfile.split("/")[-1]

        size = os.path.getsize(uploadfile)

        def my_callback(monitor):
            progress(size, monitor.bytes_read)
        print("Uploading %s (%sM)" %
              (filename, '%.2f' % (size / 1024.0 / 1024.0)))
        data['uploadfile'] = (filename, open(uploadfile, 'rb'))
        monitor = MultipartEncoderMonitor.from_fields(
            fields=data, callback=my_callback)
        req_headers = {'Content-Type': monitor.content_type}
        requests.post(self.url, data=monitor,
                      cookies=self.cookies, headers=req_headers)
        print('\nupload success')


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-r', action="store_true",
                      dest='relogin', help='重新登录')
    parser.add_option('-l', action="store_true",
                      dest='list_file', help='显示文件列表')
    parser.add_option('-u', action="store",
                      dest='upload_file', help='上传文件')
    parser.add_option('-d', action="store_true",
                      dest='download', help='下载文件，默认当前目录')
    parser.add_option('-i', action="store", type="int",
                      default=0, dest='index', help='下载文件序号，默认第1个')
    options, args = parser.parse_args()
    fex = Fex()
    fex.checklogin()
    if options.relogin:
        os.remove(os.path.join(os.path.expanduser('~'), '.fexconf'))
        print('已退出登录，如需登录请重新运行！')
    if options.upload_file != None:
        fex.upload_file(options.upload_file)
    elif options.download == True:
        if len(args) == 1:
            file_path = fex.download_file(args[0], str(options.index))
        else:
            file_path = fex.download_file(".", str(options.index))
    elif options.list_file == True:
        fex.filelist()
    else:
        print('使用帮助请输入： fex -h')
