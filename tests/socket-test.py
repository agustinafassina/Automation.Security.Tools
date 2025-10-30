import socket

def check_port(ip, port=22):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((ip, port))
    return result == 0

ip = '52.53.161.211'
if check_port(ip):
    print(f"Port 22 en {ip} está abierto")
else:
    print(f"Port 22 en {ip} está cerrado o no responde")