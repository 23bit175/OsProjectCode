import socket
import struct
import subprocess
import os
import threading  

HOST = "127.0.0.1"
PORT = 7632
PASSWORD = "letmein"

def send_with_length(conn, data: bytes):
    conn.sendall(struct.pack("!Q", len(data)))
    if data:
        conn.sendall(data)

def recv_all(conn, n):
    buf = b""
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("connection closed")
        buf += chunk
    return buf

def recv_message(conn):
    raw = conn.recv(8)
    if not raw:
        return None
    length = struct.unpack("!Q", raw)[0]
    if length == 0:
        return ""
    return recv_all(conn, length).decode(errors="ignore")

def handle_client(conn, addr):
    print(f" Connected: {addr}")

    send_with_length(conn, b"PASSWORD:")
    pw = recv_message(conn)
    if pw != PASSWORD:
        send_with_length(conn, b"AUTH_FAILED\n")
        conn.close()
        print(f" Wrong password from {addr}, closed connection.")
        return
    send_with_length(conn, b"AUTH_OK\n")

    while True:
        cmd = recv_message(conn)
        if cmd is None:
            break
        cmd = cmd.strip()
        if cmd.lower() in ("exit", "quit", "bye"):
            send_with_length(conn, b"Goodbye.\n")
            break


        if cmd.startswith("cd "):
            path = cmd[3:].strip()
            try:
                os.chdir(os.path.expanduser(path))
                out = f"Changed directory to {os.getcwd()}\n"
            except Exception as e:
                out = f"cd error: {e}\n"
            send_with_length(conn, out.encode())
            continue


        try:
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            out = (proc.stdout or "") + (proc.stderr or "")
        except Exception as e:
            out = f"Error: {e}\n"

        if not out.strip():
            out = "(No output)\n"
        send_with_length(conn, out.encode())

    conn.close()
    print(f" Connection closed: {addr}")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
    
s.listen(5) 
print(f" Server listening on {HOST}:{PORT}")


while True:
    conn, addr = s.accept()
    print(f" Accepted connection from {addr}")

    client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
    client_thread.start()
    print(f"Started thread for {addr}")
