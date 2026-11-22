import socket
import sys


def check_port(ip, port=22):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(2)
        return sock.connect_ex((ip, port)) == 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Usage: python socket-test.py <ip> [port]")

    ip = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 22

    if check_port(ip, port):
        print(f"Port {port} on {ip} is open")
    else:
        print(f"Port {port} on {ip} is closed or not responding")
