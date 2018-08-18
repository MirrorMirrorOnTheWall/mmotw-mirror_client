from socketIO_client_nexus import SocketIO
from .SocketNameSpaces import ProvisionDeviceNamespace

class SocketConnection:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = SocketIO(self.ip, self.port, ProvisionDeviceNamespace)
        return
