import logging
from pyalertme.zigbee import *
import struct
import time
import binascii
import threading

class Sensor(Device):

    def __init__(self, callback=None):
        """
        Sensor Constructor

        """
        Device.__init__(self, callback)

        # Type Info
        self.type = 'Button Device'
        self.version = 12345
        self.manu = 'PyAlertMe'
        self.manu_date = '2017-01-01'

        # Tamper State
        self.tamper_state = 0
        self.triggered = 0

    def process_message(self, message):
        """
        Process incoming message

        :param message: Dict of message
        :return:
        """
        super(Sensor, self).process_message(message)

        # ZigBee Explicit Packets
        if message['id'] == 'rx_explicit':
            profile_id = message['profile']
            cluster_id = message['cluster']

            source_addr_long = message['source_addr_long']
            source_addr_short = message['source_addr']

            if profile_id == PROFILE_ID_ALERTME:
                # AlertMe Profile ID
                cluster_cmd = message['rf_data'][2:3]

                if cluster_id == CLUSTER_ID_AM_SECURITY:
                    # Security Initialization
                    self._logger.info('Received Security Initialization')

                else:
                    self._logger.error('Unrecognised Cluster ID: %r', cluster_id)

            else:
                self._logger.error('Unrecognised Profile ID: %r', profile_id)