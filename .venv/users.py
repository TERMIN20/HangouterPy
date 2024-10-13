import socket

users = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
users.connect(("localhost", 5000))


message = users.recv(1024).decode()
users.send(input(message).encode())
message = users.recv(1024).decode()
users.send(input(message).encode())
print(users.recv(1024).decode())


