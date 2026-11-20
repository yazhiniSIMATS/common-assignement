import socket
import time

client_id = input("Client ID           : ")
server_ip = input("Server IP Address   : ")
port      = int(input("Port Number         : "))
protocol  = input("Protocol (TCP/UDP)  : ").strip().upper()
message   = input("Message             : ")

text = f"[{client_id}] {message}"

if protocol == "TCP":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, port))
    print("Connection Status   : Connected (3-way handshake done)")
    start = time.time()
    s.sendall(text.encode())
    reply = s.recv(1024).decode()
    end = time.time()
    s.close()
    ack = "Acknowledgment received"

elif protocol == "UDP":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2)
    print("Connection Status   : Connectionless (no handshake)")
    start = time.time()
    s.sendto(text.encode(), (server_ip, port))
    try:
        reply = s.recvfrom(1024)[0].decode()
        ack = "Reply received"
    except socket.timeout:
        reply, ack = "-", "No reply (packet may be lost)"
    end = time.time()
    s.close()

else:
    raise SystemExit("Please choose TCP or UDP")

print("Message Received    :", reply)
print("Acknowledgment      :", ack)
print(f"Transmission Time   : {(end - start) * 1000:.3f} ms")
