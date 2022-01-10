#!/usr/bin/env python
# encoding:utf-8

import argparse
import os

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Pack changed files to zip')
    parser.add_argument('--commit', help='git commit id')
    parser.add_argument('--zip', help='output zip file')
    args = parser.parse_args()

    # 删除旧文件
    os.system("rm -f '" + args.zip + "'")

    git_cmd = "git log --oneline --name-status " + args.commit + "..HEAD"
    git_pipe = os.popen(git_cmd)
    for (i, line) in enumerate(git_pipe.readlines()):
        # D 怎么处理 ？
        if line.startswith(('A', 'M')):
            file = line.rstrip().split('\t')[1]
            if os.path.exists(file):
                flag = '' if i == 0 else 'g'
                zip_cmd = "zip -q{} {} {}".format(flag, args.zip, file)
                os.system(zip_cmd)

        if line.startswith(('D')):
            pass
