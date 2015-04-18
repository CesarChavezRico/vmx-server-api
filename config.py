"""
api configuration file
"""
__author__ = 'Cesar'

import logging

# Logging
logging.basicConfig(format='%(asctime)s - [%(levelname)s]: %(message)s',
                    filename='/home/cesar/logs/vmx_server_api.log',
                    level=logging.DEBUG)

logging.getLogger("requests").setLevel(logging.WARNING)

# Allowed time to get a valid ip after power up
delayIP = 15

# VMX docker configuration
CONTAINER = 'vmx-environment'
RUN_VMX_SERVER = 'docker exec {0} /vmx/build/./VMXserver'.format(CONTAINER)
VMX_DIR = '/vmx'
SESSION = 'main_VMXserver'
MODEL = 'none'
PORT = 8081
