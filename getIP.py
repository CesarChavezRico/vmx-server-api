"""
Gets local IP address, if no IP within timeout then Exception
Gets Docker Container IP address, if no IP within timeout then Exception
"""

__author__ = 'Cesar'


import os
import re
import time
import config


def wait_local_ip():
    """
    Waits for a valid ip, on the host box, for config.delayIP seconds, if not ip trows exception
    """

    ip_match = None
    seconds = 0
    while ip_match is None:
        # Wait until Regular Expression Match
        if seconds < config.delayIP:
            time.sleep(1)
            seconds += 1
            config.logging.info('getIP: Trying to get host box IP ...')
            # Find LocalIp from OS
            ifconfig = os.popen('sudo ifconfig eth0').read()
            # Match LocalIp with Regular Expression
            ip_match = re.search('\d{1,3}.\d{1,3}\.\d{1,3}.\d{1,3}', ifconfig)
        else:
            config.logging.warning('getIP: TIMEOUT on: Host Box IP ...')
            raise GetIpException

    # Assign Result
    local_address = ip_match.group()
    config.logging.info('getIP: Local IP = {0}'.format(local_address))
    return local_address


def wait_docker_ip(container):
    """
    Waits for a valid ip, from the docker container, for config.delayIP seconds, if not ip trows exception
    """
    get_docker_ip_command = 'docker inspect --format \'{{{{ .NetworkSettings.IPAddress }}}}\' {0}'.format(container)

    ip_match = None
    seconds = 0
    while ip_match is None:
        # Wait until Regular Expression Match
        if seconds < config.delayIP:
            time.sleep(1)
            seconds += 1
            config.logging.info('getIP: Trying to get container: {0} IP ...'.format(container))
            # Find LocalIp from Docker
            ifconfig = os.popen('sudo -S {0}'.format(get_docker_ip_command)).read()
            ifconfig = ifconfig[:-1]
            # Match LocalIp with Regular Expression
            ip_match = re.search('\d{1,3}.\d{1,3}\.\d{1,3}.\d{1,3}', ifconfig)
        else:
            config.logging.warning('getIP: TIMEOUT on: {0} IP ...'.format(container))
            raise GetIpException

    # Assign Result
    local_address = ip_match.group()
    config.logging.info('getIP: Docker [{0}] IP = {1}'.format(container, local_address))
    return local_address


class GetIpException(Exception):
    def __init__(self, value):
        self.value = value
    config.logging.error('getIP: Error getting IP.')

    def __str__(self):
        return repr(self.value)

