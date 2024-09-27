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


# def send(client, msg):
#     message = msg.encode(FORMAT)
#     client.send(message)


# def start():
#     answer = input('Would you like to connect (yes/no)? ')
#     if answer.lower() != 'yes':
#         return

#     connection = connect()
#     while True:
#         msg = input("Message (q for quit): ")

#         if msg == 'q':
#             break

#         send(connection, msg)

#     send(connection, DISCONNECT_MESSAGE)
#     time.sleep(1)
#     print('Disconnected')


# start()


# import socket
# import threading
# import time

# PORT = 5050
# SERVER = "localhost"
# ADDR = (SERVER, PORT)
# FORMAT = "utf-8"
# DISCONNECT_MESSAGE = "!DISCONNECT"

# def connect():
#     """ Establish a connection to the server """
#     try:
#         client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         client.connect(ADDR)
#         return client
#     except ConnectionRefusedError:
#         print("Connection failed. Is the server running?")
#         return None

# def send(client, msg):
#     """ Send a message to the server """
#     try:
#         message = msg.encode(FORMAT)
#         client.send(message)
#     except:
#         print("Failed to send message.")

# def start():
#     """ Start the client and interact with the user """
#     connection = connect()
#     if not connection:
#         return
#     answer = input('Would you like to connect (yes/no)? ')
#     if answer.lower() != 'yes':
#         return

#     def receive_messages():
#         """ Receive messages from the server """
#         while True:
#             try:
#                 msg = connection.recv(1024).decode(FORMAT)
#                 if msg:
#                     print(msg)
#             except:
#                 print("Connection closed.")
#                 break

#     # Start receiving messages in a background thread
#     receive_thread = threading.Thread(target=receive_messages)
#     receive_thread.start()

#     # Send messages to the server
#     while True:
#         msg = input("Message (press q for quit): ")
#         if msg == 'q':
#             break
#         send(connection, msg)

#     send(connection, DISCONNECT_MESSAGE)
#     time.sleep(1)
#     print('Disconnected')

# start()

import socket
import threading

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('localhost', 12345))
        print("Connected to the server.")
    except ConnectionRefusedError:
        print("Failed to connect to the server. Is the server running?")
        exit()
    return client

def send(client):
    while True:
        msg = input("Client:")  # Get user input
        if msg.lower() == "exit":  # Allow graceful exit
            print("Disconnecting from the server...")
            client.close()
            break
        client.send(msg.encode('utf-8'))  # Send message to server

def receive(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')  # Receive message from server
            if message:
                print(f"\n{message}")  # Print received message
            else:
                print("Connection closed by the server.")
                client.close()
                break
        except:
            print("An error occurred! Closing connection.")
            client.close()
            break

def start():
    client = connect()  # Establish connection to the server
    threading.Thread(target=receive, args=(client,), daemon=True).start()
    send(client)  # Start sending messages

if __name__ == "__main__":
    start()  # Run the client
