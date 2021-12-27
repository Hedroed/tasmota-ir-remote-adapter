"""Tasmota IR remote adapter for WebThings Gateway."""

from os import path
import signal
import sys
import time


sys.path.append(path.join(path.dirname(path.abspath(__file__)), 'lib'))

from pkg.tasmotair_adapter import TasmotaIRAdapter  # noqa
from pkg.util import print


_DEBUG = True
_ADAPTER = None


def cleanup(signum, frame):
    """Clean up any resources before exiting."""
    if _ADAPTER is not None:
        _ADAPTER.close_proxy()

    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    _ADAPTER = TasmotaIRAdapter(verbose=_DEBUG)
    # Wait until the proxy stops running, indicating that the gateway shut us
    # down.
    print('... Running forever')
    while _ADAPTER.proxy_running():
        print('running')
        time.sleep(300)

if __name__ == '__main__':
    main()
