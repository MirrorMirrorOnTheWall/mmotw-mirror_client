from transitions import Machine

class MagicMirrorFSM:
    states = ['start', 'initializing', 'provisioning', 'onboarding', 'death']

    def __init__(self, deviceType):
        self.deviceType = deviceType

        # Initialize the state machine
        self.machine = Machine(model=self, states=MagicMirrorFSM.states, initial='start')

        self.machine.add_transition(trigger='initDevice', source='start', dest='initializing')

        self.machine.add_transition('provisionDevice', 'initializing', 'provisioning')

        self.machine.add_transition('beginOnboarding', 'provisioning', 'onboarding')
