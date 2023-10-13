import socket
import threading


def handle_client(client_socket, address, clients):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"来自{address}的消息: {data}")

            # 解析数据格式
            if ',' in data:
                parts = data.split(',')
                if len(parts) == 2:
                    port = parts[0]
                    text = parts[1]
                    if port.isdigit():
                        # 转发消息给指定端口的客户端
                        for client in clients:
                            if client.getpeername()[1] == int(port):
                                message = f"来自{address}的消息: {text}"
                                client.sendall(message.encode())
                                break

        except socket.error as e:
            print(f"Socket error: {e}")
            break

    # 关闭客户端连接
    client_socket.close()
    clients.remove(client_socket)
    print(f"Connection closed with {address}，{address} 离线")
    send_all_ports(clients)


def start_server():
    host = "127.0.0.1"
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    clients = []

    print("Server started. Waiting for client connections...")

    def listen_input():
        # 监听输入并发送消息给所有客户端
        try:
            while True:
                message = input("")
                if message:
                    for client in clients:
                        send_message = f"来自服务端{address}的消息: {message}"
                        client.sendall(send_message.encode())
        except KeyboardInterrupt:
            # 如果接收到键盘中断信号，停止监听输入
            pass

    # 启动监听输入的线程
    input_thread = threading.Thread(target=listen_input)
    input_thread.start()

    while True:
        client_socket, address = server_socket.accept()
        clients.append(client_socket)
        print(f"Client connected: {address}")

        # 启动一个新线程处理客户端连接
        thread = threading.Thread(target=handle_client, args=(client_socket, address, clients))
        thread.start()


def send_all_ports(clients):
    # 组合所有客户端的端口号
    all_ports = ','.join(str(client.getpeername()[1]) for client in clients)

    # 发送所有端口号给每个客户端
    prefix_message = "当前在线用户: " + all_ports
    for client in clients:
        client.sendall(prefix_message.encode())


start_server()
