import socket
import os
import struct
import json
from conf import settings

server = socket.socket()
server.bind(('127.0.0.1', 8080))
server.listen(5)

while True:
    try:
        conn, addr = server.accept()

        # 接受字典头
        file_header_size = struct.unpack('i', conn.recv(4))[0]

        # 接受字典
        file_header = json.loads(conn.recv(file_header_size))
        print(file_header)

        # 接受文件
        file_size = int(file_header.get('file_size'))
        file_name = file_header.get('file_name')

        with open(os.path.join(settings.SAVED_PATH, file_name), 'wb') as f:
            data = b''
            res_size = 0
            while res_size < file_size:
                data = data + conn.recv(1024)
                f.write(data)
                res_size = res_size + len(data)
                data = b''

        conn.close()
    except Exception as e:
        print(e)
        conn.close()
