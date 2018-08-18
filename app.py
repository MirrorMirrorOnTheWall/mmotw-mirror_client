from MagicMirror import MagicMirrorDevice

config = {
            'deviceType': 'MagicMirror_v01',
            'port': 4200
        }

device = MagicMirrorDevice(config['deviceType'], config['port'])

device.run()
