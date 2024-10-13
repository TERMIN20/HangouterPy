import sqlite3
import hashlib
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))

server.listen()

conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

def handle_connection(c):
    c.send("EventReq".encode())
    eventname = c.recv(1024).decode()
    print(eventname)
    if (eventname!="/~n"):
        print("EventReq found")
        c.send("DateReq".encode())
        date = c.recv(1024).decode()
        print("Date " + date)
        c.send("UserReq".encode())
        user = c.recv(1024).decode()
        print("user " + user)
        params = [user, eventname, date]
        cur.execute("INSERT INTO eventdata (username, activityname, date) VALUES (?, ?, ?)", (user, eventname, date))
        conn.commit()
        print("curexecuted")

    c.send("UsernameReq".encode())
    username = c.recv(1024).decode()
    print(username)
    if (username != "/~n"):
        c.send("PasswordReq".encode())
        password = c.recv(1024)
        password = hashlib.sha256(password).hexdigest()


        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))
        if cur.fetchall():
            print(cur.fetchall())
            c.send("successful".encode())

        else:
            c.send("failed".encode())


while True:
    client, addr = server.accept()
    threading.Thread(target=handle_connection, args=(client,)).start()
