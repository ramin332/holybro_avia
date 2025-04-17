# send_udp.py

import socket

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b'stop', ('127.0.0.1', 5010))

if __name__ == '__main__':
    main()
