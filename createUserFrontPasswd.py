#!_*_encoding:utf-8_*_

import  re

# �ýű���/etc/passwd �ļ��ж�ȡƥ����û������û�id����id
# ���ɶ�Ӧ��shell���


# ��ȡ/etc/passwd,�����û������û�id����idֵ

#��/etc/passwd �ļ��ж�ȡƥ����û������û�id����id
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
