# -----------------------------------------------------------------------------
# Copyright (c) 2020, Lucid Vision Labs, Inc.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -----------------------------------------------------------------------------
import time
import math
from ctypes import c_ubyte

from arena_api.buffer import BufferFactory
from arena_api.system import system
from arena_api.__future__ import save
from arena_api import enums

# TODO Clean up comments for this

def print_buffer(buffer):
    print('\n')

    for index, pixel in enumerate(buffer.data):
        if index % buffer.width:
            print(pixel, ' ', end='')
        else:
            print('\n')
            print(pixel, ' ', end='')

    print('\n')


def print_buffer_p(list_p, width, height, bpp=1):

    print('\n')

    for index in range(width * height * int(bpp / 8)):
        if index % width:
            print(list_p[index], ' ', end='')
        else:
            print('\n')
            print(list_p[index], ' ', end='')

    print('\n')


def create_devices_with_tries():
    """
    This function will let users know that a device is needed and
    gives them a chance to connect a device instead of raising an exception
    """

    tries = 0
    tries_max = 6
    sleep_time_secs = 10
    while tries < tries_max:  # Wait for device for 60 seconds
        devices = system.create_device()
        if not devices:
            print(f'Try {tries + 1} of {tries_max}: waiting for {sleep_time_secs} '
                  f'secs for a device to be connected!')
            for sec_count in range(sleep_time_secs):
                time.sleep(1)
                print(f'{sec_count + 1} seconds passed ',
                      '.' * sec_count, end='\r')
            tries += 1
        else:
            print(f'Created {len(devices)} device(s)')
            return devices
    else:
        raise Exception(f'No device found! Please connect a device and run '
                        f'the example again.')

# TODO proper name
# TODO document algo


def split_sub_tiles(src, dst, src_ptr_index, dst_ptr_index):
    src_pdata = src.pdata
    dst_pdata = dst.pdata
    for i in range(0, src.height, 2):  # step of 2
        for j in range(0, src.width, 2):  # step of 2
            dst_pdata[dst_ptr_index] = src_pdata[src_ptr_index]
            dst_pdata[dst_ptr_index + 1] = src_pdata[src_ptr_index + 1]

            src_ptr_index += src.double_bytes_per_pixel
            dst_ptr_index += dst.bytes_per_pixel
        src_ptr_index += src.stride
        dst_ptr_index += dst.half_stride


# TODO proper name
# TODO document algo
def split_tiles(src, dst):
    # references positions in source buffer.
    src.top_left_index = 0
    src.top_right_index = src.bytes_per_pixel
    src.bottom_left_index = src.stride
    src.bottom_right_index = src.stride + src.bytes_per_pixel

    # reference to starting position of each quadrant of destination 2x2
    # grid to write to
    dst.top_left_index = 0
    dst.top_right_index = dst.half_stride
    dst.bottom_left_index = dst.half_image_data_size
    dst.bottom_right_index = dst.half_image_data_size + dst.half_stride

    split_sub_tiles(src, dst, src.top_left_index, dst.top_left_index,)
    split_sub_tiles(src, dst, src.top_right_index, dst.top_right_index)
    split_sub_tiles(src, dst, src.bottom_left_index, dst.bottom_left_index)
    split_sub_tiles(src, dst, src.bottom_right_index, dst.bottom_right_index)


def create_hsv_buffer_from_splitted_tiles_buffer(splited_tiles_buffer):
    buffer = splited_tiles_buffer

    # hsv information

    # TODODODODOD
    hsv_bits_per_pixel = 24  # enums.PixelFormat.BGR8.value # outBitsPerPixel
    ###
    hsv_bytes_per_pixel = int(hsv_bits_per_pixel / 8)  # outPixelSize
    hsv_width = buffer.width
    hsv_height = buffer.height
    hsv_image_data_size = buffer.width * \
        hsv_height * hsv_bytes_per_pixel  # outDataSize
    # pOutput # initialized to zeros

    hsv_byte_array = (c_ubyte * hsv_image_data_size)()

    # Convert 2-channel 8-bits-per-channel DoLP AoLP
    #    The first channel of each pixel holds the DoLP data and has a
    #    maximum
    #    value of 255; the second channel of each pixel holds the AoLP data
    #    and
    #    has a maximum value of 201.
    print(f'Using AoLP as hue and DoLP as saturation, convert from HSV '
          f'to {enums.PixelFormat.BGR8.name}\n')

    # TODO CHECK IF THIS IS NEEDED
    # https://ponderosabay.atlassian.net/browse/SFW-3203
    # if buffer.pixel_format ==
    # enums.PixelFormat.LUCID_PolarizedDolpAolp_BayerRG8
    # #define LUCID_PolarizedDolpAolp_BayerRG8 0x8210029F
    if buffer.pixel_format is not enums.PixelFormat.PolarizedDolpAolp_BayerRG8:
        raise Exception('This example requires PolarizedDolpAolp_BayerRG8 '
                        'pixel format')

    buffer_index = 0  # not in c++ example
    hsv_index = 0  # not in c++ example
    for _ in range(buffer.width * buffer.height):  # number of pixles in buffer
        # Separate the AoLP and DoLP channels
        #    The first channel is the DoLP (degree of linear polarization)
        #    channel.  The second channel is the AoLP (angle of linear
        #    polarization) channel.
        dolpValue = float(buffer.pdata[buffer_index])
        aolpValue = float(buffer.pdata[buffer_index + 1])

        # Map to hue, saturation, and value
        #    For the formula to work, double the AoLP for the hue and map
        #    the DoLP values between 0 and 1 for saturation.  Maximize
        #    value
        #    to keep things bright.
        hue = aolpValue * 2.0
        if hue > 255.0:
            hue = 255.0
        saturation = dolpValue / 255.0
        value = 255.0

        # Calculate chroma, hue', and x (second largest component)
        #    These intermediary values help in the conversion of HSV to the
        #    displayable pixel format.
        c = value * saturation
        h = hue / 60.0
        x = c * (1 - abs(math.fmod(h, 2.0) - 1))

        # Calculate blue, green, and red
        #    Blue, green, and red can be calculated from hue, saturation,
        #    and value, and the intermediary values chroma, hue', and x.
        blue = 0.0
        green = 0.0
        red = 0.0

        # colors between red and yellow
        if 0 <= h <= 1:
            blue = value - c
            green = x + value - c
            red = value

        # colors between yellow and green
        elif 1 <= h <= 2:
            blue = value - c
            green = value
            red = x + value - c

        # colors between green and cyan
        elif 2 <= h <= 3:
            blue = x + value - c
            green = value
            red = value - c

        # colors between cyan and blue
        elif 3 <= h <= 4:
            blue = value
            green = x + value - c
            red = value - c

        # colors between blue and magenta
        elif 4 <= h <= 5:
            blue = value
            green = value - c
            red = x + value - c

        # colors between magenta and red
        elif 5 <= h <= 6:
            blue = x + value - c
            green = value - c
            red = value

        # set pixel format values and move to next pixel
        hsv_byte_array[hsv_index] = int(blue)
        hsv_byte_array[hsv_index + 1] = int(green)
        hsv_byte_array[hsv_index + 2] = int(red)

        buffer_index += buffer.bytes_per_pixel
        hsv_index += hsv_bytes_per_pixel

    return BufferFactory.create(hsv_byte_array, hsv_image_data_size, hsv_width,
                                hsv_height, enums.PixelFormat.BGR8)


