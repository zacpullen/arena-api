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

from pprint import pprint

from arena_api.system import system

if 1:
    def print(*args, **kwargs):
        pass
    pprint = print


def add_one_to_ip(ip):

    bit0, bit1, bit2, bit3 = ip.split('.')
    if bit3 == '254':  # Avoid 255
        bit3 = '1'
    else:
        bit3 = str(int(bit3) + 1)
    return f'{bit0}.{bit1}.{bit2}.{bit3}'


def example_entry_point():

    # Discover devices --------------------------------------------------------

    print('Discover devices on network')
    device_infos1 = system.device_infos
    if not device_infos1:
        raise BaseException('No device is found!')
    device_info1 = device_infos1[0]
    print('Device1 info: ')
    pprint(device_info1, indent=4)

    # Create new IP -----------------------------------------------------------

    print('Current IP = ', device_info1['ip'])
    new_ip = add_one_to_ip(device_info1['ip'])
    device_info1_new = {
        'mac': device_info1['mac'],
        'ip': new_ip,
        'subnetmask': device_info1['subnetmask'],
        'defaultgateway': device_info1['defaultgateway']
    }
    print('New IP     = ', device_info1_new['ip'])
    # Force IP ----------------------------------------------------------------

    # Note: The force_ip function can also take a list of device infos to
    # force new IP addesses for multiple devices.
    print('New IP is being forced')
    system.force_ip(device_info1_new)
    print('New IP was forced successfully')

    # Discover devices --------------------------------------------------------

    print('Discover devices on network --------------------------------------')
    device_infos2 = system.device_infos
    if not device_infos2:
        raise BaseException('No device is found!')
    device_info2 = device_infos2[0]
    print('Device2 info: ')
    pprint(device_info2, indent=4)

    if device_info2 != device_info1_new:
        #raise Exception('device_info did not update')
        pass

    # create device with new ip
    system.create_device(device_info1_new)


if __name__ == '__main__':

    print('WARNING:\nTHIS EXAMPLE MIGHT CHANGE THE DEVICE(S) SETTINGS!')
    print('Example started')
    example_entry_point()
    print('Example finished successfully')
