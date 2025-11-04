import socket
import subprocess
import os
import threading

HOST = "127.0.0.1"
PORT = 7632

def handle_client(conn, addr):
    print(f"[+] Connected to {addr}")
    conn.send(b"Connected to the server. You can now run commands.\n")

    while True:
        cmd = conn.recv(1024).decode().strip()
        if not cmd:
            break

        if cmd.lower() in ["exit", "quit", "bye"]:
            conn.send(b"Goodbye!\n")
            break

        if cmd.startswith("cd "):
            path = cmd[3:].strip()
            try:
                os.chdir(os.path.expanduser(path))
                conn.send(f"Changed directory to {os.getcwd()}\n".encode())
            except:
                conn.send(b"cd error\n")
            continue

        result = subprocess.getoutput(cmd)
        if result.strip() == "":
            result = "(No output)"
        conn.send((result + "\n").encode())

    conn.close()
    print(f"[-] Disconnected {addr}")

s = socket.socket()
s.bind((HOST, PORT))
s.listen(5)
print(f"Server started on {HOST}:{PORT}")
print("Waiting for clients...\n")

while True:
    conn, addr = s.accept()
    threading.Thread(target=handle_client, args=(conn, addr)).start()