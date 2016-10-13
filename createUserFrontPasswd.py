#!_*_encoding:utf-8_*_

import  re

# 该脚本从/etc/passwd 文件中读取匹配的用户名，用户id和组id
# 生成对应的shell语句


# 读取/etc/passwd,返回用户名，用户id，组id值

#从/etc/passwd 文件中读取匹配的用户名，用户id和组id
def get_username_gid_uid():
    with open('./passwd', 'r') as f:
        for line in f.readlines():
            strLine = line.strip()
            #print strLine
            m = re.search(r'^nice',strLine)
            if m:
                tempStrin = m.string
                username = tempStrin.split(':')[0]
                uid = tempStrin.split(':')[2]
                gid = tempStrin.split(':')[3]
                print 'groupadd -g '+gid+' '+username
                print 'useradd -r -g '+gid+' -u '+uid+username


get_username_gid_uid()
