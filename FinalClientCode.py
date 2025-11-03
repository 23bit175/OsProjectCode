import socket
import struct
import sys

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7632
PASSWORD = "letmein"

def send_with_length(sock, data: bytes):
    sock.sendall(struct.pack("!Q", len(data)))
    if data:
        sock.sendall(data)

def recv_all(sock, n):
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("connection closed")
        buf += chunk
    return buf

def recv_message(sock):
    raw = sock.recv(8)
    if not raw:
        return None
    length = struct.unpack("!Q", raw)[0]
    if length == 0:
        return ""
    return recv_all(sock, length).decode(errors="ignore")


s = socket.socket()

try:
    s.connect((SERVER_HOST, SERVER_PORT))
except Exception as e:
    print(f"Could not connect: {e}")
    sys.exit(1)

    
prompt = recv_message(s)
if prompt and prompt.startswith("PASSWORD"):
    send_with_length(s, PASSWORD.encode())
    auth = recv_message(s)
    if not auth or not auth.startswith("AUTH_OK"):
        print("Authentication failed.")
        s.close()
        
    print("Connected to remote shell.\n")
else:
    print("Unexpected server response.")
    s.close()
    

    
while True:
    cmd = input("cmd> ").strip()
    if not cmd:
        continue
    send_with_length(s, cmd.encode())
    if cmd.lower() in ("exit", "quit", "bye"):
        print("Closing connection.")
        break

    try:
        out = recv_message(s)
    except ConnectionError:
        print("Server disconnected.")
        break
    if out is None:
        print("Server closed connection.")
        break

    print(out, end="")
s.close()
