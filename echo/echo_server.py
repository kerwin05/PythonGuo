import socket
import threading
import time


def tcpLink(connection, address):
    print('Accept new connection from %s:%s...' % address)
    connection.send(b'Welcome!')
    while True:
        data = connection.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        connection.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    connection.close()
    print('Connection from %s:%s closed.' % address)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 9999))
    s.listen(5)
    print('Waiting for connection...')
    while True:
        # 接受一个新连接:
        client_socket, client_address = s.accept()
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=tcpLink, args=(client_socket, client_address))
        t.start()
