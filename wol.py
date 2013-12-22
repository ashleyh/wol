import socket
import argparse
import sys


_py_ver = sys.version_info[0]


if _py_ver == 2:
    def ints_to_bytes(ints):
        return ''.join(chr(x) for x in ints)
elif _py_ver == 3:
    ints_to_bytes = bytes


def mac_addr(s):
    if len(s) == 17:
        step = 3
    elif len(s) == 12:
        step = 2
    else:
        raise ValueError("Couldn't parse " + s)

    ints = [int(s[i:i + 2], base=16) for i in range(0, len(s), step)]

    return ints_to_bytes(ints)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mac_addr', type=mac_addr)
    parser.add_argument('--broadcast-address', default='255.255.255.255')
    parser.add_argument('--port', default=1234, type=int)
    args = parser.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    packet = b'\xff' * 6 + args.mac_addr * 16
    s.sendto(packet, (args.broadcast_address, args.port))


if __name__ == '__main__':
    main()
