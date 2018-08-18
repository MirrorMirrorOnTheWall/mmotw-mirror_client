from socketIO_client_nexus import SocketIO, BaseNamespace

class ProvisionDeviceNamespace(BaseNamespace):
    #   Tricky: "provision_response" is header name from server
    #   Library extracts name from function name and uses it to abract this ...
    #   socket.on('provision_response', on_provision_response)
    #   This will be used for call backs when expecting the server to return data
    def on_provisionResponse(self, *args):
        print('Response: {}'.format(args[0]))

    def on_connected(self):
        print('Connected to server socket...')

    def on_disconnected(self):
        print('Disconnected from server socket...')
