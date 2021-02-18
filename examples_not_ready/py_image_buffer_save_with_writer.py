
# -----------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------


from arena_api.__future__.save import Writer
from arena_api.system import system


def example_entry_point():

    # Get connected devices ---------------------------------------------------

    # create_device function with no arguments would create a list of
    # device objects from all connected devices
    devices = system.create_device()
    if not len(devices):
        raise Exception(f'No device found!\n'
                        f'Please connect a device and run the example again.')
    print(f'Created {len(devices)} device(s)')

    device = devices[0]
    print(f'Device used in the example:\n\t{device}')

    # just to have a viewable image
    print('Setting \'Width\' and \'Height\' Nodes value to their '
          'max values')
    device.nodemap['Width'].value = device.nodemap['Width'].max
    device.nodemap['Height'].value = device.nodemap['Height'].max

    with device.start_stream(1):
        print('Stream started')

        buffer = device.get_buffer()
        print(f'Image buffer received')

        # create an image writer
        # The writer, optionally, can take width, height, and bits per pixel
        # of the image(s) it would save. if these arguments are not passed
        # at run time, the first buffer passed to the Writer.save()
        # function will configure the writer to the arguments buffer's width,
        # height, and bits per pixel
        writer = Writer()
        # default name for the image is 'image_<count>.jpg' where count
        # is a pre-defined tag that gets updated every time a buffer image
        # is saved. More custom tags can be added using
        # Writer.register_tag() function
        writer.save(buffer)
        print(f'Image saved {writer.saved_images[-1]}')

        device.requeue_buffer(buffer)
        print(f'Image buffer requeued')

    # device.stop_stream() is automatically called at the end of the
    # context manger scope

    # clean up ----------------------------------------------------------------

    # This function call with no arguments will destroy all of the
    # created devices. Having this call here is optional, if it is not
    # here it will be called automatically when the system module is unloading.
    system.destroy_device()
    print('Destroyed all created devices')


if __name__ == '__main__':
    print('WARNING:\nTHIS EXAMPLE MIGHT CHANGE THE DEVICE(S) SETTINGS!')
    print('Example started')
    example_entry_point()
    print('Example finished successfully')
