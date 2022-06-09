from ipAddressHelper import get_ipv4_address


def test_get_ipv4_address():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))
    ipv4_address = s.getsockname()[0]
    s.close()

    assert get_ipv4_address() == ipv4_address

if __name__ == "__main__":
    print("HWW")