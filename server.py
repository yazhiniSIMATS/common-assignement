import socket
import threading

HOST, PORT = "127.0.0.1", 5000


def handle_tcp_client(conn, addr):
    print(f"[TCP] Connection established with {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode()
            print(f"[TCP] Received from {addr}: {msg}")
            conn.sendall(f"ACK: {msg}".encode())
    print(f"[TCP] Connection closed with {addr}")


def tcp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"[TCP] Server listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_tcp_client,
                         args=(conn, addr), daemon=True).start()


def udp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    print(f"[UDP] Server listening on {HOST}:{PORT}")
    while True:
        data, addr = s.recvfrom(1024)
        msg = data.decode()
        print(f"[UDP] Received from {addr}: {msg}")
        s.sendto(f"ACK: {msg}".encode(), addr)


if __name__ == "__main__":
    threading.Thread(target=udp_server, daemon=True).start()
    tcp_server()
