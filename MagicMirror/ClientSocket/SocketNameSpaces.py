from socketIO_client_nexus import BaseNamespace

class ProvisionDeviceNamespace(BaseNamespace):
    #   This can only be used for logging unless we can figure out how to return data
    #   From here

    def on_connect(self):
        print('PROVISION: Connected to server socket...')

    def on_disconnect(self):
        print('PROVISION: Disconnected from server socket...')


class OnboardingNamespace(BaseNamespace):

    def on_connect(self):
        print('ONBOARDING: Connected to server socket...')

    def on_disconnect(self):
        print('ONBOARDING: Disconnected from server socket...')
