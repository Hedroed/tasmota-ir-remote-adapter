"""Xiaomi adapter for WebThings Gateway."""

from gateway_addon import Adapter, Database

from .mitemp_device import TasmotaIRSensorDevice
from .util import print

_TIMEOUT = 3


class TasmotaIRAdapter(Adapter):
    """Adapter for Xiaomi temperature and humidity sensor devices."""

    def __init__(self, loop=None, verbose=False):
        """
        Initialize the object.

        verbose -- whether or not to enable verbose logging
        """
        self.name = self.__class__.__name__
        Adapter.__init__(self,
                         'tasmota-ir-remote-adapter',
                         'tasmota-ir-remote-adapter',
                         verbose=verbose)

        self.loop = loop

        self.pairing = False
        self.start_pairing(_TIMEOUT)

    def _add_from_config(self):
        """Attempt to add all configured devices."""
        database = Database('tasmota-ir-remote-adapter')
        if not database.open():
            return

        config = database.load_config()
        database.close()

        print(f'WIP: loading config {config}')

        if config.get('devices') is None:
            return

        for dev in config['devices']:

            _id = f"mitemp-{dev['ip'].replace('.', '-')}"
            if _id not in self.devices:
                device = TasmotaIRSensorDevice(self, _id, dev['ip'], dev['codes'], loop=self.loop)

                self.handle_device_added(device)

    def start_pairing(self, timeout):
        """
        Start the pairing process.

        timeout -- Timeout in seconds at which to quit pairing
        """
        if self.pairing:
            return

        self.pairing = True

        self._add_from_config()

        self.pairing = False

    def cancel_pairing(self):
        """Cancel the pairing process."""
        self.pairing = False
