# import threading
# import socket
# import time

# # Server setup
# PORT = 5050
# SERVER = "localhost"  # Localhost for simplicity
# ADDR = (SERVER, PORT)
# FORMAT = "utf-8"
# DISCONNECT_MESSAGE = "!DISCONNECT"

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(ADDR)

# clients = set()
# clients_lock = threading.Lock()

# def broadcast(message, _client):
#     """ Send a message to all connected clients except the sender """
#     with clients_lock:
#         for client in clients:
#             if client != _client:
#                 try:
#                     client.sendall(message)
#                 except:
#                     client.close()
#                     clients.remove(client)

# def handle_client(conn, addr):
#     """ Handle messages from a single client """
#     print(f"[NEW CONNECTION] {addr} connected.")
#     try:
#         connected = True
#         while connected:
#             msg = conn.recv(1024).decode(FORMAT)
#             if not msg:
#                 break
#             if msg == DISCONNECT_MESSAGE:
#                 connected = False
#             else:
#                 timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
#                 full_message = f"[{timestamp}] {addr}: {msg}"
#                 print(full_message)
#                 broadcast(full_message.encode(FORMAT), conn)
#     except ConnectionResetError:
#         print(f"[ERROR] Connection lost with {addr}")
#     finally:
#         with clients_lock:
#             clients.remove(conn)
#         conn.close()

# def start():
#     """ Start the server to listen for clients """
#     print("[SERVER STARTED] Waiting for connections...")
#     server.listen()
#     while True:
#         conn, addr = server.accept()
#         with clients_lock:
#             clients.add(conn)
#         thread = threading.Thread(target=handle_client, args=(conn, addr))
#         thread.start()

# start()


import socket
import threading

# List to keep track of connected clients
clients = []

def handle_client(conn, addr):
    print(f"{addr} connected.")
    clients.append(conn)
    try:
        while True:
            msg = conn.recv(1024).decode('utf-8')
            if msg:
                print(f"Received from {addr}: {msg}")
                broadcast(msg, conn)  # Broadcast received message to all clients
            else:
                break
    finally:
        print(f"{addr} disconnected.")
        clients.remove(conn)
        conn.close()

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:  # Don't send the message back to the sender
            client.send(message.encode('utf-8'))

def send_message_to_all(message):
    for client in clients:
        client.send(f"Server: {message}".encode('utf-8'))

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen()
    # print("Server started and waiting for connections...")
    
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    threading.Thread(target=start, daemon=True).start()
    
    while True:
        print("Server started and waiting for connections...")
        server_msg = input("Enter a message to send to all clients (type 'exit' to quit): ")
        if server_msg.lower() == 'exit':
            break
        send_message_to_all(server_msg)
