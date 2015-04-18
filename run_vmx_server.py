"""
Spins a VMXserver in the current vmx-environment container

    ./VMXserver "[vmx main dir]" "[session name]" "[model to load]" "[docker ip]:[port]"
    ./VMXserver "/vmx" "test" "none" "172.17.0.59:8081"

"""
__author__ = 'cesar'

import config
import getIP
import os

config.logging.warning('... Start VMX Server run script ...')


ip = getIP.wait_docker_ip(config.CONTAINER)

command = '{0} {1} {2} {3} {4}:{5}'.format(config.RUN_VMX_SERVER,
                                           config.VMX_DIR,
                                           config.SESSION,
                                           config.MODEL,
                                           ip,
                                           config.PORT)

r = os.popen('echo {0}|sudo -S {1}'.format('ces', command))

config.logging.warning('... End VMX Server run script...')
