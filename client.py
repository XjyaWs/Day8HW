import socket
import os
import struct
import json
from conf import settings

client = socket.socket()
client.connect(('127.0.0.1', 8080))

# 接受提示信息
data1_size = int(client.recv(1024).decode('utf-8'))
data1 = client.recv(data1_size)

# 发送选择信息
reply = input(data1.decode('utf-8')).strip()
client.send(reply.encode('utf-8'))

# 接受字典头
file_header_size = struct.unpack('i', client.recv(4))[0]

# 接受字典
file_header = json.loads(client.recv(file_header_size))

# 接受文件
file_size = int(file_header.get('file_size'))

with open(os.path.join(settings.SAVED_PATH, 'video.mp4'), 'wb') as f:
    data = b''
    res_size = 0
    while res_size < file_size:
        data = data + client.recv(1024)
        f.write(data)
        res_size = res_size + len(data)
        data = b''
