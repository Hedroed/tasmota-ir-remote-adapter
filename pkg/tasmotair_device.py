"""Xiaomi adapter for WebThings Gateway."""

from gateway_addon import Device, Property, Action
import time
import requests
import struct
from typing import List, Dict

from .util import print


class TasmotaIRSensorDevice(Device):
    """Xiaomi smart bulb type."""

    def __init__(self, adapter, _id, ip: str, codes: List[Dict]):
        """
        Initialize the object.

        adapter -- the Adapter managing this device
        _id -- ID of this device
        """
        self.properties: List[Property]

        super().__init__(adapter, _id)

        self._type = []
        self.name = 'Tasmota IR Remote'
        self.description = 'A Tasmota IR remote'

        self.ip = ip
        self.codes = codes

        self.remote_actions = {}

        print(f'WIP: new {self.ip} device {self.codes}')

        for d in self.codes:
            code = d['code']
            name = d['name']

            action_name = f'Trigger {name}'
            self.add_action(action_name, {
                '@type': 'TriggerAction',
                'title': action_name,
                'description': f'Send code IR {code}',
            })

            self.remote_actions[action_name] = code

    def perform_action(self, action: Action):
        if action.name not in self.remote_actions:
            return action.stop()

        action.start()
        code = self.remote_actions[action.name]

        cmd = "{%22Protocol%22:%22NEC%22,%22Bits%22:32,%22Data%22:%22" + code + "%22}"

        res = requests.get(f'http://{self.ip}/cm?cmnd=IrSend%20{cmd}')
        res.raise_for_status()

        data: Dict = res.json()

        if data.get('IRSend') == "Done":
            print('Code sent successfully')

        action.start()
