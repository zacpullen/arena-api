# -------------------------------------------------------------------------
# Copyright (c) 2020, Lucid Vision Labs, Inc.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -------------------------------------------------------------------------

import os

from arena_api.system import system
import numpy as np              # pip install numpy


def example_entry_point():

    # create devices
    print('Creating devices')
    devices = system.create_device()
    try:
        device = devices[0]
    except IndexError as ie:
        print('No device found!')
        raise ie
    print(f'Device used in the example:\n\t{device}')

    # get nodes
    nodes = device.nodemap.get_node(['Width', 'Height', 'PixelFormat'])

    # nodes
    nodes['Width'].value = nodes['Width'].max

    print('Setting Height to its maximum value')
    height = nodes['Height']
    height.value = height.max

    # set pixel format to mono8, most cameras should support it
    print('Setting Pixel Format to Mono8')
    nodes['PixelFormat'].value = 'Mono8'
    device.nodemap.get_node('TestPattern').value = 'Pattern0'

    # grab and save an image buffer
    print('Starting stream')
    with device.start_stream(1):
        print('Grabbing an image buffer')
        image = device.get_buffer()  # optional args

        print(f' Width X Height = {image.width} x {image.height}')

        print('Converting image buffer to a numpy array')
        bytes_per_pixel = image.bits_per_pixel/8
        nparray = np.asarray(image.data, dtype=np.uint8)
        nparray.reshape((image.height, image.width, bytes_per_pixel))

        image_name = 'mono8_image_saved_as_mono8.raw'
        nparray.tofile(image_name)

        print(f' Saved image path is: {os.getcwd()}\\{image_name}')
        device.requeue_buffer(image)


if __name__ == '__main__':
    try:
        print('WARNING:\nTHIS EXAMPLE MIGHT CHANGE THE DEVICE(S) SETTINGS!')
        print('Example started')
        example_entry_point()
        print('Example finished successfully')
    except BaseException as be:
        print(be)
        raise be