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

import os
import sys
from ctypes import byref, create_string_buffer

from arena_api._xlayer.xarena.arenac import harenac
from arena_api._xlayer.xarena.arenac_defaults import \
    XARENA_STR_BUFFER_SIZE_DEFAULT
from arena_api._xlayer.xarena.arenac_types import (acDevice, acNodeMap,
                                                   acSystem, bool8_t, size_t,
                                                   uint32_t, uint64_t)


class _xSystem:

    def __init__(self, hxsystem):
        # TODO SFW-2546
        if not hxsystem:
            raise TypeError('system handle is None')
        self.__acsystem = acSystem(hxsystem)
        self.hxsystem = self.__acsystem.value

    def xSystemGetNumInterfaces(self):

        num = size_t(0)
        # AC_ERROR acSystemGetNumInterfaces(
        #   acSystem hSystem,
        #   size_t * pNumDevices)
        harenac.acSystemGetNumInterfaces(
            self.__acsystem,
            byref(num))

        return num.value

    def xSystemGetInterfaceIpAddress(self, index):

        index = size_t(index)
        ip = uint32_t(0)
        # AC_ERROR acSystemGetInterfaceIpAddress(
        #   acSystem hSystem,
        #   size_t index,
        #   uint32_t* pIpAddress)
        harenac.acSystemGetInterfaceIpAddress(
            self.__acsystem,
            index,
            byref(ip))

        return ip.value

    def xSystemGetInterfaceIpAddressStr(self, index):

        index = size_t(index)
        ip_str_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_DEFAULT)
        buf_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acSystemGetInterfaceIpAddressStr(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pIpAddressStr,
        #   size_t * pBufLen)
        harenac.acSystemGetInterfaceIpAddressStr(
            self.__acsystem,
            index,
            ip_str_p,
            byref(buf_len))

        return (ip_str_p.value).decode()  # check if it work with no brakets

    def xSystemGetInterfaceSubnetMask(self, index):

        index = size_t(index)
        subnet_mask = uint32_t(0)
        # AC_ERROR acSystemGetInterfaceSubnetMask(
        #   acSystem hSystem,
        #   size_t index,
        #   uint32_t* pSubnetMask)
        harenac.acSystemGetInterfaceSubnetMask(
            self.__acsystem,
            index,
            byref(subnet_mask))

        return subnet_mask.value

    def xSystemGetInterfaceSubnetMaskStr(self, index):

        index = size_t(index)
        subnet_mask_str_p = create_string_buffer(
            XARENA_STR_BUFFER_SIZE_DEFAULT)
        buf_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acSystemGetInterfaceSubnetMaskStr(
        #   acSystem hSystem,
        #   size_t index,
        #   char* pSubnetMaskStr,
        #   size_t* pBufLen)
        harenac.acSystemGetInterfaceSubnetMaskStr(
            self.__acsystem,
            index,
            subnet_mask_str_p,
            byref(buf_len))

        return (subnet_mask_str_p.value).decode()

    def xSystemGetInterfaceMacAddress(self, index):

        index = size_t(index)
        mac_address = uint64_t(0)
        # AC_ERROR acSystemGetInterfaceMacAddress(
        #   acSystem hSystem,
        #   size_t index,
        #   uint64_t * pMacAddress)
        harenac.acSystemGetInterfaceMacAddress(
            self.__acsystem,
            index,
            byref(mac_address))

        return mac_address.value

    def xSystemGetInterfaceMacAddressStr(self, index):

        index = size_t(index)
        mac_address_str_p = create_string_buffer(
            XARENA_STR_BUFFER_SIZE_DEFAULT)
        buf_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acSystemGetInterfaceMacAddressStr(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pMacAddress,
        #   size_t * pBufLen)
        harenac.acSystemGetInterfaceMacAddressStr(
            self.__acsystem,
            index,
            mac_address_str_p,
            byref(buf_len))

        return (mac_address_str_p.value).decode()

    #
    # Device ------------------------------------------------------------------
    #

    def xSystemUpdateDevices(self, timout_milisec):

        timout_milisec = uint64_t(timout_milisec)
        # AC_ERROR acSysteUpdateDevices(
        #   acSystem hSystem,
        #   uint64_t timeout)
        harenac.acSystemUpdateDevices(
            self.__acsystem,
            timout_milisec)

    def xSystemUpdateDevicesHasChanged(self, timout_milisec):

        timout_milisec = uint64_t(timout_milisec)
        has_changed = bool8_t(False)
        # AC_ERROR acSystemUpdateDevicesHasChanged(
        #   acSystem hSystem,
        #   uint64_t timeout,
        #   bool8_t* pHasChanged)
        harenac.acSystemUpdateDevicesHasChanged(
            self.__acsystem,
            timout_milisec,
            byref(has_changed))

        return has_changed.value

    def xSystemUpdateDevicesOnInterface(self, interface_index, timout_milisec):

        index = size_t(interface_index)
        timout_milisec = uint64_t(timout_milisec)
        has_changed = bool8_t(False)
        # AC_ERROR acSystemUpdateDevicesOnInterface(
        #   acSystem hSystem,
        #   size_t interfaceIndex,
        #   uint64_t timeout,
        #   bool8_t * pHasChanged)
        harenac.acSystemUpdateDevicesOnInterface(
            self.__acsystem,
            index,
            timout_milisec,
            byref(has_changed))

        return has_changed.value

    def xSystemGetNumDevices(self):

        num = size_t(0)

        # num = c_int(0)
        # AC_ERROR acSystemGetNumDevices(
        #   acSystem hSystem,
        #   size_t * pNumDevices)
        harenac.acSystemGetNumDevices(
            self.__acsystem,
            byref(num))

        return num.value

    def xSystemCreateDevice(self, index):

        index = size_t(index)
        hxdevice = acDevice(None)
        # AC_ERROR acSystemCreateDevice(
        #   acSystem hSystem,
        #   size_t index,
        #   acDevice * phDevice)
        harenac.acSystemCreateDevice(
            self.__acsystem,
            index,
            byref(hxdevice))

        return hxdevice.value

    def xSystemDestroyDevice(self, device_p):

        hxdevice = acDevice(device_p)
        # AC_ERROR acSystemDestroyDevice(
        #   acSystem hSystem,
        #   acDevice hDevice)
        harenac.acSystemDestroyDevice(
            self.__acsystem,
            hxdevice)

    def xSystemGetDeviceModel(self, index):

        index = size_t(index)
        device_model_str_p = create_string_buffer(
            XARENA_STR_BUFFER_SIZE_DEFAULT)
        buf_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acSystemGetDeviceModel(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pModelNameBuf,
        #   size_t * pBufLen)
        harenac.acSystemGetDeviceModel(
            self.__acsystem,
            index,
            device_model_str_p,
            byref(buf_len))

        return (device_model_str_p.value).decode()

    def xSystemGetDeviceVendor(self, index):

        index = size_t(index)
        device_vendor_str_p = create_string_buffer(
            XARENA_STR_BUFFER_SIZE_DEFAULT)
        buf_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acSystemGetDeviceVendor(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pVendorNameBuf,
        #   size_t * pBufLen)
        harenac.acSystemGetDeviceVendor(
            self.__acsystem,
            index,
            device_vendor_str_p,
            byref(buf_len))

        return (device_vendor_str_p.value).decode()

    def xSystemGetDeviceSerial(self, index):

        index = size_t(index)
        device_serial_str_p = create_string_buffer(
            XARENA_STR_BUFFER_SIZE_DEFAULT)
        buf_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acSystemGetDeviceSerial(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pSerialNumberBuf,
        #   size_t * pBufLen)
        harenac.acSystemGetDeviceSerial(
            self.__acsystem,
            index,
            device_serial_str_p,
            byref(buf_len))

        return (device_serial_str_p.value).decode()

    def xSystemGetDeviceIpAddress(self, index):

        index = size_t(index)
        ip = uint32_t(0)
        # AC_ERROR acSystemGetDeviceIpAddress(
        #   acSystem hSystem,
        #   size_t index,
        #   uint32_t * pIpAddress)
        harenac.acSystemGetDeviceIpAddress(
            self.__acsystem,
            index,
            byref(ip))

        return ip.value

    def xSystemGetDeviceIpAddressStr(self, index):

        index = size_t(index)
        ip_str_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_DEFAULT)
        buf_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acSystemGetDeviceIpAddressStr(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pIpAddressStr,
        #   size_t * pBufLen)
        harenac.acSystemGetDeviceIpAddressStr(
            self.__acsystem,
            index,
            ip_str_p,
            byref(buf_len))

        return (ip_str_p.value).decode()

    def xSystemGetDeviceSubnetMask(self, index):

        index = size_t(index)
        subnet_mask = uint32_t(0)
        # AC_ERROR acSystemGetDeviceSubnetMask(
        #   acSystem hSystem,
        #   size_t index,
        #   uint32_t* pSubnetMask)
        harenac.acSystemGetDeviceSubnetMask(
            self.__acsystem,
            index,
            byref(subnet_mask))

        return subnet_mask.value

    def xSystemGetDeviceSubnetMaskStr(self, index):

        index = size_t(index)
        subnet_mask_str_p = create_string_buffer(
            XARENA_STR_BUFFER_SIZE_DEFAULT)
        buf_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acSystemGetDeviceSubnetMaskStr(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pSubnetMaskStr,
        #   size_t * pBufLen)
        harenac.acSystemGetDeviceSubnetMaskStr(
            self.__acsystem,
            index,
            subnet_mask_str_p,
            byref(buf_len))

        return (subnet_mask_str_p.value).decode()

    def xSystemGetDeviceDefaultGateway(self, index):

        index = size_t(index)
        gateway = uint32_t(0)
        # AC_ERROR acSystemGetDeviceDefaultGateway(
        #   acSystem hSystem,
        #   size_t index,
        #   uint32_t * pDefaultGateway)
        harenac.acSystemGetDeviceDefaultGateway(
            self.__acsystem,
            index,
            byref(gateway))

        return gateway.value

    def xSystemGetDeviceDefaultGatewayStr(self, index):

        index = size_t(index)
        gateway_str_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_DEFAULT)
        buf_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acSystemGetDeviceDefaultGatewayStr(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pDefaultGatewayStr,
        #   size_t * pBufLen)
        harenac.acSystemGetDeviceDefaultGatewayStr(
            self.__acsystem,
            index,
            gateway_str_p,
            byref(buf_len))

        return (gateway_str_p.value).decode()

    def xSystemGetDeviceMacAddress(self, index):

        index = size_t(index)
        mac_address = uint64_t(0)
        # AC_ERROR acSystemGetDeviceMacAddress(
        #   acSystem hSystem,
        #   size_t index,
        #   uint64_t * pMacAddress)
        harenac.acSystemGetDeviceMacAddress(
            self.__acsystem,
            index,
            byref(mac_address))

        return mac_address.value

    def xSystemGetDeviceMacAddressStr(self, index):

        index = size_t(index)
        mac_address_str_p = create_string_buffer(
            XARENA_STR_BUFFER_SIZE_DEFAULT)
        buf_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acSystemGetDeviceMacAddressStr(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pMacAddress,
        #   size_t * pBufLen)
        harenac.acSystemGetDeviceMacAddressStr(
            self.__acsystem,
            index,
            mac_address_str_p,
            byref(buf_len))

        return (mac_address_str_p.value).decode()

    def xSystemGetDeviceUserDefinedName(self, index):

        index = size_t(index)
        user_defined_name_p = create_string_buffer(
            XARENA_STR_BUFFER_SIZE_DEFAULT)
        buf_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acSystemGetDeviceUserDefinedName(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pUserDefinedName,
        #   size_t * pBufLen)
        harenac.acSystemGetDeviceUserDefinedName(
            self.__acsystem,
            index,
            user_defined_name_p,
            byref(buf_len))

        return (user_defined_name_p.value).decode()

    def xSystemForceIpAddress(self, mac, ip, subnetmask, defaultgateway):

        mac = uint64_t(mac)
        ip = uint64_t(ip)
        subnetmask = uint64_t(subnetmask)
        defaultgateway = uint64_t(defaultgateway)

        # AC_ERROR acSystemForceIpAddress(
        #   acSystem hSystem,
        #   uint64_t macAddress,
        #   uint64_t ipAddress,
        #   uint64_t subnetMask,
        #   uint64_t defaultGateway)
        harenac.acSystemForceIpAddress(
            self.__acsystem,
            mac,
            ip,
            subnetmask,
            defaultgateway)

    def xSystemGetDeviceVersion(self, index):

        index = size_t(index)
        user_defined_name_p = create_string_buffer(
            XARENA_STR_BUFFER_SIZE_DEFAULT)
        buf_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acSystemGetDeviceVersion
        #   (acSystem hSystem,
        #   size_t index,
        #   char * pDeviceVersion,
        #   size_t * pBufLen)
        harenac.acSystemGetDeviceVersion(
            self.__acsystem,
            index,
            user_defined_name_p,
            byref(buf_len))

        return (user_defined_name_p.value).decode()

    def xSystemIsDeviceDHCPConfigurationEnabled(self, index):

        index = size_t(index)
        dhcp_config_enabled = bool8_t(False)
        # AC_ERROR acSystemIsDeviceDHCPConfigurationEnabled
        #   (acSystem hSystem,
        #   size_t index,
        #   bool8_t * pIsDHCPConfigurationEnabled)
        harenac.acSystemIsDeviceDHCPConfigurationEnabled(
            self.__acsystem,
            index,
            byref(dhcp_config_enabled))

        return dhcp_config_enabled.value

    def xSystemIsDevicePersistentIpConfigurationEnabled(self, index):

        index = size_t(index)
        persistent_ip_config_enabled = bool8_t(False)
        # AC_ERROR acSystemIsDevicePersistentIpConfigurationEnabled(
        #   acSystem hSystem,
        #   size_t index,
        #   bool8_t * pIsPersistentIpConfigurationEnabled)
        harenac.acSystemIsDevicePersistentIpConfigurationEnabled(
            self.__acsystem,
            index,
            byref(persistent_ip_config_enabled))

        return persistent_ip_config_enabled.value

    def xSystemIsDeviceLLAConfigurationEnabled(self, index):

        index = size_t(index)
        lla_config_enabled = bool8_t(False)
        # AC_ERROR acSystemIsDeviceLLAConfigurationEnabled(
        #   acSystem hSystem,
        #   size_t index,
        #   bool8_t * pIsLLAIpConfigurationEnabled)
        harenac.acSystemIsDeviceLLAConfigurationEnabled(
            self.__acsystem,
            index,
            byref(lla_config_enabled))

        return lla_config_enabled.value

    def xSystemGetTLSystemNodeMap(self):

        xhnodemap = acNodeMap(None)
        # AC_ERROR acSystemGetTLSystemNodeMap(
        #   acSystem hSystem,
        #   acNodeMap * phNodeMap)
        harenac.acSystemGetTLSystemNodeMap(
            self.__acsystem,
            byref(xhnodemap))

        return xhnodemap.value
