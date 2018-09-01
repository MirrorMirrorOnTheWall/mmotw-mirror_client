import os
import json
from transitions import Machine
from .ClientSocket.SocketConnection import SocketConnection

class MagicMirrorFSM:
    states = ['start',
              'initializing',
              'provisioning',
              'onboarding',
              'faceDetection',
              'shutdown']

    def __init__(self):

        # Initialize the state machine
        self.machine = Machine(model=self, states=MagicMirrorFSM.states, initial='start')

        self.machine.add_transition(trigger='initDevice',
                                    source='start',
                                    dest='initializing',
                                    after='initializeDevice')

        self.machine.add_transition(trigger='provisionDevice',
                                    source='initializing',
                                    dest='provisioning')

        self.machine.add_transition(trigger='onboarding',
                                    source='provisioning',
                                    dest='onboarding')

        self.machine.add_transition(trigger='onboarding',
                                    source='initializing',
                                    dest='onboarding')

        #    Not implmenented
        self.machine.add_transition(trigger='onboardingComplete',
                                    source='initializing',
                                    dest='faceDetection')

        #    Not implmenented
        self.machine.add_transition(trigger='onboardingComplete',
                                    source='onboarding',
                                    dest='faceDetection')

    def initializeDevice(self, MagicMirrorDevice, deviceDetailsPath):
        if os.path.exists(deviceDetailsPath):
            #   Reads current device details from disk -> Maybe we should use like a Sqlite db
            deviceDetailsData = open(deviceDetailsPath)
            MagicMirrorDevice.header = json.load(deviceDetailsData)
        else:
            #   Default header used for initializing
            header = {"deviceType": "MagicMirror_v01",
                      "deviceId": '0',
                      "deviceHasBeenOnboarded": "0"} #Change this to test pre/post onboardingRequest
            MagicMirrorDevice.header = header

        #   Do more initializing stuff