def acquire_an_image_and_save_as_DoLPAoLP(device):
    nodemap = device.nodemap

    # get node values that will be changed in order to return their values at
    # the end of the example
    pixelformat_node = nodemap['PixelFormat']
    pixelformat_initial_value = pixelformat_node.value

    # Change to DoLP AoLP pixel format
    #    DoLP AoLP pixel formats are a 2-channel image.  The first channel
    #    holds
    #    DoLP (Degree of Linear Polarization) data while the second holds AoLP
    #    (Angle of Linear Polarization) data.
    print('Set PolarizedDolpAolp_BayerRG8 to pixel format\n')
    pixelformat_node.value = 'PolarizedDolpAolp_BayerRG8'

    #nodemap['Width'].value = nodemap['Width'].min
    #nodemap['Height'].value = nodemap['Height'].min
    #nodemap['TestPattern'].value = 'Pattern4'

    # retrieve image
    with device.start_stream():

        src = device.get_buffer()

        # src info ------------------------------------------------------------
        src.bytes_per_pixel = int(src.bits_per_pixel / 8)
        src.double_bytes_per_pixel = src.bytes_per_pixel * 2
        src.stride = src.width * int(src.bits_per_pixel / 8)

        # dst info ------------------------------------------------------------
        # create a copy from the buffer to rearrange its data as tiles
        dst = BufferFactory.copy(src)
        dst.bytes_per_pixel = int(dst.bits_per_pixel / 8)
        dst.stride = src.stride
        dst.half_stride = int(dst.stride / 2)
        # not using Buffer.buffer_size
        # Buffer.buffer_size = imagedata size + chunkdata size.
        # Image data is what interset us
        dst.half_image_data_size = int(
            dst.width * dst.height * (dst.bits_per_pixel / 8) / 2)

        # initi ###############################################################
        '''
        print('## change vals ')
        for index in range(dst.half_image_data_size * 2):
            src.pdata[index] = index
            dst.pdata[index] = src.pdata[index] + 100
            pass

        print('## initial ')
        print_buffer(src)
        print_buffer(dst)
        '''
        #######################################################################

        # split bayer tile data into 2x2 grid
        print('Splitting bayer tile data into 2x2 grid\n')
        split_tiles(src, dst)

        print('## new arr')
        #print_buffer(src)
        #print_buffer(dst)

        # Manually convert to HSV image
        # ---------------------------------------------------
        #   Treat the AoLP data as hue and the DoLP data as saturation, and
        #   manually
        #   convert from HSV to the desired pixel format: algorithm available
        #   on Wikipedia:
        #   https://en.wikipedia.org/wiki/HSL_and_HSV#From_HSV

        hsv = create_hsv_buffer_from_splitted_tiles_buffer(dst)

        # Save hsv buffer --------------------------------------------------------
        hsv_writer = save.Writer.from_buffer(hsv)
        hsv_writer.save(hsv, 'hsv.jpg')
        print(hsv_writer.saved_images[-1]) # last saved buffer
        
        # clean up
        device.requeue_buffer(src) # made by device.get_buffer()
        BufferFactory.destroy(dst) # made by BufferFactory.copy()
        BufferFactory.destroy(hsv) # made by BufferFactory.create()

    # return nodes to their initial values
    pixelformat_node.value = pixelformat_initial_value


def example_entry_point():

    # Create a device ---------------------------------------------------------
    devices = create_devices_with_tries()
    device = devices[0]
    print(f'Device used in the example:\n\t{device}')

    acquire_an_image_and_save_as_DoLPAoLP(device)
    # Clean up ----------------------------------------------------------------

    # Destroy all created devices.  This call is optional and will
    # automatically be called for any remaining devices when the system module
    # is unloading.
    system.destroy_device()
    print('Destroyed all created devices')


if __name__ == '__main__':
    print('\nWARNING:\nTHIS EXAMPLE MIGHT CHANGE THE DEVICE(S) SETTINGS!')
    print('\nExample started\n')
    example_entry_point()
    print('\nExample finished successfully')
