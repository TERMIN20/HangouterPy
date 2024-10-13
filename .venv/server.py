import sqlite3
import hashlib
import socket
import threading

HOST = "localhost"
PORT = 9999
#server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.bind(("localhost", 9999))

#server.listen()

sql = sqlite3.connect("users.db", check_same_thread=False)
cur = sql.cursor()

def handle_client(conn, addr):
    try:
        while True:
            conn.send("EventReq".encode())
            eventname = conn.recv(1024).decode()
            print(eventname)
            if (eventname != "/~n"):
                print("EventReq found")
                conn.send("DateReq".encode())
                date = conn.recv(1024).decode()
                print("Date " + date)
                conn.send("UserReq".encode())
                user = conn.recv(1024).decode()
                print("user " + user)
                params = [user, eventname, date]
                cur.execute("INSERT INTO eventdata (username, activityname, date) VALUES (?, ?, ?)",
                            (user, eventname, date))
                sql.commit()
                print("curexecuted")

            conn.send("UsernameReq".encode())
            username = conn.recv(1024).decode()
            print(username)
            if (username != "/~n"):
                conn.send("PasswordReq".encode())
                password = conn.recv(1024)
                password = hashlib.sha256(password).hexdigest()

                cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))
                if cur.fetchall():
                    print(cur.fetchall())
                    conn.send("successful".encode())

                else:
                    conn.send("failed".encode())
    except BrokenPipeError:
        print('[DEBUG] addr:', addr, 'Connection closed by client?')
    except Exception as ex:
        print('[DEBUG] addr:', addr, 'Exception:', ex, )
    finally:
        conn.close()

#while True:
#   client, addr = server.accept()
#    threading.Thread(target=handle_connection, args=(client,)).start()
#
try:
    # --- create socket ---

    print('[DEBUG] create socket')

    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = socket.socket() # default value is (socket.AF_INET, socket.SOCK_STREAM) so you don't have to use it

    # --- options ---

    # solution for "[Error 89] Address already in use". Use before bind()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # --- assign socket to local IP (local NIC) ---

    print('[DEBUG] bind:', (HOST, PORT))

    s.bind((HOST, PORT)) # one tuple (HOST, PORT), not two arguments

    # --- set size of queue ---

    print('[DEBUG] listen')

    s.listen(1) # number of clients waiting in queue for "accept".
                # If queue is full then client can't connect.

    while True:
        # --- accept client ---

        # accept client and create new socket `conn` (with different port) for this client only
        # and server will can use `s` to accept other clients (if you will use threading)

        print('[DEBUG] accept ... waiting')

        conn, addr = s.accept() # socket, address

        print('[DEBUG] addr:', addr)

        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()

        #all_threads.append(t)

except Exception as ex:
    print(ex)
except KeyboardInterrupt as ex:
    print(ex)
except:
    print(sys.exc_info())
finally:
    # --- close socket ---

    print('[DEBUG] close socket')

    s.close()
