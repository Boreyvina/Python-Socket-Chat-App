# import socket
# import time

# PORT = 5050
# SERVER = "localhost"
# ADDR = (SERVER, PORT)
# FORMAT = "utf-8"
# DISCONNECT_MESSAGE = "!DISCONNECT"


# def connect():
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect(ADDR)
#     return client


# def start():
#     connection = connect()
#     while True:
#         msg = connection.recv(1024).decode(FORMAT)
#         print(msg)


# start()

# import socket

# PORT = 5050
# SERVER = "localhost"
# ADDR = (SERVER, PORT)
# FORMAT = "utf-8"

# def connect():
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect(ADDR)
#     return client

# def start():
#     connection = connect()
#     while True:
#         try:
#             msg = connection.recv(1024).decode(FORMAT)
#             if msg:
#                 print(msg)
#         except:
#             print("Connection closed.")
#             break

# start()

import socket

def connect():
    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the server at localhost on port 12345
        client.connect(('localhost', 12345))
        print("Connected to the server.")
    except ConnectionRefusedError:
        print("Failed to connect to the server. Is the server running?")
        exit()
    return client

def start():
    client = connect()  # Establish connection to the server
    try:
        while True:
            message = client.recv(1024).decode('utf-8')  # Receive message from server
            if message:
                print(f"New message: {message}")  # Print received message
            else:
                print("Connection closed by the server.")
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()  # Ensure the socket is closed

if __name__ == "__main__":
    start()  # Run the message listener
