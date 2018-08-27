from socketIO_client_nexus import SocketIO

class SocketConnection:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        return

    def openSocket(self, namespace):
        socket = SocketIO(self.ip, self.port, namespace)
        return socket

    def closeSocket(self, SocketConnection):
        SocketConnection.close()
