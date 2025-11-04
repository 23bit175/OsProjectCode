import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7632

s = socket.socket()
s.connect((SERVER_HOST, SERVER_PORT))

welcome = s.recv(1024).decode()
print(welcome)

while True:
    cmd = input("cmd> ").strip()
    if not cmd:
        continue

    s.send(cmd.encode())

    if cmd.lower() in ["exit", "quit", "bye"]:
        print("Closing connection...")
        break

    output = s.recv(4096).decode()
    print(output)

s.close()