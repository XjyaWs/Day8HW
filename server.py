import socket
import os
import struct
import json
from conf import settings

server = socket.socket()
server.bind(('127.0.0.1', 8080))
server.listen(5)

# 列出文件夹下的所有文件名
files_list = []
for file in os.listdir(settings.VIDEO_PATH):
    files_list.append(file)

conn, addr = server.accept()

# 发送的提示信息
msg1 = "可选文件如下：\n"
for index, file in enumerate(files_list, 1):
    msg1 = msg1 + str(index) + '. ' + file + '\n'
msg1 = (msg1 + '请输入数字选择想要下载的文件:\n').encode('utf-8')

conn.send(str(len(msg1)).encode('utf-8'))    # send the size of msg1
conn.send(msg1)    # send msg1

# 接受选择信息
client_reply = int(conn.recv(1024).decode('utf-8'))
file_chosen = files_list[client_reply-1]

# -------------发送指定文件-------------
# 读取文件内容
with open(os.path.join(settings.VIDEO_PATH, file_chosen), 'rb') as f:
    file_data = f.read()
# 生成文件头字典
file_header = json.dumps({'file_name': file_chosen, 'file_size': len(file_data)})
# 发送字典大小
dict_header = struct.pack('i', len(file_header))
conn.send(dict_header)

# 发送字典
conn.send(file_header.encode('utf-8'))

# 发送文件
conn.send(file_data)

conn.close()
