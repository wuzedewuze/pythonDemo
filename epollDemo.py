#!/usr/bin/env python
# coding=utf-8

import select
import socket

listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)    # 创建套接字、ipv4，流模式tcp，默认0协议编号
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # 设置给定套接字选项的值，防止端口不释放的情况
listen_sock.bind(("0.0.0.0", 8888))                                 # 绑定ip地址和端口，以元组的形式
listen_sock.listen(10)                                               # 开始监听，设置操作系统最大挂起值，正常设置为5即可
listen_sock.setblocking(0)                                           # 设置为非阻塞模式，默认为阻塞模式

epoll_sock = select.epoll()                                        # 创建epoll对象,只支持unix类系统
epoll_sock.register(listen_sock.fileno(), select.EPOLLIN )         # 注册epoll，设置socke的filedescription，和lin模式

fdsock = {
    listen_sock.fileno(): listen_sock,                             # 设置一个字典，文件fd和socke对象
}

# read 12345\r\n
# write 54321\r\n
sent = 0
buf = ""

while True:
    epoll_list = epoll_sock.poll() # 返回poll对象：元组list[(fid,eventid),(fid2,eventid2)]，此处是阻塞的，在没有时间的时候停止运行。
    for fd, events in epoll_list:   
        if select.EPOLLIN & events:                             # 如果有输入事件
            if fd == listen_sock.fileno():                   # 如果fd和初始值相同，说明监听到有第一次连接进来，而不是后面输入的数据
                conn,addr = listen_sock.accept()                # 获取conn对象和连接地址
                conn.setblocking(0)                             # 设置非阻塞
                print conn, addr, conn.fileno()
                epoll_sock.register(conn.fileno(), select.EPOLLIN) # 注册epoll，此时epoll_list就会有两组数据了
                fdsock[conn.fileno()] = conn                     # 存储conn的fd值，方便后面调用conn对象
            else:                                  # 如果文件描述id的值不是初始值，说明是连接conn的fd，开始接受用户输入数据
                buf += fdsock[fd].recv(100)                      # 获取100个字符
                if len(buf) > 2 and buf[-2] == '\r' and buf[-1] == '\n': # 如果获取到的buf长度大于2，并且最后两位是\r\n换行就翻转
                    buf = buf[:-2][::-1]+ "\r\n"       # 翻转输入的字符，从倒数第二个字符开始，反向每隔一个去一个字符放入到buf中
                    epoll_sock.unregister(conn)# 取消注册，此时epoll_sock对象里只剩一个注册事件了，epoll_list就又回到到等待上去
                    epoll_sock.register(conn.fileno(), select.EPOLLOUT)   # 注册输出，将翻转后的conn对象注册为IPOLLOUT

        elif select.EPOLLOUT & events:                             # 发现输出事件
            print sent, buf                                        # 打印输出的字符
            s = fdsock[fd].send(buf[sent:])                        # conn.send发送返回数据，返回发送的字节数量
            print 's', s                                         # 打印出长度
            if s > 0:                                             # 如果有发送数据
                sent += s                                         # send设置成已发送送的字节数
            if sent == len(buf):                              # 获取到buf长度，如果缓冲区长度和发送长度相等，取消注册，重新等待输入
                epoll_sock.unregister(conn)                       # 获取完以后取消conn注册事件
                epoll_sock.register(conn.fileno(), select.EPOLLIN)# 再返回注册成conn的epollin事件
                buf = ""                                          # buf缓冲区再设置成空
                sent = 0                                          # 发送的send设置为0
