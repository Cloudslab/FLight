"""
All required Ip Configuration helpers
"""

###
# Get the ipv4 address of this machine, needs connection to Google
import sys
def get_ipv4_address():
    if not hasattr(sys.modules, "ipv4"):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))
        sys.modules["ipv4"] = s.getsockname()[0]
        s.close()
    return sys.modules["ipv4"]