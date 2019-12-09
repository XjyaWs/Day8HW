import socket
import os
import struct
import json
from conf import settings
import hashlib

client = socket.socket()

# 列出文件夹下的所有文件名
files_list = []
for file in os.listdir(settings.VIDEO_PATH):
    files_list.append(file)

# 提示信息
msg1 = "可选文件如下：\n"
for index, file in enumerate(files_list, 1):
    msg1 = msg1 + str(index) + '. ' + file + '\n'
msg1 = (msg1 + '请输入数字选择想要下载的文件:\n')

# 选择信息
reply = ''
while len(reply) ==0:
    reply = input(msg1).strip()
reply = int(reply)
file_chosen = files_list[reply-1]

# 读取文件内容、 生成大文件md5
m = hashlib.md5()
with open(os.path.join(settings.VIDEO_PATH, file_chosen), 'rb') as f:
    while True:
        data = f.read(4096)
        if not data:
            break
        m.update(data)
    file_data = f.read()
file_md5 = m.hexdigest()


# 生成文件头字典
file_header = json.dumps({'file_name': file_chosen, 'file_size': len(file_data), 'md5': file_md5})
print(file_header)

# 链接服务器
client.connect(('127.0.0.1', 8080))

# -------------发送指定文件-------------
# 发送字典大小
dict_header = struct.pack('i', len(file_header))
client.send(dict_header)

# 发送字典
client.send(file_header.encode('utf-8'))

# 发送文件
client.send(file_data)
