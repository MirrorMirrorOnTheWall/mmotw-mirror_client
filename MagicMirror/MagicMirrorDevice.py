from .MagicMirrorFSM import MagicMirrorFSM
from .ClientSocket.SocketConnection import SocketConnection
from .ClientSocket.SocketNameSpaces import ProvisionDeviceNamespace, OnboardingNamespace
import json

#   TODO: rename string2JSON its really json to string *for transmission only*
#   TODO: Doc strings (basic -> still prototype)

class MagicMirrorDevice:
    def __init__(self, deviceType, port):
        self.deviceFSM = MagicMirrorFSM()
        self.ip = 'localhost'
        self.port = port
        self.deviceDetailsPath = 'deviceDetails.json'
        self.SocketConnection = SocketConnection(self.ip, self.port)
        self.header = {}

        print('Device is in state: {}'.format(self.deviceFSM.state))
        return

    def string2JSON(self, headerStr):
        #   In order to send json the single quotes must be replaces and the 'u' tag needs
        #   to be removed
        data = str(headerStr).replace("'", '"').replace('u', '')
        return data

    def provisionResponse(self, *args):
        #   Update header with device id info
        print('Provision Response: {}'.format(args[0]))
        self.header =  args[0]

    # This method will run indefinitely cycling through the FSM and perfrom actions
    def run(self):
        #   Cycle through FSM
        #       State 1: Initialize
        self.deviceFSM.initDevice(MagicMirrorDevice=self,deviceDetailsPath=self.deviceDetailsPath)
        print('Device is in state: {}'.format(self.deviceFSM.state))
        print('Device Header: '+str(self.header))

        #       State 2: Provision New Device in database if it has not already been registered
        if self.header['deviceId'] == '0': #   Zero will be reserved for unregistered devices
                                                     #   for client registration purposes
            self.deviceFSM.provisionDevice()
            print('Device is in state: {}'.format(self.deviceFSM.state))
            #   Listen to socket: specifically for provision device events (namespace)
            provisionSocket = self.SocketConnection.openSocket(ProvisionDeviceNamespace)
            pvNS = provisionSocket.get_namespace()


            #   Here we emit our current device details to the server and they will respond
            #   with a device id number for the client to save on the device
            #   This id number will be used to connect the UI to this camera device
            #   Note: Add these emitters and stuff to callbacks for FSM transitions??
            provisionSocket.emit('provisionRequest', self.string2JSON(self.header), self.provisionResponse)
            provisionSocket.on('provisionResponse', self.provisionResponse)
            provisionSocket.wait(seconds=1)

            #   Writing device details to disk as persisting data to load on next boot cycle
            with open(self.deviceDetailsPath, 'w') as f:
                json.dump(self.header, f)

            #   CLOSE SOCKET
            provisionSocket.emit('disconnected')
        else:
            print('Device Has already been registered: '+str(self.header))

        #   FRAMEWORK not implemented yet. This is a placeholder
        #   By this point the device has been provisioned by the server. This means that
        #   The server will have recorded this device in the DB with a device ID
        #   This device id will allow the connection of the FaceID engine to the
        #   mirror's UI components
        if self.header['deviceHasBeenOnboarded'] == '0':
            onboardingSocket = self.SocketConnection.openSocket(OnboardingNamespace)

            self.deviceFSM.onboarding()
            print('Device is in state: {}'.format(self.deviceFSM.state))
            onboardingSocket.emit('onboardingRequest', self.string2JSON(self.header))
            #   Here we expect the server to respond with onboarding data
            print('Device Header is now: '+str(self.header))

            onboardingSocket.emit('disconnected')
