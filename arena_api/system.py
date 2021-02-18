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

from copy import deepcopy
from ipaddress import ip_address

from arena_api._xlayer.xarena._xglobal import _xGlobal
from arena_api._xlayer.xarena._xsystem import _xSystem
from arena_api._xlayer.xarena.arenac_defaults import \
    UPDATE_DEVICES_TIMEOUT_MILLISEC_DEFAULT as \
    _UPDATE_DEVICES_TIMEOUT_MILLISEC_DEFAULT
from arena_api._device import Device as _Device
from arena_api._nodemap import Nodemap as _Nodemap


class _System():
    '''
    The System is the entry point to the ``Arena SDK``. The class
    is a singleton and an instance gets created when
    ``arena_api`` module is imported. use
    ``from arena_api.system import system`` to import the system instance.

    The class manages devices ``Device`` and the Transport Layer
    System node map ``system.tl_system_nodemap`` by :\n
    \t- maintaing a list of enumerated devices ``system.device_infos``,
    \t- creating and destroying devices ``system.create_device()`` and\
    ``system.destroy_device()``,
    \t- and providing access to its node map ``tl_system_nodemap``

    :warning:
    - The instance of ``System``, ``system`` is created when \
    ``arena_api.system`` module is imported the first time. Every \
    other import after that would return the same instance.
    - You may not import ``_System`` nor create it directly. Instead, Import \
    the system instance as follows ``from arena_api.system import system``.

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    __singleton = None
    __run_init = True

    def __new__(cls, *args, **kwargs):

        if not cls.__singleton:
            cls.__singleton = super(_System, cls).__new__(
                cls, *args, ** kwargs)
        return cls.__singleton

    def __init__(self):

        if not self.__run_init:
            return
        else:
            self.__run_init = False

        self.__xsystem = None
        self.__device_infos = []
        self.__created_devices = {}  # {mac value : device}
        self.__DEVICE_INFOS_TIMEOUT_MILLISEC = _UPDATE_DEVICES_TIMEOUT_MILLISEC_DEFAULT
        self.__open()

    # ---------------------------------------------------------------------

    def __del__(self):
        self.__close()

    # ---------------------------------------------------------------------

    def __open(self):
        if not self.__xsystem:
            hxsystem = _xGlobal.xOpenSystem()
            self.__xsystem = _xSystem(hxsystem)
            # initialize the callback
            from arena_api.callback import callback
        else:
            return self

    # ---------------------------------------------------------------------

    def __close(self):
        if self.__xsystem:
            # clean up before close system
            if len(self.__created_devices) != 0:
                self.destroy_device()

            _xGlobal.xCloseSystem(self.__xsystem.hxsystem)

        self.__xsystem = None
        self.__device_infos.clear()
        self.__device_infos = None
        if self.__created_devices != {}:
            raise BaseException(
                'Internal: __connect_devices list is not updated')

    # ---------------------------------------------------------------------

    def __get_DEVICE_INFOS_TIMEOUT_MILLISEC(self):
        return self.__DEVICE_INFOS_TIMEOUT_MILLISEC

    def __set_DEVICE_INFOS_TIMEOUT_MILLISEC(self, value):
        if isinstance(value, int):
            self.__DEVICE_INFOS_TIMEOUT_MILLISEC = value
        else:
            raise TypeError('expected int or float values')
    DEVICE_INFOS_TIMEOUT_MILLISEC = property(
        __get_DEVICE_INFOS_TIMEOUT_MILLISEC,
        __set_DEVICE_INFOS_TIMEOUT_MILLISEC)
    '''
    Time to wait for connected devices to respond. The default value
    is ``100`` millisec.

    :getter: Returns the current timeout.
    :setter: Sets the timeout. expects int or float.
    :type: int

    When ``system.device_infos`` is called, the system broadcasts a discovery
    packet to all interfaces, waiting until the end of the timeout for any
    responses from enumerated devices.

    The GigE Vision spec requires devices respond to a broadcast discovery
    packet within one second unless set
    otherwise ``device.get_node('DiscoveryAckDelay')``.

    Lucid devices are set to respond within 100 ms. Therefore, 100 works
    as an appropriate timeout value in many use cases.This response
    time can be customized through the ``DiscoveryAckDelay`` feature, if
    supported. The timeout value should reflect any such changes.

    :warning: \n
    - Slightly affects bandwidth usage due to the broadcasting of
      discovery packets.
    - Discovers devices on all subnets, even when unable to communicate
      with them due to IP configuration. \n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''

    # ---------------------------------------------------------------------

    def __get_interface_infos(self):
        num_of_interfaces = self.__xsystem.xSystemGetNumInterfaces()
        all_interfaces_info = []
        for index in range(num_of_interfaces):
            interface_info = {}
            interface_info['ip'] = self.__xsystem.xSystemGetInterfaceIpAddressStr(
                index)
            interface_info['subnetmask'] = self.__xsystem.xSystemGetInterfaceSubnetMaskStr(
                index)
            interface_info['mac'] = self.__xsystem.xSystemGetInterfaceMacAddressStr(
                index)
            all_interfaces_info.append(interface_info)

        return all_interfaces_info

    interface_infos = property(__get_interface_infos)
    '''
    A list of dictionaries that informs about interfaces.
    Each dictionary represents an interface on the host.
    an interface info dictionary has the following keys: ``ip``,\
     ``subnetmask``, and ``mac``. User changes to the\
    values of the dictionary will not reflect on the device.\n
    -----------------------------------------------------------------------
    **ip**: a string value that represets the IP address, in
    dot-decimal notation, of the interface on the host.
    An interface has its IP address, subnet mask, and mac address checked
    through the Transport Layer Interface node map:
    ``GevInterfaceIPAddress``, ``GevInterfaceSubnetMask``,
    ``GevInterfaceMACAddress``.\n
    -----------------------------------------------------------------------
    **subnetmask**: a string value that represets the subnet mask, in
    dot-decimal notation, of the interface on the host.
    An interface has its IP address, subnet mask, and mac address checked
    through the Transport Layer Interface node map:
    ``GevInterfaceIPAddress``, ``GevInterfaceSubnetMask``,
    ``GevInterfaceMACAddress``.\n
    -----------------------------------------------------------------------
    **mac**: A string value that represents the MAC address of the
    interface on the host.
    An interface has its IP address, subnet mask, and mac address checked
    through the Transport Layer Interface node map:
    ``GevInterfaceIPAddress``, ``GevInterfaceSubnetMask``,
    ``GevInterfaceMACAddress``.\n
    -----------------------------------------------------------------------

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # device_infos --------------------------------------------------------

    def __get_device_infos(self):

        # update devices first otherwise it will be zero devices
        device_info_has_changed = self.__xsystem.xSystemUpdateDevicesHasChanged(
            self.DEVICE_INFOS_TIMEOUT_MILLISEC)

        num_of_devices = self.__xsystem.xSystemGetNumDevices()
        device_infos = []
        for index in range(num_of_devices):
            device_info = {}

            device_info['model'] = self.__xsystem.xSystemGetDeviceModel(index)
            device_info['vendor'] = self.__xsystem.xSystemGetDeviceVendor(
                index)
            device_info['serial'] = self.__xsystem.xSystemGetDeviceSerial(
                index)
            device_info['ip'] = self.__xsystem.xSystemGetDeviceIpAddressStr(
                index)
            device_info['subnetmask'] = self.__xsystem.xSystemGetDeviceSubnetMaskStr(
                index)
            device_info['defaultgateway'] = self.__xsystem.xSystemGetDeviceDefaultGatewayStr(
                index)
            device_info['mac'] = self.__xsystem.xSystemGetDeviceMacAddressStr(
                index)
            device_info['name'] = self.__xsystem.xSystemGetDeviceUserDefinedName(
                index)
            device_info['version'] = self.__xsystem.xSystemGetDeviceVersion(
                index)
            device_info['dhcp'] = self.__xsystem.xSystemIsDeviceDHCPConfigurationEnabled(
                index)
            device_info['presistentip'] = self.__xsystem.xSystemIsDevicePersistentIpConfigurationEnabled(
                index)
            device_info['lla'] = self.__xsystem.xSystemIsDeviceLLAConfigurationEnabled(
                index)
            device_infos.append(device_info)

        # update old list
        # index is the device info position
        del self.__device_infos[:]
        self.__device_infos = deepcopy(device_infos)

        return device_infos
    # calling this will update the inner __device_infos list as well
    device_infos = property(__get_device_infos)
    '''
    A list of dictionaries used to create devices. Each dictionary
    represents a discovered device on the network.
    A device info dictionary has the following keys: ``model``,
    ``vendor``, ``serial``, ``ip``, ``subnetmask``,
    ``defaultgateway``, ``mac``, ``name``, ``dhcp``,
    ``presistentip``, ``lla``, and ``version``. User changes  the
    values of the dictionary will not reflect on the device.\n
    -----------------------------------------------------------------------
    **model**: a string value that represents the model name of the
    discovered device. Model names are used to differentiate
    between products. Lucid Vision model names: PHX050S-MC, PHX032S-CC,
    TRI032S-MC. The model name is the same as the one received
    in the GigE Vision discovery acknowledgement.\n
    -----------------------------------------------------------------------
    **vendor**: a string value that represents the vendor/manufacturer
    name of the discovered device.
    Vendor names differentiate between device vendors/manufacturers.
    Lucid devices return 'Lucid Vision Labs'.
    The vendor name is the same as the one received
    in the GigE Vision discovery acknowledgement.\n
    -----------------------------------------------------------------------
    **serial**: a string value that represents the serial number of the
    discovered device.
    A serial number differentiates between devices.
    Each Lucid device has a unique serial number. Lucid serial numbers are
    numeric, but the serial numbers of other vendors may be alphanumeric.
    The serial number is the same as the one received in the GigE Vision
    discovery acknowledgement.
    \t:warning:
    \t- Serial numbers from different manufacturers may overlap.\n
    -----------------------------------------------------------------------
    **ip**: a string value that represets the discovered device
    IP address on the network in dot-decimal notation.This IP
    address is the same as the one received in the GigE Vision
    discovery acknowledgement, but as a dot-separated string.
    The GigE Vision specification only allows for IPv4 IP addresses.
    A device may have its IP address, subnet mask, and default gateway
    assigned by LLA or DHCP, set as persistent, or temporarily forced.
    They can be checked through the main node map nodes:
    ``GevCurrentIPAddress``, ``GevCurrentSubnetMask``,
    ``GevCurrentDefaultGateway``.\n

    - DHCP ``GevCurrentIPConfigurationDHCP`` and IP persistence\
    ``GevCurrentIPConfigurationPersistentIP`` can be enabled/disabled\
    through the node map. If both are enabled, a device will default\
    to its persistent IP settings. If neither, it will default to LLA\
    ``GevCurrentIPConfigurationLLA``, which cannot be disabled.\n

    - In order to configure a device to use a persistent IP\
    configuration, not only must IP persistence be enabled\
    ``GevCurrentIPConfigurationPersistentIP``, but\
    the IP address ``GevPersistentIPAddress``,\
    subnet mask ``GevPersistentSubnetMask``, and\
    default gateway ``GevPersistentDefaultGateway`` must be set.\n

    - Forcing an IP  temporarily changes an IP address, subnet mask,\
    and default gateway of a device.\
    A forced IP configuration will reset on a device reboot\
    ``DeviceReset``.\n

    - A persistent IP may be quicker to enumerate than DHCP, which\
    should be faster than LLA\n
    -----------------------------------------------------------------------
    **subnetmask**: a string value that represets the discovered device
    subnet mask on the network in dot-decimal notation. This subnet
    mask is the same as the one received in the GigE Vision
    discovery acknowledgement, but as a dot-separated string.
    The GigE Vision specification only allows for IPv4 subnet masks.
    A device may have its IP address, subnet mask, and
    default gateway assigned by LLA or DHCP, set as persistent,
    or temporarily forced. They can be checked through the
    main node map ``GevCurrentIPAddress``, ``GevCurrentSubnetMask``,
    ``GevCurrentDefaultGateway``.\n

    - DHCP ``GevCurrentIPConfigurationDHCP`` and IP persistence\
    ``GevCurrentIPConfigurationPersistentIP`` can be \
    enabled/disabled through the node map. If both are enabled, a\
    device will default to its persistent IP settings.\
    If neither, it will default to LLA ``GevCurrentIPConfigurationLLA``\
    which cannot be disabled.\n

    - In order to configure a device to use a persistent IP\
    configuration, not only must IP persistence be enabled \
    ``GevCurrentIPConfigurationPersistentIP``, \
    but the IP address ``GevPersistentIPAddress``,\
    subnet mask ``GevPersistentSubnetMask``, \
    and default gateway ``GevPersistentDefaultGateway`` must be set.\n

    - Forcing an IP temporarily changes an IP address, \
    subnet mask, and default gateway of a device. A forced IP \
    configuration will reset on a device reboot ``DeviceReset``.\n

    - A persistent IP may be quicker to enumerate than DHCP, which \
    should be faster than LLA.\n
    -----------------------------------------------------------------------
    **defaultgateway**: a string value represents the default gateway\
    of the discovered device.\n
    -----------------------------------------------------------------------
    **mac**: a string value that represents MAC address of the\
    discovered device on the network. The MAC address returned \
    by this getter is the same as the one received in the GigE Vision \
    discovery acknowledgement.
    -----------------------------------------------------------------------
    **name**: a string value that represents User-defined name of
    a device. If supported, it is a customizable string with a maximum
    of 16 bytes that can be used to identify a device ``DeviceUserID``.
    \t:warning:
    \t- Not necessarily supported\n
    -----------------------------------------------------------------------
    **dhcp**: a bool value that represents whether DHCP is enabled
    on the discovered device. True if DHCP enabled Otherwise, false.\n
    -----------------------------------------------------------------------
    **presistentip**: a bool value that represents whether
    persistent IP is enabled on the discovered device. True if persistent
    IP enabled otherwise, false.\n
    -----------------------------------------------------------------------
    **lla**: a bool value that represents whether LLA is enabled on
    the device. True if LLA enabled  Otherwise, false.\n
    -----------------------------------------------------------------------
    **version**: a string value that represents the version of the device
    currently running on the device. For Lucid devices, this refers
    to firmware version.\n
    -----------------------------------------------------------------------

    :warning:
    - this is not guaranteed to keep the order of device infos in the \
    list even if there is no change in the number of devices.

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # create_device -------------------------------------------------------

    def create_device(self, device_infos=None):
        '''
        Creates and initializes ``arena_api._device.Device`` instance(s)\
        from device_infos argument. The device(s) must be destroyed\
        using ``arena_api.system.destroy_device()`` when no longer needed.

        **Args**:
            device_infos : can be\n
                - list of device info dicts which is obtained from\
                ``system.device_infos``. Also, it can be a sliced list from\
                the full list returned from ``system.device_infos``.\n
                - a device info dict is acceptable in case the user\
                 wants to create one device from ``system.device_infos``\
                 list.\n
                - ``None``. This is the default value. The system\
                calls ``system.device_infos`` and create all of the\
                devices in the returned list. \
                in other words, if these calls as the same:\n
                    - ``system.create_device(system.device_infos)``
                    - ``system.create_device()``
        **Raises**:
            - ``ValueError`` :
                - device_infos is an empty list.
            - ``TypeError`` :
                - device_infos type is not a list of dicts, a dict, nor None.
                - device_infos is a dict with MAC Address of a device\
                that is not on the network.\n
            - BaseException :
                - device_info is a dict and ``system.device_infos``\
                was not called.\n
        **Returns**:
            - A list of ``arena_api._device.Device`` instances.\n

        When called, prepares each device for user interaction,
        opening the control channel socket and initializing all node
        maps. The returned device(s) are ready to stream images,
        send events, and read or customize features.

        A single process may only create a single device once, but a
        single device may be opened on multiple processes.
        The first process to create the device is given read-write
        access. Additional processes are given read-only access.
        With read-only access, processes can read features and
        receive images and events; they cannot, however, write
        values, start the image stream or initialize events.

        :warning:
        - This is the only way ``arena_api._device.Device``\
        instances are created.
        - Provides read-write access only to initial process that creates\
        the device; following processes given read-only access.
        - Devices must be destroyed.

        **------------------------------------------------------------------**\
        **-------------------------------------------------------------------**
        '''

        device_infos_as_list = None

        # Handle different types -------------------------------------------

        # None
        if device_infos is None:
            device_infos_as_list = self.device_infos

        # single dict
        elif isinstance(device_infos, dict):
            # make it in a list
            device_infos_as_list = [device_infos]

        # list
        elif isinstance(device_infos, list):
            if len(device_infos) == 0:
                raise ValueError('input can not be an empty list')
            device_infos_as_list = device_infos

        # other types
        else:
            raise TypeError(f'Expected list of dicts, a dict, or None '
                            f'instead of {type(device_infos).__name__}')

        # create devices from device info ----------------------------------

        devices = []
        for device_info in device_infos_as_list:
            self.__validate_device_info_before_create_device(device_info)

            # new device
            if device_info['mac'] not in self.__created_devices.keys():
                new_device = self.__create_new_device(device_info)
                devices.append(new_device)
                self.__created_devices[device_info['mac']] = new_device
            # existing device
            else:
                existing_device = self.__created_devices[device_info['mac']]
                devices.append(existing_device)

        return devices

    def __validate_device_info_before_create_device(self, device_info):

        # no device_info has been broadcasted
        if self.__device_infos == []:
            raise BaseException('Call system.device_infos first')

        # list has an element that is not dict
        elif not isinstance(device_info, dict):
            raise TypeError(f'Expected a list of dicts instead of a list '
                            f'that has a {type(device_infos).__name__} '
                            f'element')

        # unknown mac
        for info in self.__device_infos:
            if info['mac'] == device_info['mac']:
                break
        else:
            raise ValueError(f'Invalid device_info : {device_info}')

    def __create_new_device(self, device_info):
        # find index of device_info to create it
        device_index = self.__get_device_index(device_info)
        hxdevice = self.__xsystem.xSystemCreateDevice(device_index)
        new_device = _Device(hxdevice)

        return new_device

    def __get_device_index(self, device_info):
        device_index = 0
        # incase user want to create device from a sliced device_info list
        # self.__device_infos has the latest sort of device_info; so its
        # indexing can be trusted
        for index, __device_info in enumerate(self.__device_infos):
            if device_info == __device_info:
                device_index = index
                break
        return device_index

    # destroy_device ------------------------------------------------------

    def destroy_device(self, device=None):
        '''
        destroys and cleans up the internal memory of a ``Device``\
        instance(s). Devices that have been created \
        ``system.create_device()`` must be destroyed. if not called,\
        the system will called it when the module unloads.\n

        **Args**:
            device: can be\n
                - list of ``arena_api._device.Device`` instances\
                obtained from ``system.create_device()``. \
                Also, it can be a sliced list from the full list\
                returned from ``system.create_device()``.\n
                - an ``arena_api._device.Device`` instance is\
                acceptable in case the user wants to destroy one device.\n
                - ``None``. This is the default value. The system\
                destroys all of the created devices. Any device\
                reference can not be used after calling this function\n
        **Raises**:
            - ``ValueError`` :
                - device is an empty list.
                - a device is not found in the internal connected devices\
                internal list.\n
                - this function is called with a device instance\
                but the internal connected devices list is empty.\n
                - the device internal C pointer has changed from python.\n
            - ``TypeError`` :
                - device type is not a list of\
                ``arena_api._device.Device``, an \
                ``arena_api._device.Device`` instance, nor None.\n
        **Returns**:
            - None\n
        When called, it deletes all internal memory associated with a\
        a device: if a stream has been left open, it is closed; all \
        node maps and chunk data adapters are deallocated; \
        events are unregistered and the message channel closed;\
        finally, the control channel socket is closed, allowing \
        the device to be opened in read-write mode again.\n

        Destroying a device does not reset device settings, and will\
        not return a camera to a stable state. To reset settings or \
        return to a stable state, power-cycle a device \
        (unplug and plug back in) or reset it using ``DeviceReset`` node.\n

        :warning:
        - Devices must be destroyed
        - Does not affect device settings

        **------------------------------------------------------------------**\
        **-------------------------------------------------------------------**
    '''

        devices_as_list = None

        # Handel diffrent types -------------------------------------------

        # None
        if device is None:
            devices_as_list = self.__created_devices.values()

        # single device
        elif isinstance(device, _Device):
            # make it in a list
            devices_as_list = [device]

        # list
        elif isinstance(device, list):
            if len(device) == 0:
                raise ValueError('input can not be an empty list')
            devices_as_list = device

        # other types
        else:
            raise TypeError(f'Expected list of devices, device or None '
                            f'instead of {type(device).__name__}')

        # destroy devices in list -----------------------------------------

        updated_connected_devices = self.__created_devices.copy()
        for device in devices_as_list:

            self.__validate_device_before_destroy_device(device)

            mac_to_remove = None
            for mac in updated_connected_devices.keys():
                if device == updated_connected_devices[mac]:
                    mac_to_remove = mac
                    break

            if mac_to_remove is None:
                raise ValueError('Internal error : device is not found in '
                                 'connected devices')

            self.__xsystem.xSystemDestroyDevice(device._xdev.hxdevice.value)
            del updated_connected_devices[mac_to_remove]

        self.__created_devices = updated_connected_devices

    def __validate_device_before_destroy_device(self, device):

        # no device_info has been broadcasted
        if self.__created_devices == {}:
            raise ValueError(f'Invalid device')

        # list has an element that is not a device
        if not isinstance(device, _Device):
            raise TypeError(f'Expected list of devices instead of list '
                            f'with an element of type {type(device).__name__}')

        available_devices = []
        for device in self.__created_devices.values():
            available_devices.append(device)  # might want to compare hxdevice

        # unknown device
        if device not in available_devices:
            raise ValueError(f'Invalid device')

    # force_ip ----------------------------------------------------------------

    def force_ip(self, device_info):
        '''
        Forces the device that matches the mac address to a temporary new
        ip address, subnet mask and default gateway.
        The function will send a ForceIP command out on all the
        interfaces. This call also updates the internal list of interfaces
        in case that has not been done yet. The ForceIP command will be a
        network wide broadcast ``255.255.255.255`` and will request
        an acknowledgment to be broadcast back to the host. The information
        needed to force the new ip are : mac of the device, ip, subnet mask, 
        and default gateway.

        **Args**:
            device_infos : can be\n
            - ``dict`` that has the following keys: ``mac``,\
            ``ip``, ``subnetmask``, ``defaultgateway``.
                ---------------------------------------------------------------
                **mac**: a string value that represents MAC address of the\
                device to change  the ip for.\n
                ---------------------------------------------------------------
                **ip**: a string value that represets the new IP address in
                dot-decimal notation.\n
                ---------------------------------------------------------------
                **subnetmask**: a string value that represets the new
                Subnet Mask in dot-decimal notation.\n
                ---------------------------------------------------------------
                **defaultgateway**: a string value that represets the new
                Default Gateway in dot-decimal notation.\n
                ---------------------------------------------------------------
            - ``list`` of the formentioned dicts.
        **------------------------------------------------------------------**\
        **-------------------------------------------------------------------**
        '''
        # single device
        if isinstance(device_info, dict):
            self.__force_ip(device_info)
        # multi devices
        elif isinstance(device_info, list):
            for dev_inf in device_info:
                self.__force_ip(dev_inf)

    def __force_ip(self, device_info):
        # mac
        mac = device_info['mac']
        trans = str.maketrans('', '', ":.- ")
        mac_translated = mac.translate(trans)
        mac_int = int(mac_translated, 16)
        # ip
        ip_int = int(ip_address(device_info['ip']))
        # subnet and gateway
        subnetmask_int = int(ip_address(device_info['subnetmask']))
        defaultgateway_int = int(ip_address(device_info['defaultgateway']))

        self.__xsystem.xSystemForceIpAddress(
            mac_int, ip_int, subnetmask_int, defaultgateway_int)

    # ---------------------------------------------------------------------

    def __get_tl_system_nodemap(self):
        hxnodemap = self.__xsystem.xSystemGetTLSystemNodeMap()
        return _Nodemap(hxnodemap)

    tl_system_nodemap = property(__get_tl_system_nodemap)
    '''
    Used to access system related node.\n

    :getter: Returns ``GenTL`` node map for the system\n
    :type: ``arean_api.nodemap.Nodemap`` instance.\n

    Nodes in this node map include nodes related to:\n
    - ``Arena SDK`` information\n
    - ``GenTL`` and GEV versioning information\n
    - the ability to update and select interfaces\n
    - interface discovery and IP configuration information\n

    -----------------------------------------------------------------------

    Retrieves this node map without doing anything to initialize, \
    manage, or maintain it. This node map is initialized when \
    ``arena_api`` package is imported and deinitialized when the the
    package is unloads. All available nodes can be viewed in
    ``ArenaView`` software or run ``py_nodemaps_exploration.py``.

    ``arena_api`` package provides access to five different node maps that\
    can be splitted into two groups:\n
        - Software:\n
            The following node maps describe and provide access\
            to information and settings through the software rather\
            than the device:\n
                - ``system.tl_system_nodemap``
                - ``system.tl_interface_nodemap``
                - ``device.tl_device_nodemap``
                - ``device.tl_stream_nodemap``
                - ``device.tl_interface_nodemap``
        - Device:\n
            The following node maps describe and provide access to\
            information and settings through the device:\n
                - ``device.nodemap``
    -----------------------------------------------------------------------

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''


# the main instance that would be instantiated as soon as from arena_api system is called
system = _System()
