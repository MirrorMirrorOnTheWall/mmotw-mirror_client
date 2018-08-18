from .ClientSocket.SocketConnection import SocketConnection
from .MagicMirrorFSM import MagicMirrorFSM

class MagicMirrorDevice:
    def __init__(self, deviceType, port):
        self.deviceFSM = MagicMirrorFSM(deviceType=deviceType)
        self.ip = 'localhost'
        self.port = port

        print('Device is in state: {}'.format(self.deviceFSM.state))

        # Connects devie to server via socketIO_client_nexus package
        socketConnection = SocketConnection(self.ip, self.port)
        self.socket = socketConnection.socket
        return

    # This method will run indefinitely cycling through the FSM and perfrom actions
    def run(self):
        # Connect to server

        # Cycle through FSM
        self.deviceFSM.initDevice()
        print('Device is in state: {}'.format(self.deviceFSM.state))

        self.deviceFSM.provisionDevice()
        print('Device is in state: {}'.format(self.deviceFSM.state))

        self.socket.emit('provisionRequest', '{"deviceType": "MagicMirror_v01"}')
        self.socket.wait(seconds=20)
        self.socket.emit('disconnected')

        self.deviceFSM.beginOnboarding()
        print('Device is in state: {}'.format(self.deviceFSM.state))
