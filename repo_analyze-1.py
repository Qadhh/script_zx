import argparse
import math
import subprocess
import pandas as pd
import os, sys,time,os.path,shutil,argparse

#以日期为文件夹名称保存jar包
currentTimeStr=time.strftime('%m-%d')
#获取桌面路径
ReviewPath=os.path.join(os.path.expanduser('~'), "Desktop")+"/review_aosp_wm/"+currentTimeStr+"/"

# authors = dict()
# commits = dict()

name_mapping = {
    "zhangzy95": "Zhang Zhaoyue",
    "shixf7": "Shi Xufeng",
    "zhoubinbin": "Zhou Binbin",
    "zhangrunqiu": "Zhang Runqiu",
    "Shi xu feng": "Shi Xufeng",
    "zengshuyu": "Zeng Shuyu",
    "zhoubb5": "Zhou Binbin",
}

data = []


def read_stdout(command):
    stdout = subprocess.PIPE
    stderr = subprocess.STDOUT
    process = subprocess.Popen(command, stdout=stdout, stderr=stderr, shell=True)
    lines = []
    while True:
        line = process.stdout.readline().decode()  # 将字节转换为字符串
        if line == "" and process.poll() is not None:
            break
        line = line.strip()
        if line != "":
            lines.append(line)  # 输出每一行的结果
    return lines


# def lok(path):
#     print(path)
#     lines = read_stdout("lok -o=json " + path + ' | jq ".items[0].code"')
#     return int(lines[0])
def count_loc(file_path):
    # """
    # 计算给定文件的代码行数。

    # 参数:
    # file_path (str): 文件路径。

    # 返回:
    # int: 文件的代码行数。
    # """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return len(lines)


def analyze_file(hash, name):
    """
    分析单个git提交，计算每个文件的添加和删除行数，并根据映射关系转换作者名称。

    参数:
    hash (str): 提交的哈希值。
    name (str): 提交者的名称。
    """
    # lines2 = read_stdout("git diff " + hash + "^.." + hash + " --numstat")
    lines2 = read_stdout("git show " + hash + ' --pretty="format:" --numstat')
    for line2 in lines2:
        print(line2)
        elems2 = line2.split("\t")
        added = 0
        removed = 0
        if elems2[0] != "-":
            added = int(elems2[0])
        if elems2[1] != "-":
            removed = int(elems2[1])
        path = elems2[2]
        if path.endswith("java"):
            loc = count_loc(path)
            percent = min(math.ceil(added / loc * 100), 100)
            readed = math.ceil(loc * (added / loc))
            if name in name_mapping:
                name = name_mapping[name]
            print(name, path, added, removed, loc, readed, str(percent) + "%")
            data.append(
                {
                    "Name": name,
                    "Path": path,
                    "Added": added,
                    "Removed": removed,
                    "LoC": loc,
                    "Readed": readed,
                    "Percent": str(percent) + "%",
                }
            )
        else:
            if name in name_mapping:
                name = name_mapping[name]
            data.append(
                {
                    "Name": name,
                    "Path": path,
                    "Added": added,
                    "Removed": removed,
                    "LoC": 0,
                    "Readed": 0,
                    "Percent": "100%",
                }
            )


# 65fca3889d0864afa2cb1d6d5e18f431797aa780 | Shi Xufeng | shixufeng@jianguodata.com | 1713521305
# 31ae4507a79d9f130c0c8e34dfbf1c61d3f20973 | Zhang Xu | zhangxu@jianguodata.com | 1713442809
# 2c4b107b03124f6ce2ae02f8b7c63aade0d8a0ba | Liu Bingzhao | liubingzhao@jianguodata.com | 1713442294
# be4e8036730b76295f6d5e46718bc762dd1b2dae | Liu Bingzhao | liubingzhao@jianguodata.com | 1713441128
def get_all_commits(since: str, until: str):
    lines = read_stdout(
        f'git log --since="{since}" --until="{until}" --no-merges --pretty="format:%H|%aN|%aE"'
    )
    for line in lines:
        elems = line.split("|")

        hash = elems[0]
        name = elems[1]

        # authors.setdefault(name, list())
        # di = authors[name]
        # di.append(elems[0])

        print(name, hash)
        analyze_file(hash, name)

    # print(authors)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="Repo Analyze",
        description="Analyze the commiter and code lines",
        epilog="Licensed by EnsureBit, Inc.",
    )
    parser.add_argument("filename")
    parser.add_argument("-s", "--since")
    parser.add_argument("-u", "--until")
    parser.add_argument("-v", "--verbose", action="store_true")

    return parser.parse_args()


def main():
    
    args = parse_args()

    print(args.filename, args.since, args.until, args.verbose)

    # 2024-04-29
    get_all_commits(args.since, args.until)

    df = pd.DataFrame(
        data, columns=["Name", "Path", "Added", "Readed", "LoC", "Percent"]
    )
    print(df)

    print(ReviewPath)
    df.to_csv(ReviewPath+args.filename)


# 0       0       "module/warnings_dialog/\350\255\246\345\221\212\345\257\271\350\257\235\346\241\206.adoc" => module/warnings_dialog/dialog.adoc
# 1       1       module/warnings_dialog/index.adoc
# log = subprocess.getoutput("git diff b3667edf0d9f9a30aa2e955979b18c440da317f8^..b3667edf0d9f9a30aa2e955979b18c440da317f8 --numstat")
if __name__ == "__main__":
    #创建目录 
    if os.path.isdir(ReviewPath):
        print("ReviewPath:"+ReviewPath+"已经存在")
    else:
        os.makedirs(ReviewPath)
        print("创建目录："+ReviewPath)
    main()
