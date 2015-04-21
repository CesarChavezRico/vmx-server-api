"""
Class that identifies a VMXserver.
"""
__author__ = 'cesar'

import requests
import config
import getIP

BUCKET = 'ocr-test-pics-cropped'
IMAGE = 'red-a6309a03-aa26-493c-99db-ba68cfa225c8.jpg'


class VMXserver():
    ip = None
    port = None

    def _server_alive(self):
        """
        Makes a simple request to tha VMXserver to check it's status
        :return: True if server OK, False otherwise
        """
        try:
            config.logging.debug('Checking if server @ {0} is alive'.format(self.ip))
            alive = self._ping()['error']
            if alive == 0:
                return True
            else:
                return False
        except requests.RequestException as e:
            config.logging.error('Requests Exception: {0}'.format(e.__str__()))
            return False

    def _ping(self):
        """
        Gets current server operational parameters
            :return: JSON of parameters
        """
        data = '{"command":"get_config"}'
        config.logging.debug('Pinging server @ {0}:{1} with: {2}'.format(self.ip, self.port, data))
        r = requests.post("http://{0}:{1}".format(self.ip, self.port), data=data)
        res = r.json()
        config.logging.debug('Response to Ping: {0}'.format(res))
        return res

    def __init__(self):
        """
        Inits a communication with a VMXserver
        """
        self.ip = getIP.wait_docker_ip(config.CONTAINER)
        self.port = str(config.PORT)
        if self._server_alive():
            pass
        else:
            raise VMXserverException('Server not found!')

    def process_image(self, url):
        """
        Process an image (from Google Cloud Storage) in this VMXserver.
            :param url:
            :return: JSON of detected objects
        """
        data = '{{"command":"process_image",' \
               '  "images":' \
               '     [{{"image":"{0}"}}]' \
               '}}'.format(url)

        r = requests.post("http://{0}:{1}".format(self.ip, self.port), data=data)
        return r.text

    def get_parameters(self):
        """
        Gets current server operational parameters
            :return: JSON of parameters
        """
        data = '{"command":"get_params"}'
        r = requests.post("http://{0}:{1}".format(self.ip, self.port), data=data)
        return r.text

    def list_models(self):
        """
        Gets current server models stored on the VMXserver
            :return: JSON of models list
        """
        data = '{"command":"list_models"}'
        r = requests.post("http://{0}:{1}".format(self.ip, self.port), data=data)
        return r.text

    def load_model(self, uuid):
        """
        Loads a model (by uuid) to perform detections on current VMXserver
            :param: uuid: Unique identifier of the model
            :return: True if model loaded successfully, False otherwise
        """
        data = '{{"command":"load_model",' \
               '  "uuids":' \
               '     ["{0}"]' \
               '}}'.format(uuid)

        r = requests.post("http://{0}:{1}".format(self.ip, self.port), data=data)
        return r.text


class VMXserverException(Exception):
    def __init__(self, value):
        self.value = value
        config.logging.error('VMXserver: Error!: {0}'.format(self.__str__()))

    def __str__(self):
        return repr(self.value)

