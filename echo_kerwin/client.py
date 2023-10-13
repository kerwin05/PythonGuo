import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"{data}")
        except socket.error as e:
            print(f"Socket error: {e}")
            break

    client_socket.close()
    print("Disconnected from server.")


def start_client():
    host = "127.0.0.1"
    server_port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, server_port))

    client_address = client_socket.getsockname()
    print(f"Connected to server on {client_address[0]}:{client_address[1]}")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input("")
        client_socket.sendall(message.encode())

        if message.lower() == "quit":
            break

    receive_thread.join()
    client_socket.close()
    print("Disconnected from server.")


start_client()
