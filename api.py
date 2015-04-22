"""
Flask app to create a REST api for VMXserver.
"""
__author__ = 'cesar'

from flask import Flask, request
import config
import sys
from getIP import wait_local_ip, GetIpException
from vmx_server import VMXserver, VMXserverException
from server_utils import shutdown_server

app = Flask(__name__)
vmx = None

@app.route('/')
def title():
    return 'VMXserver API'


@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down'


@app.route('/get_models')
def get_models():
    return vmx.list_models()


@app.route('/get_server_parameters')
def get_server_parameters():
    return vmx.get_parameters()


@app.route('/process_image')
def process_image():
    """
    Processes an image based on the model recived.
        :param: image: URL of the image to process
        :param: model: UUID of the model to use in the processing
        :return: Result JSON
    """
    image = request.args.get('image')
    model = request.args.get('model')

    vmx.load_model(model)
    return vmx.process_image(image)


if __name__ == '__main__':
    config.logging.info('---Start VMXServer API---')
    try:
        # Get system ip
        local_ip_address = wait_local_ip()
    except GetIpException:
        config.logging.error('VMXServerAPI ended due to a failure getting IP Address')
        sys.exit(1)

    try:
        # Spin VMXserver handler
        vmx = VMXserver()
    except VMXserverException:
        config.logging.error('VMXServerAPI ended due to a failure starting VMXServer Handling')
        sys.exit(1)

    app.run(host=local_ip_address, port=config.PORT)
