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

from ctypes import POINTER, py_object
from enum import Enum, unique
from inspect import currentframe, getframeinfo

from arena_api._xlayer.binary.binary_function_return_value_checker import \
    BinaryFunctionReturnValueChecker
from arena_api._xlayer.xarena.arenac_types import (
    ac_access_mode, ac_bayer_algorithm, ac_caching_mode, ac_display_notation,
    ac_error, ac_inc_mode, ac_interface_type, ac_namespace, ac_payload_type,
    ac_pixel_endianness, ac_representation, ac_visibility, acBuffer,
    acCallback, acCallbackFunction, acChunkdata, acDevice, acFeatureStream,
    acImageCallbackFunction, acNode, acNodeMap, acSystem, bool8_t, char_ptr,
    double, int64_t, size_t, uint8_t, uint32_t, uint64_t)


@unique
class _ArenaCErr(Enum):
    SUCCESS = 0
    ERROR = -1001
    NOT_INITIALIZED = -1002
    NOT_IMPLEMENTED = -1003
    RESOURCE_IN_USE = -1004
    ACCESS_DENIED = -1005

    INVALID_HANDLE = -1006
    INVALID_ID = -1007
    NO_DATA = -1008
    INVALID_PARAMETER = -1009

    IO = -1010
    TIMEOUT = -1011
    ABORT = -1012
    INVALID_BUFFER = -1013
    NOT_AVAILABLE = -1014

    INVALID_ADDRESS = -1015
    BUFFER_TOO_SMALL = -1016
    INVALID_INDEX = -1017
    PARSING_CHUNK_DATA = -1018
    INVALID_VALUE = -1019
    RESOURCE_EXHAUSTED = -1020
    OUT_OF_MEMORY = -1021
    BUSY = -1022
    CUSTOM = -10000


_error_to_exception_dict = {
    # success
    _ArenaCErr.SUCCESS.value: None,
    # general
    _ArenaCErr.ERROR.value: Exception,
    _ArenaCErr.NOT_INITIALIZED.value: Exception,
    _ArenaCErr.RESOURCE_IN_USE.value: Exception,
    _ArenaCErr.BUSY.value: Exception,
    _ArenaCErr.CUSTOM.value: Exception,
    _ArenaCErr.INVALID_ID.value: Exception,
    _ArenaCErr.NO_DATA.value: Exception,
    _ArenaCErr.ABORT.value: Exception,
    _ArenaCErr.NOT_AVAILABLE.value: Exception,
    _ArenaCErr.INVALID_ADDRESS.value: Exception,
    _ArenaCErr.BUFFER_TOO_SMALL.value: Exception,
    _ArenaCErr.PARSING_CHUNK_DATA.value: Exception,
    _ArenaCErr.RESOURCE_EXHAUSTED.value: Exception,
    _ArenaCErr.ACCESS_DENIED.value: Exception,

    # type error
    _ArenaCErr.INVALID_HANDLE.value: TypeError,
    _ArenaCErr.INVALID_PARAMETER.value: TypeError,

    # different
    _ArenaCErr.NOT_IMPLEMENTED.value: NotImplementedError,
    _ArenaCErr.IO.value: IOError,
    _ArenaCErr.TIMEOUT.value: TimeoutError,
    _ArenaCErr.INVALID_BUFFER.value: BufferError,
    _ArenaCErr.INVALID_INDEX.value: IndexError,
    _ArenaCErr.INVALID_VALUE.value: ValueError,
    _ArenaCErr.OUT_OF_MEMORY.value: MemoryError,
}


def _get_msg_func(c_err):
    # cpp err msg
    # there is circular import
    # ( arenac.harenac -> arenac_configurator -> _xglobal -> arenac.harenac)
    # so arenac_configurator (this file) would break the circular import
    # if it did not import _xglobal. _xglobal need arenac.harenac for sure
    # so we can not take off this dependency. so we get a reference
    # to _xGlobal here
    from arena_api._xlayer.xarena._xglobal import _xGlobal
    cpp_error_msg = f'\t{_xGlobal.xGetLastErrorMessage()}'

    # c err msg
    c_err = _ArenaCErr(c_err)
    c_error_msg = f'\t{c_err.name} {c_err.value}'

    # together
    boarder = '\n' + '*' * 100 + '\n'
    full_msg = f'\n\nArena ERROR :\n{cpp_error_msg}\n\n' + \
        f'ArenaC ERROR :\n{c_error_msg}\n\n'
    return full_msg


class ArenaCConfigurator:

    def __init__(self, handle):
        global _error_to_exception_dict, _get_msg_func
        self.handle = handle

        ret_value_checker = BinaryFunctionReturnValueChecker(
            _error_to_exception_dict,
            _get_msg_func)

        self.raise_if_error = ret_value_checker.raise_if_error

    def configure(self):
        # - assign system c function returns types dynamically since they all
        #   return the same type of c_int
        # - These assignment are enforcement to make sure the right types of
        # argument are passed to the c functions
        self._configure_global()
        self._configure_system()
        self._configure_device()
        self._configure_buffer()
        self._configure_image()
        self._configure_chunkdata()
        self._configure_featurestream()
        self._configure_imagefactory()
        self._configure_nodemap()
        self._configure_callback()
        self._configure_node()
        self._configure_value()
        self._configure_integer()
        self._configure_boolean()
        self._configure_command()
        self._configure_float()
        self._configure_string()
        self._configure_register()
        self._configure_category()
        self._configure_enumeration()
        self._configure_enumentry()
        self._configure_selector()

        # self._raiseifnotconfigured()

    def _configure_global(self):
        c_funcs_list = [
            self.handle.acOpenSystem,
            self.handle.acCloseSystem,
            self.handle.acGetBitsPerPixel,
            self.handle.acCalculateCRC32,
            self.handle.acIsReadable,
            self.handle.acIsWritable,
            self.handle.acCalculateMaximumNumberOfBuffers
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acOpenSystem(
        #   acSystem* phSystem)
        self.handle.acOpenSystem.argtypes = [
            POINTER(acSystem)]

        # AC_ERROR acCloseSystem(
        #   acSystem phSystem)
        self.handle.acCloseSystem.argtypes = [
            acSystem]

        # AC_ERROR acGetBitsPerPixel(
        #   uint64_t pixelFormat,
        #   size_t* pBitsPerPixel)
        self.handle.acGetBitsPerPixel.argtypes = [
            uint64_t,
            POINTER(size_t)]

        # AC_ERROR acCalculateCRC32(
        #   uint8_t* pData,
        #   size_t pDataLen,
        #   size_t* pCRCValue)
        self.handle.acCalculateCRC32.argtypes = [
            POINTER(uint8_t),
            size_t,
            POINTER(size_t)]

        # AC_ERROR acIsReadable(
        #   acNode hNode,
        #   bool8_t* pIsReadable)
        self.handle.acIsReadable.argtypes = [
            acNode,
            POINTER(bool8_t)]

        # AC_ERROR acIsWritable(
        #   acNode hNode,
        #   bool8_t* pIsWritable)
        self.handle.acIsWritable.argtypes = [
            acNode,
            POINTER(bool8_t)]

        # AC_ERROR acCalculateMaximumNumberOfBuffers(
        #   size_t payloadSize,
        #   size_t* pMaxBufs)
        self.handle.acCalculateMaximumNumberOfBuffers.argtypes = [
            size_t,
            POINTER(size_t)]

    def _configure_system(self):

        c_funcs_list = [
            self.handle.acSystemGetNumInterfaces,
            self.handle.acSystemGetInterfaceIpAddress,
            self.handle.acSystemGetInterfaceIpAddressStr,
            self.handle.acSystemGetInterfaceSubnetMask,
            self.handle.acSystemGetInterfaceSubnetMaskStr,
            self.handle.acSystemGetInterfaceMacAddress,
            self.handle.acSystemGetInterfaceMacAddressStr,
            self.handle.acSystemUpdateDevices,
            self.handle.acSystemUpdateDevicesHasChanged,
            self.handle.acSystemUpdateDevicesOnInterface,
            self.handle.acSystemGetNumDevices,
            self.handle.acSystemGetDeviceModel,
            self.handle.acSystemGetDeviceVendor,
            self.handle.acSystemGetDeviceSerial,
            self.handle.acSystemGetDeviceIpAddress,
            self.handle.acSystemGetDeviceIpAddressStr,
            self.handle.acSystemGetDeviceSubnetMask,
            self.handle.acSystemGetDeviceSubnetMaskStr,
            self.handle.acSystemGetDeviceDefaultGateway,
            self.handle.acSystemGetDeviceDefaultGatewayStr,
            self.handle.acSystemGetDeviceMacAddress,
            self.handle.acSystemGetDeviceMacAddressStr,
            self.handle.acSystemGetDeviceUserDefinedName,
            self.handle.acSystemForceIpAddress,
            self.handle.acSystemIsDeviceDHCPConfigurationEnabled,
            self.handle.acSystemIsDevicePersistentIpConfigurationEnabled,
            self.handle.acSystemGetDeviceVersion,
            self.handle.acSystemIsDeviceLLAConfigurationEnabled,
            self.handle.acSystemCreateDevice,
            self.handle.acSystemDestroyDevice,
            self.handle.acSystemGetTLSystemNodeMap
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acSystemGetNumInterfaces(
        #   acSystem hSystem,
        #   size_t * pNumDevices)

        self.handle.acSystemGetNumInterfaces.argtypes = [
            acSystem,
            POINTER(size_t)]

        # acSystemGetInterfaceIpAddress(
        #   acSystem hSystem,
        #   size_t index,
        #   uint32_t * pIpAddress)
        self.handle.acSystemGetInterfaceIpAddress.argtypes = [
            acSystem,
            size_t,
            POINTER(uint32_t)]

        # AC_ERROR acSystemGetInterfaceIpAddressStr(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pIpAddressStr,
        #   size_t * pBufLen)

        self.handle.acSystemGetInterfaceIpAddressStr.argtypes = [
            acSystem,
            size_t,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acSystemGetInterfaceSubnetMask(
        #   acSystem hSystem,
        #   size_t index,
        #   uint32_t * pSubnetMask)
        self.handle.acSystemGetInterfaceSubnetMask.argtypes = [
            acSystem,
            size_t,
            POINTER(uint32_t)]

        # AC_ERROR acSystemGetInterfaceSubnetMaskStr(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pSubnetMaskStr,
        #   size_t * pBufLen)
        self.handle.acSystemGetInterfaceSubnetMaskStr.argtypes = [
            acSystem,
            size_t,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acSystemGetInterfaceMacAddress(
        #   acSystem hSystem,
        #   size_t index,
        #   uint64_t * pMacAddress)
        self.handle.acSystemGetInterfaceMacAddress.argtypes = [
            acSystem,
            size_t,
            POINTER(uint64_t)]

        # AC_ERROR acSystemGetInterfaceMacAddressStr(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pMacAddress,
        #   size_t * pBufLen)
        self.handle.acSystemGetInterfaceMacAddressStr.argtypes = [
            acSystem,
            size_t,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acSystemUpdateDevices(
        #   acSystem hSystem,
        #   uint64_t timeout)
        self.handle.acSystemUpdateDevices.argtypes = [
            acSystem,
            uint64_t]

        # AC_ERROR acSystemUpdateDevicesHasChanged(
        #   acSystem hSystem,
        #   uint64_t timeout,
        #   bool8_t * pHasChanged)
        self.handle.acSystemUpdateDevicesHasChanged.argtypes = [
            acSystem,
            uint64_t,
            POINTER(bool8_t)]

        # AC_ERROR acSystemUpdateDevicesOnInterface(
        #   acSystem hSystem,
        #   size_t interfaceIndex,
        #   uint64_t timeout,
        #   bool8_t * pHasChanged)
        self.handle.acSystemUpdateDevicesOnInterface.argtypes = [
            acSystem,
            size_t,
            uint64_t,
            POINTER(bool8_t)]

        # AC_ERROR acSystemGetNumDevices(
        #   acSystem hSystem,
        #   size_t * pNumDevices)
        self.handle.acSystemGetNumDevices.argtypes = [
            acSystem,
            POINTER(size_t)]

        # AC_ERROR acSystemGetDeviceModel(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pModelNameBuf,
        #   size_t * pBufLen)
        self.handle.acSystemGetDeviceModel.argtypes = [
            acSystem,
            size_t,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acSystemGetDeviceVendor(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pVendorNameBuf,
        #   size_t * pBufLen)
        self.handle.acSystemGetDeviceVendor.argtypes = [
            acSystem,
            size_t,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acSystemGetDeviceSerial(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pSerialNumberBuf,
        #   size_t * pBufLen)
        self.handle.acSystemGetDeviceSerial.argtypes = [
            acSystem,
            size_t,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acSystemGetDeviceIpAddress(
        #   acSystem hSystem,
        #   size_t index,
        #   uint32_t * pIpAddress)
        self.handle.acSystemGetDeviceIpAddress.argtypes = [
            acSystem,
            size_t,
            POINTER(uint32_t)]

        # AC_ERROR acSystemGetDeviceIpAddressStr(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pIpAddressStr,
        #   size_t * pBufLen)
        self.handle.acSystemGetDeviceIpAddressStr.argtypes = [
            acSystem,
            size_t,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acSystemGetDeviceSubnetMask(
        #   acSystem hSystem,
        #   size_t index,
        #   uint32_t * pSubnetMask)
        self.handle.acSystemGetDeviceSubnetMask.argtypes = [
            acSystem,
            size_t,
            POINTER(uint32_t)]

        # AC_ERROR acSystemGetDeviceSubnetMaskStr(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pSubnetMaskStr,
        #   size_t * pBufLen)
        self.handle.acSystemGetDeviceSubnetMaskStr.argtypes = [
            acSystem,
            size_t,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acSystemGetDeviceDefaultGateway(
        #   acSystem hSystem,
        #   size_t index,
        #   uint32_t * pDefaultGateway)
        self.handle.acSystemGetDeviceDefaultGateway.argtypes = [
            acSystem,
            size_t,
            POINTER(uint32_t)]

        # AC_ERROR acSystemGetDeviceDefaultGatewayStr(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pDefaultGatewayStr,
        #   size_t * pBufLen)
        self.handle.acSystemGetDeviceDefaultGatewayStr.argtypes = [
            acSystem,
            size_t,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acSystemGetDeviceMacAddress(
        #   acSystem hSystem,
        #   size_t index,
        #   uint64_t * pMacAddress)
        self.handle.acSystemGetDeviceMacAddress.argtypes = [
            acSystem,
            size_t,
            POINTER(uint64_t)]

        # AC_ERROR acSystemGetDeviceMacAddressStr(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pMacAddress,
        #   size_t * pBufLen)
        self.handle.acSystemGetDeviceMacAddressStr.argtypes = [
            acSystem,
            size_t,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acSystemGetDeviceUserDefinedName(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pUserDefinedName,
        #   size_t * pBufLen)
        self.handle.acSystemGetDeviceUserDefinedName.argtypes = [
            acSystem,
            size_t,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acSystemForceIpAddress(
        #   acSystem hSystem,
        #   uint64_t macAddress,
        #   uint64_t ipAddress,
        #   uint64_t subnetMask,
        #   uint64_t defaultGateway)
        self.handle.acSystemForceIpAddress.argtypes = [
            acSystem,
            uint64_t,
            uint64_t,
            uint64_t,
            uint64_t
        ]

        # AC_ERROR acSystemIsDeviceDHCPConfigurationEnabled(
        #   acSystem hSystem,
        #   size_t index,
        #   bool8_t * pIsDHCPConfigurationEnabled)
        self.handle.acSystemIsDeviceDHCPConfigurationEnabled.argtypes = [
            acSystem,
            size_t,
            POINTER(bool8_t)]

        # AC_ERROR acSystemIsDevicePersistentIpConfigurationEnabled(
        #   acSystem hSystem,
        #   size_t index,
        #   bool8_t * pIsPersistentIpConfigurationEnabled)
        self.handle.acSystemIsDevicePersistentIpConfigurationEnabled.argtypes = [
            acSystem,
            size_t,
            POINTER(bool8_t)]

        # AC_ERROR acSystemGetDeviceVersion(
        #   acSystem hSystem,
        #   size_t index,
        #   char * pDeviceVersion,
        #   size_t * pBufLen)
        self.handle.acSystemGetDeviceVersion.argtypes = [
            acSystem,
            size_t,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acSystemIsDeviceLLAConfigurationEnabled(
        #   acSystem hSystem,
        #   size_t index,
        #   bool8_t * pIsLLAIpConfigurationEnabled)
        self.handle.acSystemIsDeviceLLAConfigurationEnabled.argtypes = [
            acSystem,
            size_t,
            POINTER(bool8_t)]

        # AC_ERROR acSystemCreateDevice(
        #   acSystem hSystem,
        #   size_t index,
        #   acDevice * phDevice)
        self.handle.acSystemCreateDevice.argtypes = [
            acSystem,
            size_t,
            POINTER(acSystem)]

        # AC_ERROR acSystemDestroyDevice(
        #   acSystem hSystem,
        #   acDevice hDevice)
        self.handle.acSystemDestroyDevice.argtypes = [
            acSystem,
            acDevice]

        # AC_ERROR acSystemGetTLSystemNodeMap(
        #   acSystem hSystem,
        #   acNodeMap * phNodeMap)
        self.handle.acSystemGetTLSystemNodeMap.argtypes = [
            acSystem,
            POINTER(acNodeMap)]

    def _configure_device(self):

        c_funcs_list = [
            self.handle.acDeviceStartStream,
            self.handle.acDeviceStartStreamNumBuffersAndFlags,
            self.handle.acDeviceStopStream,
            self.handle.acDeviceGetBuffer,
            self.handle.acDeviceRequeueBuffer,
            self.handle.acDeviceInitializeEvents,
            self.handle.acDeviceDeinitializeEvents,
            self.handle.acDeviceWaitOnEvent,
            self.handle.acDeviceGetNodeMap,
            self.handle.acDeviceGetTLDeviceNodeMap,
            self.handle.acDeviceGetTLStreamNodeMap,
            self.handle.acDeviceGetTLInterfaceNodeMap,
            self.handle.acDeviceRegisterImageCallback,
            self.handle.acDeviceDeregisterImageCallback,
        ]

        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR  acDeviceStartStream(
        #   acDevice hDevice);
        self.handle.acDeviceStartStream.argtypes = [
            acDevice]

        # AC_ERROR acDeviceStartStreamNumBuffersAndFlags(
        #   acDevice hDevice,
        #   size_t numBuffers);
        self.handle.acDeviceStartStreamNumBuffersAndFlags.argtypes = [
            acDevice,
            size_t]

        # AC_ERROR acDeviceStopStream(
        #   acDevice hDevice);
        self.handle.acDeviceStopStream.argtypes = [
            acDevice]

        # AC_ERROR acDeviceGetBuffer(
        #   acDevice hDevice,
        #   uint64_t timeout,
        #   acBuffer * phBuffer)
        self.handle.acDeviceGetBuffer.argtypes = [
            acDevice,
            uint64_t,
            POINTER(acBuffer)]

        # AC_ERROR acDeviceRequeueBuffer(
        #   acDevice hDevice,
        #   acBuffer pBuffer)
        self.handle.acDeviceRequeueBuffer.argtypes = [
            acDevice,
            acBuffer]

        # AC_ERROR acDeviceInitializeEvents(
        #   acDevice hDevice);
        self.handle.acDeviceInitializeEvents.argtypes = [
            acDevice]

        # AC_ERROR acDeviceDeinitializeEvents(
        #   acDevice hDevice);
        self.handle.acDeviceDeinitializeEvents.argtypes = [
            acDevice]

        # AC_ERROR acDeviceWaitOnEvent(
        #   acDevice hDevice,
        #   int64_t timeout)
        self.handle.acDeviceWaitOnEvent.argtypes = [
            acDevice,
            int64_t]

        # AC_ERROR acDeviceGetNodeMap(
        #   acDevice hDevice,
        #   acNodeMap * phNodeMap)
        self.handle.acDeviceGetNodeMap.argtypes = [
            acDevice,
            POINTER(acNodeMap)]

        # AC_ERROR acDeviceGetTLDeviceNodeMap(
        #   acDevice hDevice,
        #   acNodeMap * phNodeMap)
        self.handle.acDeviceGetTLDeviceNodeMap.argtypes = [
            acDevice,
            POINTER(acNodeMap)]

        # AC_ERROR acDeviceGetTLStreamNodeMap(
        #   acDevice hDevice,
        #   acNodeMap * phNodeMap)
        self.handle.acDeviceGetTLStreamNodeMap.argtypes = [
            acDevice,
            POINTER(acNodeMap)]

        # AC_ERROR acDeviceGetTLInterfaceNodeMap(
        #   acDevice hDevice,
        #   acNodeMap * phNodeMap)
        self.handle.acDeviceGetTLInterfaceNodeMap.argtypes = [
            acDevice,
            POINTER(acNodeMap)]

        # AC_ERROR acDeviceRegisterImageCallback(
        #   acDevice hDevice,
        #   acCallback* phCallback,
        #   acImageCallbackFunction callbackFn,
        #   void* pUserData)
        self.handle.acDeviceRegisterImageCallback.argtypes = [
            acDevice,
            POINTER(acCallback),
            acImageCallbackFunction,
            # ArenaC API takes void* but we pass a py_object to
            # receive it in the callback.
            py_object]

        # AC_ERROR acDeviceDeregisterImageCallback(
        #   acDevice hDevice,
        #   acCallback* phCallback)
        self.handle.acDeviceDeregisterImageCallback.argtypes = [
            acDevice,
            POINTER(acCallback)]

    def _configure_buffer(self):

        c_funcs_list = [
            self.handle.acBufferGetSizeFilled,
            self.handle.acBufferGetPayloadSize,
            self.handle.acBufferGetSizeOfBuffer,
            self.handle.acBufferGetFrameId,
            self.handle.acBufferGetPayloadType,
            self.handle.acBufferHasChunkData,
            self.handle.acBufferHasImageData,
            self.handle.acBufferIsIncomplete,
            self.handle.acBufferDataLargerThanBuffer,
            self.handle.acBufferVerifyCRC
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acBufferGetSizeFilled(
        #   acBuffer hBuffer,
        #   size_t * pSizeFilled)
        self.handle.acBufferGetSizeFilled.argtypes = [
            acBuffer,
            POINTER(size_t)]

        # AC_ERROR acBufferGetPayloadSize(
        #   acBuffer hBuffer,
        #   size_t * pPayloadSize)
        self.handle.acBufferGetPayloadSize.argtypes = [
            acBuffer,
            POINTER(size_t)]

        # AC_ERROR acBufferGetSizeOfBuffer(
        #   acBuffer hBuffer,
        #   size_t * pSizeOfBuffer)
        self.handle.acBufferGetSizeOfBuffer.argtypes = [
            acBuffer,
            POINTER(size_t)]

        # AC_ERROR acBufferGetFrameId(
        #   acBuffer hBuffer,
        #   uint64_t * pFrameId)
        self.handle.acBufferGetFrameId.argtypes = [
            acBuffer,
            POINTER(uint64_t)]

        # AC_ERROR acBufferGetPayloadType(
        #   acBuffer hBuffer,
        #   AC_PAYLOAD_TYPE * pPayloadType)
        self.handle.acBufferGetPayloadType.argtypes = [
            acBuffer,
            POINTER(ac_payload_type)]

        # AC_ERROR acBufferHasChunkData(
        #   acBuffer hBuffer,
        #   bool8_t * pHasChunkData)
        self.handle.acBufferHasChunkData.argtypes = [
            acBuffer,
            POINTER(bool8_t)]

        # AC_ERROR acBufferHasImageData(
        #   acBuffer hBuffer,
        #   bool8_t * pHasImageData)
        self.handle.acBufferHasImageData.argtypes = [
            acBuffer,
            POINTER(bool8_t)]

        # AC_ERROR acBufferIsIncomplete(
        #   acBuffer hBuffer,
        #   bool8_t * pIsIncomplete)
        self.handle.acBufferIsIncomplete.argtypes = [
            acBuffer,
            POINTER(bool8_t)]

        # AC_ERROR acBufferDataLargerThanBuffer(
        #   acBuffer hBuffer,
        #   bool8_t * pDataLargerThanBuffer)
        self.handle.acBufferDataLargerThanBuffer.argtypes = [
            acBuffer,
            POINTER(bool8_t)]

        # AC_ERROR acBufferVerifyCRC(
        #   acBuffer hBuffer,
        #   bool8_t * pVerifyCRC)
        self.handle.acBufferVerifyCRC.argtypes = [
            acBuffer,
            POINTER(bool8_t)]

    def _configure_image(self):

        c_funcs_list = [
            self.handle.acImageGetWidth,
            self.handle.acImageGetHeight,
            self.handle.acImageGetOffsetX,
            self.handle.acImageGetOffsetY,
            self.handle.acImageGetPaddingX,
            self.handle.acImageGetPaddingY,
            self.handle.acImageGetPixelFormat,
            self.handle.acImageGetBitsPerPixel,
            self.handle.acImageGetPixelEndianness,
            self.handle.acImageGetTimestamp,
            self.handle.acImageGetTimestampNs,
            self.handle.acImageGetData
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acImageGetWidth(
        #   acBuffer hBuffer,
        #   size_t* pWidth)
        self.handle.acImageGetWidth.argtypes = [
            acBuffer,
            POINTER(size_t)]

        # AC_ERROR acImageGetHeight(
        #   acBuffer hBuffer,
        #   size_t* pHeight)
        self.handle.acImageGetHeight.argtypes = [
            acBuffer,
            POINTER(size_t)]

        # AC_ERROR acImageGetOffsetX(
        #   acBuffer hBuffer,
        #   size_t* pOffsetX)
        self.handle.acImageGetOffsetX.argtypes = [
            acBuffer,
            POINTER(size_t)]

        # AC_ERROR acImageGetOffsetY(
        #   acBuffer hBuffer,
        #   size_t* pOffsetY)
        self.handle.acImageGetOffsetY.argtypes = [
            acBuffer,
            POINTER(size_t)]

        # AC_ERROR acImageGetPaddingX(
        #   acBuffer hBuffer,
        #   size_t* pPaddingX)
        self.handle.acImageGetPaddingX.argtypes = [
            acBuffer,
            POINTER(size_t)]

        # AC_ERROR acImageGetPaddingY(
        #   acBuffer hBuffer,
        #   size_t* pPaddingY)
        self.handle.acImageGetPaddingY.argtypes = [
            acBuffer,
            POINTER(size_t)]

        # AC_ERROR acImageGetPixelFormat(
        #   acBuffer hBuffer,
        #   uint64_t* pPixelFormat)
        self.handle.acImageGetPixelFormat.argtypes = [
            acBuffer,
            POINTER(uint64_t)]

        # AC_ERROR acImageGetBitsPerPixel(
        #   acBuffer hBuffer,
        #   size_t* pBitsPerPixel)
        self.handle.acImageGetBitsPerPixel.argtypes = [
            acBuffer,
            POINTER(size_t)]

        # AC_ERROR acImageGetPixelEndianness(
        #   acBuffer hBuffer,
        #   AC_PIXEL_ENDIANNESS* pPixelEndianness)
        self.handle.acImageGetPixelEndianness.argtypes = [
            acBuffer,
            POINTER(ac_pixel_endianness)]

        # AC_ERROR acImageGetTimestamp(
        #   acBuffer hBuffer,
        #   uint64_t* pTimestamp)
        self.handle.acImageGetTimestamp.argtypes = [
            acBuffer,
            POINTER(uint64_t)]

        # AC_ERROR acImageGetTimestampNs(
        #   acBuffer hBuffer,
        #   uint64_t* pTimestampNs)
        self.handle.acImageGetTimestampNs.argtypes = [
            acBuffer,
            POINTER(uint64_t)]

        # AC_ERROR acImageGetData(
        #   acBuffer hBuffer,
        #   uint8_t** ppData)
        self.handle.acImageGetData.argtypes = [
            acBuffer,
            POINTER(POINTER(uint8_t))]

    def _configure_chunkdata(self):

        c_funcs_list = [
            self.handle.acChunkDataGetChunk,
            self.handle.acChunkDataGetChunkAndAccessMode
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acChunkDataGetChunk(
        #   acBuffer hBuffer,
        #   const char* pName,
        #   acNode* phChunkNode)
        self.handle.acChunkDataGetChunk.argtypes = [
            acChunkdata,
            char_ptr,
            POINTER(acNode)
        ]

        # AC_ERROR acChunkDataGetChunkAndAccessMode(
        #   acBuffer hBuffer,
        #   char* pName,
        #   acNode* phChunkNode,
        #   AC_ACCESS_MODE* pAccessMode)
        self.handle.acChunkDataGetChunkAndAccessMode.argtypes = [
            acBuffer,
            char_ptr,
            POINTER(acNode),
            POINTER(ac_access_mode)
        ]

    def _configure_featurestream(self):

        c_funcs_list = [
            self.handle.acFeatureStreamCreate,
            self.handle.acFeatureStreamDestroy,
            self.handle.acFeatureStreamSelect,
            self.handle.acFeatureStreamWrite,
            self.handle.acFeatureStreamWriteFileName,
            self.handle.acFeatureStreamRead,
            self.handle.acFeatureStreamReadFileName
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acFeatureStreamCreate(
        #   acNodeMap hNodeMap,
        #   acFeatureStream* phFeatureStream)
        self.handle.acFeatureStreamCreate.argtypes = [
            acNodeMap,
            POINTER(acFeatureStream)]

        # AC_ERROR acFeatureStreamDestroy(
        #   acFeatureStream hFeatureStream)
        self.handle.acFeatureStreamDestroy.argtypes = [
            acFeatureStream]

        # AC_ERROR acFeatureStreamSelect(
        #   acFeatureStream hFeatureStream,
        #   char* pFeatureName)
        self.handle.acFeatureStreamSelect.argtypes = [
            acFeatureStream,
            char_ptr]

        # AC_ERROR acFeatureStreamWrite(
        #   acFeatureStream hFeatureStream)
        self.handle.acFeatureStreamWrite.argtypes = [
            acFeatureStream]

        # AC_ERROR acFeatureStreamWriteFileName(
        #   acFeatureStream hFeatureStream,
        #   char* pFileName)
        self.handle.acFeatureStreamWriteFileName.argtypes = [
            acFeatureStream,
            char_ptr]

        # AC_ERROR acFeatureStreamRead(
        #   acFeatureStream hFeatureStream)
        self.handle.acFeatureStreamRead.argtypes = [
            acFeatureStream]

        # AC_ERROR acFeatureStreamReadFileName(
        #   acFeatureStream hFeatureStream,
        #   char* pFileName)
        self.handle.acFeatureStreamReadFileName.argtypes = [
            acFeatureStream,
            char_ptr]

    def _configure_imagefactory(self):

        c_funcs_list = [
            self.handle.acImageFactoryCreate,
            self.handle.acImageFactoryCopy,
            self.handle.acImageFactoryDestroy,
            self.handle.acImageFactoryConvert,
            self.handle.acImageFactoryConvertBayerAlgorithm
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acImageFactoryCreate(
        #   uint8_t* pData,
        #   size_t dataSize,
        #   size_t width,
        #   size_t height,
        #   uint64_t pixelFormat,
        #   acBuffer* phDst)
        self.handle.acImageFactoryCreate.argtypes = [
            POINTER(uint8_t),
            size_t,
            size_t,
            size_t,
            uint64_t,
            POINTER(acBuffer)]

        # AC_ERROR acImageFactoryCopy(
        #   acBuffer hSrc,
        #   acBuffer* phDst)
        self.handle.acImageFactoryCopy.argtypes = [
            acBuffer,
            POINTER(acBuffer)]

        # AC_ERROR acImageFactoryDestroy(
        #   acBuffer hBuffer)
        self.handle.acImageFactoryDestroy.argtypes = [
            acBuffer]

        # AC_ERROR acImageFactoryConvert(
        #   acBuffer hSrc,
        #   uint64_t pixelFormat,
        #   acBuffer* phDst)
        self.handle.acImageFactoryConvert.argtypes = [
            acBuffer,
            uint64_t,
            POINTER(acBuffer)]

        # AC_ERROR acImageFactoryConvertBayerAlgorithm(
        #   acBuffer hSrc,
        #   uint64_t pixelFormat,
        #   AC_BAYER_ALGORITHM bayerAlgo,
        #   acBuffer* phDst)
        self.handle.acImageFactoryConvertBayerAlgorithm.argtypes = [
            acBuffer,
            uint64_t,
            ac_bayer_algorithm,
            POINTER(acBuffer)]

    def _configure_nodemap(self):

        c_funcs_list = [
            self.handle.acNodeMapGetNode,
            self.handle.acNodeMapGetNodeAndAccessMode,
            self.handle.acNodeMapInvalidateNodes,
            self.handle.acNodeMapGetDeviceName,
            self.handle.acNodeMapPoll,
            self.handle.acNodeMapLock,
            self.handle.acNodeMapUnlock,
            self.handle.acNodeMapTryLock,
            self.handle.acNodeMapGetNumNodes,
            self.handle.acNodeMapGetNodeByIndex,
            self.handle.acNodeMapGetNodeByIndexAndAccessMode,
            self.handle.acNodeMapGetStringValue,
            self.handle.acNodeMapGetIntegerValue,
            self.handle.acNodeMapGetFloatValue,
            self.handle.acNodeMapGetBooleanValue,
            self.handle.acNodeMapGetEnumerationValue,
            self.handle.acNodeMapSetStringValue,
            self.handle.acNodeMapSetIntegerValue,
            self.handle.acNodeMapSetFloatValue,
            self.handle.acNodeMapSetBooleanValue,
            self.handle.acNodeMapSetEnumerationValue,
            self.handle.acNodeMapExecute
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acNodeMapGetNode(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   acNode* phNode)
        self.handle.acNodeMapGetNode.argtypes = [
            acNodeMap,
            char_ptr,
            POINTER(acNode)]

        # AC_ERROR acNodeMapGetNodeAndAccessMode(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   acNode* phNode,
        #   AC_ACCESS_MODE* pAccessMode)
        self.handle.acNodeMapGetNodeAndAccessMode.argtypes = [
            acNodeMap,
            char_ptr,
            POINTER(acNode),
            POINTER(ac_access_mode)]

        # AC_ERROR acNodeMapInvalidateNodes(
        #   acNodeMap hNodeMap)
        self.handle.acNodeMapInvalidateNodes.argtypes = [
            acNodeMap]

        # AC_ERROR acNodeMapGetDeviceName(
        #   acNodeMap hNodeMap,
        #   char* pDeviceNameBuf,
        #   size_t* pBufLen)
        self.handle.acNodeMapGetDeviceName.argtypes = [
            acNodeMap,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acNodeMapPoll(
        #   acNodeMap hNodeMap,
        #   int64_t elapsedTime)
        self.handle.acNodeMapPoll.argtypes = [
            acNodeMap,
            int64_t]

        # AC_ERROR acNodeMapLock(
        #   acNodeMap hNodeMap)
        self.handle.acNodeMapLock.argtypes = [
            acNodeMap]

        # AC_ERROR acNodeMapUnlock(
        #   acNodeMap hNodeMap)
        self.handle.acNodeMapUnlock.argtypes = [
            acNodeMap]

        # AC_ERROR acNodeMapTryLock(
        #   acNodeMap hNodeMap,
        #   bool8_t* pLocked)
        self.handle.acNodeMapTryLock.argtypes = [
            acNodeMap,
            POINTER(bool8_t)]

        # AC_ERROR acNodeMapGetNumNodes(
        #   acNodeMap hNodeMap,
        #   uint64_t* pNumNodes)
        self.handle.acNodeMapGetNumNodes.argtypes = [
            acNodeMap,
            POINTER(uint64_t)]

        # AC_ERROR acNodeMapGetNodeByIndex(
        #   acNodeMap hNodeMap,
        #   size_t index,
        #   acNode* phNode)
        self.handle.acNodeMapGetNodeByIndex.argtypes = [
            acNodeMap,
            size_t,
            POINTER(acNode)]

        # AC_ERROR acNodeMapGetNodeByIndexAndAccessMode(
        #   acNodeMap hNodeMap,
        #   size_t index,
        #   acNode* phNode,
        #   AC_ACCESS_MODE* pAccessMode)
        self.handle.acNodeMapGetNodeByIndexAndAccessMode.argtypes = [
            acNodeMap,
            size_t,
            POINTER(acNode),
            POINTER(ac_access_mode)]

        # AC_ERROR acNodeMapGetStringValue(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   char* pValueBuf,
        #   size_t* pBufLen)
        self.handle.acNodeMapGetStringValue.argtypes = [
            acNodeMap,
            char_ptr,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acNodeMapGetIntegerValue(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   int64_t* pValue)
        self.handle.acNodeMapGetIntegerValue.argtypes = [
            acNodeMap,
            char_ptr,
            POINTER(int64_t)]

        # AC_ERROR acNodeMapGetFloatValue(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   double* pValue)
        self.handle.acNodeMapGetFloatValue.argtypes = [
            acNodeMap,
            char_ptr,
            POINTER(double)]

        # AC_ERROR acNodeMapGetBooleanValue(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   bool8_t* pValue)
        self.handle.acNodeMapGetBooleanValue.argtypes = [
            acNodeMap,
            char_ptr,
            POINTER(bool8_t)]

        # AC_ERROR acNodeMapGetEnumerationValue(
        #   acNodeMap hNodeMap,
        #   char* pSymbolicBuf,
        #   size_t* pBufLen)
        self.handle.acNodeMapGetEnumerationValue.argtypes = [
            acNodeMap,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acNodeMapSetStringValue(
        #   acNodeMap hNodeMap,
        #   char* pValue)
        self.handle.acNodeMapSetStringValue.argtypes = [
            acNodeMap,
            char_ptr]

        # AC_ERROR acNodeMapSetIntegerValue(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   int64_t value)
        self.handle.acNodeMapSetIntegerValue.argtypes = [
            acNodeMap,
            char_ptr,
            int64_t]

        # AC_ERROR acNodeMapSetFloatValue(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   double value)
        self.handle.acNodeMapSetFloatValue.argtypes = [
            acNodeMap,
            char_ptr,
            double]

        # AC_ERROR acNodeMapSetBooleanValue(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   bool8_t value)
        self.handle.acNodeMapSetBooleanValue.argtypes = [
            acNodeMap,
            char_ptr,
            bool8_t]

        # AC_ERROR acNodeMapSetEnumerationValue(
        #   acNodeMap hNodeMap,
        #   char* pSymbolic)
        self.handle.acNodeMapSetEnumerationValue.argtypes = [
            acNodeMap,
            char_ptr]

        # AC_ERROR acNodeMapExecute(
        #   acNodeMap hNodeMap,
        #   char* pNodeName)
        self.handle.acNodeMapExecute.argtypes = [
            acNodeMap,
            char_ptr]

    def _configure_callback(self):

        c_funcs_list = [
            self.handle.acCallbackRegister,
            self.handle.acCallbackDeregister
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acCallbackRegister(
        #   acCallback* phCallback,
        #   acNode hNode,
        #   acCallbackFunction callbackFunction,
        #   void* pUserData)
        self.handle.acCallbackRegister.argtypes = [
            POINTER(acCallback),
            acNode,
            acCallbackFunction,
            # ArenaC API takes void* but we pass a py_object to
            # receive it in the callback.
            py_object]

        # AC_ERROR acCallbackDeregister(
        #   acCallback hCallback)
        self.handle.acCallbackDeregister.argtypes = [
            acCallback]

    def _configure_node(self):

        c_funcs_list = [
            self.handle.acNodeGetAccessMode,
            self.handle.acNodeGetAlias,
            self.handle.acNodeGetCachingMode,
            self.handle.acNodeGetCastAlias,
            self.handle.acNodeGetNumChildren,
            self.handle.acNodeGetChild,
            self.handle.acNodeGetChildAndAccessMode,
            self.handle.acNodeGetDescription,
            self.handle.acNodeGetDeviceName,
            self.handle.acNodeGetDisplayName,
            self.handle.acNodeGetDocuURL,
            self.handle.acNodeGetEventID,
            self.handle.acNodeGetName,
            self.handle.acNodeGetFullyQualifiedName,
            self.handle.acNodeGetNamespace,
            self.handle.acNodeGetNumParents,
            self.handle.acNodeGetParent,
            self.handle.acNodeGetParentAndAccessMode,
            self.handle.acNodeGetPollingTime,
            self.handle.acNodeGetPrincipalInterfaceType,
            self.handle.acNodeGetProperty,
            self.handle.acNodeGetNumPropertyNames,
            self.handle.acNodeGetPropertyName,
            self.handle.acNodeGetToolTip,
            self.handle.acNodeInvalidateNode,
            self.handle.acNodeGetVisibility,
            self.handle.acNodeImposeVisibility,
            self.handle.acNodeImposeAccessMode,
            self.handle.acNodeIsCachable,
            self.handle.acNodeIsDeprecated,
            self.handle.acNodeIsFeature
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acNodeGetAccessMode(
        #   acNode hNode,
        #   AC_ACCESS_MODE* pAccessMode)
        self.handle.acNodeGetAccessMode.argtypes = [
            acNode,
            POINTER(ac_access_mode)]

        # AC_ERROR acNodeGetAlias(
        #   acNode hNode,
        #   acNode* phAliasNode)
        self.handle.acNodeGetAlias.argtypes = [
            acNode,
            POINTER(acNode)]

        # AC_ERROR acNodeGetCachingMode(
        #   acNode hNode,
        #   AC_CACHING_MODE* pCachingMode)
        self.handle.acNodeGetCachingMode.argtypes = [
            acNode,
            POINTER(ac_caching_mode)]

        # AC_ERROR acNodeGetCastAlias(
        #   acNode hNode,
        #   acNode* phAliasNode)
        self.handle.acNodeGetCastAlias.argtypes = [
            acNode,
            POINTER(acNode)]

        # AC_ERROR acNodeGetNumChildren(
        #   acNode hNode,
        #   size_t* pNumChildren)
        self.handle.acNodeGetNumChildren.argtypes = [
            acNode,
            POINTER(size_t)]

        # AC_ERROR acNodeGetChild(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phChildNode)
        self.handle.acNodeGetChild.argtypes = [
            acNode,
            size_t,
            POINTER(acNode)]

        # AC_ERROR acNodeGetChildAndAccessMode(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phChildNode,
        #   AC_ACCESS_MODE* pAccessMode)
        self.handle.acNodeGetChildAndAccessMode.argtypes = [
            acNode,
            size_t,
            POINTER(acNode),
            POINTER(ac_access_mode)]

        # AC_ERROR acNodeGetDescription(
        #   acNode hNode,
        #   char* pDescriptionBuf,
        #   size_t* pBufLen)
        self.handle.acNodeGetDescription.argtypes = [
            acNode,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acNodeGetDeviceName(
        #   acNode hNode,
        #   char* pDeviceNameBuf,
        #   size_t* pBufLen)
        self.handle.acNodeGetDeviceName.argtypes = [
            acNode,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acNodeGetDisplayName(
        #   acNode hNode,
        #   char* pDisplayNameBuf,
        #   size_t* pBufLen)
        self.handle.acNodeGetDisplayName.argtypes = [
            acNode,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acNodeGetDocuURL(
        #   acNode hNode,
        #   char* pDocuURLBuf,
        #   size_t* pBufLen)
        self.handle.acNodeGetDocuURL.argtypes = [
            acNode,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acNodeGetEventID(
        #   acNode hNode,
        #   char* pEventIDBuf,
        #   size_t* pBufLen)
        self.handle.acNodeGetEventID.argtypes = [
            acNode,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acNodeGetName(
        #   acNode hNode,
        #   char* pNameBuf,
        #   size_t* pBufLen)
        self.handle.acNodeGetName.argtypes = [
            acNode,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acNodeGetFullyQualifiedName(
        #   acNode hNode,
        #   char* pNameBuf,
        #   size_t* pBufLen)
        self.handle.acNodeGetFullyQualifiedName.argtypes = [
            acNode,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acNodeGetNamespace(
        #   acNode hNode,
        #   AC_NAMESPACE* pNameSpace)
        self.handle.acNodeGetNamespace.argtypes = [
            acNode,
            POINTER(ac_namespace)]

        # AC_ERROR acNodeGetNumParents(
        #   acNode hNode,
        #   size_t* pNumParents)
        self.handle.acNodeGetNumParents.argtypes = [
            acNode,
            POINTER(size_t)]

        # AC_ERROR acNodeGetParent(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phParentNode)
        self.handle.acNodeGetParent.argtypes = [
            acNode,
            size_t,
            POINTER(acNode)]

        # AC_ERROR acNodeGetParentAndAccessMode(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phParentNode,
        #   AC_ACCESS_MODE* pAccessMode)
        self.handle.acNodeGetParentAndAccessMode.argtypes = [
            acNode,
            size_t,
            POINTER(acNode),
            POINTER(ac_access_mode)]

        # AC_ERROR acNodeGetPollingTime(
        #   acNode hNode,
        #   int64_t* pPollingTime)
        self.handle.acNodeGetPollingTime.argtypes = [
            acNode,
            POINTER(int64_t)]

        # AC_ERROR acNodeGetPrincipalInterfaceType(
        #   acNode hNode,
        #   AC_INTERFACE_TYPE* pInterfaceType)
        self.handle.acNodeGetPrincipalInterfaceType.argtypes = [
            acNode,
            POINTER(ac_interface_type)]

        # AC_ERROR acNodeGetProperty(
        #   acNode hNode,
        #   const char* pPropertyName,
        #   char* pPropertyValueBuf,
        #   size_t* pPropertyValueBufLen,
        #   char* pPropertyAttributeBuf,
        #   size_t* pPropertyAttributeBufLen)
        self.handle.acNodeGetProperty.argtypes = [
            acNode,
            char_ptr,
            char_ptr,
            POINTER(size_t),
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acNodeGetNumPropertyNames(
        #   acNode hNode,
        #   size_t* pNumPropertyNames)
        self.handle.acNodeGetNumPropertyNames.argtypes = [
            acNode,
            POINTER(size_t)]

        # AC_ERROR acNodeGetPropertyName(
        #   acNode hNode,
        #   size_t index,
        #   char* pPropertyNameBuf,
        #   size_t* pBufLen)
        self.handle.acNodeGetPropertyName.argtypes = [
            acNode,
            size_t,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acNodeGetToolTip(
        #   acNode hNode,
        #   char* pToolTipBuf,
        #   size_t* pBufLen)
        self.handle.acNodeGetToolTip.argtypes = [
            acNode,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acNodeInvalidateNode(
        #   acNode hNode)
        self.handle.acNodeInvalidateNode.argtypes = [
            acNode]

        # AC_ERROR acNodeGetVisibility(
        #   acNode hNode,
        #   AC_VISIBILITY* pVisibility)
        self.handle.acNodeGetVisibility.argtypes = [
            acNode,
            POINTER(ac_visibility)]

        # AC_ERROR acNodeImposeVisibility(
        #   acNode hNode,
        #   AC_VISIBILITY imposedVisibility)
        self.handle.acNodeImposeVisibility.argtypes = [
            acNode,
            ac_visibility]

        # AC_ERROR acNodeImposeAccessMode(
        #   acNode hNode,
        #   AC_ACCESS_MODE imposedAccessMode)
        self.handle.acNodeImposeAccessMode.argtypes = [
            acNode,
            ac_access_mode]

        # AC_ERROR acNodeIsCachable(
        #   acNode hNode,
        #   bool8_t* pIsCachable)
        self.handle.acNodeIsCachable.argtypes = [
            acNode,
            POINTER(bool8_t)]

        # AC_ERROR acNodeIsDeprecated(
        #   acNode hNode,
        #   bool8_t* pIsDeprecated)
        self.handle.acNodeIsDeprecated.argtypes = [
            acNode,
            POINTER(bool8_t)]

        # AC_ERROR acNodeIsFeature(
        #   acNode hNode,
        #   bool8_t* pIsFeature)
        self.handle.acNodeIsFeature.argtypes = [
            acNode,
            POINTER(bool8_t)]

    def _configure_value(self):

        c_funcs_list = [
            self.handle.acValueToString,
            self.handle.acValueFromString,
            self.handle.acValueIsValueCacheValid
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acValueToString(
        #   acNode hNode,
        #   char* pValueBuf,
        #   size_t* pBufLen)
        self.handle.acValueToString.argtypes = [
            acNode,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acValueFromString(
        #   acNode hNode,
        #   char* pValue)
        self.handle.acValueFromString.argtypes = [
            acNode,
            char_ptr]

        # AC_ERROR acValueIsValueCacheValid(
        #   acNode hNode,
        #   bool8_t* pIsValid)
        self.handle.acValueIsValueCacheValid.argtypes = [
            acNode,
            POINTER(bool8_t)]

    def _configure_integer(self):

        c_funcs_list = [
            self.handle.acIntegerGetInc,
            self.handle.acIntegerGetIncMode,
            self.handle.acIntegerGetMax,
            self.handle.acIntegerGetMin,
            self.handle.acIntegerGetRepresentation,
            self.handle.acIntegerGetUnit,
            self.handle.acIntegerGetValue,
            self.handle.acIntegerImposeMin,
            self.handle.acIntegerImposeMax,
            self.handle.acIntegerSetValue
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acInteger
        #   acNode hNode,
        #   int64_t* pIncrement)
        self.handle.acIntegerGetInc.argtypes = [
            acNode,
            POINTER(int64_t)]

        # AC_ERROR acIntegerGetIncMode(
        #   acNode hNode,
        #   AC_INC_MODE* pIncrementMode)
        self.handle.acIntegerGetIncMode.argtypes = [
            acNode,
            POINTER(ac_inc_mode)]

        # AC_ERROR acIntegerGetMax(
        #   acNode hNode,
        #   int64_t* pMaximum)
        self.handle.acIntegerGetMax.argtypes = [
            acNode,
            POINTER(int64_t)]

        # AC_ERROR acIntegerGetMin(
        #   acNode hNode,
        #   int64_t* pMinimum)
        self.handle.acIntegerGetMin.argtypes = [
            acNode,
            POINTER(int64_t)]

        # AC_ERROR acIntegerGetRepresentation(
        #   acNode hNode,
        #   AC_REPRESENTATION* pRepresentation)
        self.handle.acIntegerGetRepresentation.argtypes = [
            acNode,
            POINTER(ac_representation)]

        # AC_ERROR acIntegerGetUnit(
        #   acNode hNode,
        # char* pUnitBuf,
        #   size_t* pBufLen)
        self.handle.acIntegerGetUnit.argtypes = [
            acNode,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acIntegerGetValue(
        #   acNode hNode,
        #   int64_t* pValue)
        self.handle.acIntegerGetValue.argtypes = [
            acNode,
            POINTER(int64_t)]

        # AC_ERROR acIntegerImposeMin(
        #   acNode hNode,
        #   int64_t imposedMinimum)
        self.handle.acIntegerImposeMin.argtypes = [
            acNode,
            int64_t]

        # AC_ERROR acIntegerImposeMax(
        #   acNode hNode,
        #   int64_t imposedMaximum)
        self.handle.acIntegerImposeMax.argtypes = [
            acNode,
            int64_t]

        # AC_ERROR acIntegerSetValue(
        #   acNode hNode,
        #   int64_t value)
        self.handle.acIntegerSetValue.argtypes = [
            acNode,
            int64_t]

    def _configure_boolean(self):

        c_funcs_list = [
            self.handle.acBooleanGetValue,
            self.handle.acBooleanSetValue
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acBooleanGetValue(
        #   acNode hNode,
        #   bool8_t* pValue)
        self.handle.acBooleanGetValue.argtypes = [
            acNode,
            POINTER(bool8_t)]

        # AC_ERROR acBooleanSetValue(
        #   acNode hNode,
        #   bool8_t value)
        self.handle.acBooleanSetValue.argtypes = [
            acNode,
            bool8_t]

    def _configure_command(self):
        c_funcs_list = [
            self.handle.acCommandExecute,
            self.handle.acCommandIsDone
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acCommandExecute(
        #   acNode hNode)
        self.handle.acCommandExecute.argtypes = [
            acNode]

        # AC_ERROR acCommandIsDone(
        #   acNode hNode,
        #   bool8_t* pIsDone)
        self.handle.acCommandIsDone.argtypes = [
            acNode,
            POINTER(bool8_t)]

    def _configure_float(self):

        c_funcs_list = [
            self.handle.acFloatSetValue,
            self.handle.acFloatGetValue,
            self.handle.acFloatGetMin,
            self.handle.acFloatGetMax,
            self.handle.acFloatHasInc,
            self.handle.acFloatGetIncMode,
            self.handle.acFloatGetInc,
            self.handle.acFloatGetRepresentation,
            self.handle.acFloatGetUnit,
            self.handle.acFloatGetDisplayNotation,
            self.handle.acFloatGetDisplayPrecision,
            self.handle.acFloatImposeMin,
            self.handle.acFloatImposeMax
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acFloatSetValue(
        #   acNode hNode,
        #   double value)
        self.handle.acFloatSetValue.argtypes = [
            acNode,
            double]

        # AC_ERROR acFloatGetValue(
        #   acNode hNode,
        #   double* pValue)
        self.handle.acFloatGetValue.argtypes = [
            acNode,
            POINTER(double)]

        # AC_ERROR acFloatGetMin(
        #   acNode hNode,
        #   double* pMinimum)
        self.handle.acFloatGetMin.argtypes = [
            acNode,
            POINTER(double)]

        # AC_ERROR acFloatGetMax(
        #   acNode hNode,
        #   double* pMaximum)
        self.handle.acFloatGetMax.argtypes = [
            acNode,
            POINTER(double)]

        # AC_ERROR acFloatHasInc(
        #   acNode hNode,
        #   bool8_t* pHasInc)
        self.handle.acFloatHasInc.argtypes = [
            acNode,
            POINTER(bool8_t)]

        # AC_ERROR acFloatGetIncMode(
        #   acNode hNode,
        #   AC_INC_MODE* pIncMode)
        self.handle.acFloatGetIncMode.argtypes = [
            acNode,
            POINTER(ac_inc_mode)]

        # AC_ERROR acFloatGetInc(
        #   acNode hNode,
        #   double* pIncrement)
        self.handle.acFloatGetInc.argtypes = [
            acNode,
            POINTER(double)]

        # AC_ERROR acFloatGetRepresentation(
        #   acNode hNode,
        #   AC_REPRESENTATION* pRepresentation)
        self.handle.acFloatGetRepresentation.argtypes = [
            acNode,
            POINTER(ac_representation)]

        # AC_ERROR acFloatGetUnit(
        #   acNode hNode,
        #   char* pUnitBuf,
        #   size_t* pBufLen)
        self.handle.acFloatGetUnit.argtypes = [
            acNode,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acFloatGetDisplayNotation(
        #   acNode hNode,
        #   AC_DISPLAY_NOTATION* pDisplayNotation)
        self.handle.acFloatGetDisplayNotation.argtypes = [
            acNode,
            POINTER(ac_display_notation)]

        # AC_ERROR acFloatGetDisplayPrecision(
        #   acNode hNode,
        #   int64_t* pDisplayPrecision)
        self.handle.acFloatGetDisplayPrecision.argtypes = [
            acNode,
            POINTER(int64_t)]

        # AC_ERROR acFloatImposeMin(
        #   acNode hNode,
        #   double imposedMinimum)
        self.handle.acFloatImposeMin.argtypes = [
            acNode,
            double]

        # AC_ERROR acFloatImposeMax(
        #   acNode hNode,
        #   double imposedMaximum)
        self.handle.acFloatImposeMax.argtypes = [
            acNode,
            double]

    def _configure_string(self):

        c_funcs_list = [
            self.handle.acStringSetValue,
            self.handle.acStringGetValue,
            self.handle.acStringGetMaxLength
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acStringSetValue(
        #   acNode hNode,
        #   char* pValue)
        self.handle.acStringSetValue.argtypes = [
            acNode,
            char_ptr]

        # AC_ERROR acStringGetValue(
        #   acNode hNode,
        #   char* pValue,
        #   size_t* pBufLen)
        self.handle.acStringGetValue.argtypes = [
            acNode,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acStringGetMaxLength(
        #   acNode hNode,
        #   int64_t* pMaxLength)
        self.handle.acStringGetMaxLength.argtypes = [
            acNode,
            POINTER(int64_t)]

    def _configure_register(self):

        c_funcs_list = [
            self.handle.acRegisterSet,
            self.handle.acRegisterGet
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acRegisterSet(
        #   acNode hNode,
        #   const uint8_t* pBuf,
        #   int64_t bufLen)
        self.handle.acRegisterSet.argtypes = [
            acNode,
            POINTER(uint8_t),
            int64_t]

        # AC_ERROR acRegisterGet(
        #   acNode hNode,
        #   uint8_t* pBuf,
        #   int64_t bufLen)
        self.handle.acRegisterGet.argtypes = [
            acNode,
            POINTER(uint8_t),
            int64_t]

    def _configure_category(self):

        c_funcs_list = [
            self.handle.acCategoryGetNumFeatures,
            self.handle.acCategoryGetFeature,
            self.handle.acCategoryGetFeatureAndAccessMode
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acCategoryGetNumFeatures(
        #   acNode hNode,
        #   size_t* pNumFeatures)
        self.handle.acCategoryGetNumFeatures.argtypes = [
            acNode,
            POINTER(size_t)]

        # AC_ERROR acCategoryGetFeature(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phFeatureNode)
        self.handle.acCategoryGetFeature.argtypes = [
            acNode,
            size_t,
            POINTER(acNode)]

        # AC_ERROR acCategoryGetFeatureAndAccessMode(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phFeatureNode,
        #   AC_ACCESS_MODE* pAccessMode)
        self.handle.acCategoryGetFeatureAndAccessMode.argtypes = [
            acNode,
            size_t,
            POINTER(acNode),
            POINTER(ac_access_mode)]

    def _configure_enumeration(self):

        c_funcs_list = [
            self.handle.acEnumerationGetNumEntries,
            self.handle.acEnumerationGetEntryByIndex,
            self.handle.acEnumerationGetEntryAndAccessModeByIndex,
            self.handle.acEnumerationGetNumSymbolics,
            self.handle.acEnumerationGetSymbolicByIndex,
            self.handle.acEnumerationSetByIntValue,
            self.handle.acEnumerationSetBySymbolic,
            self.handle.acEnumerationGetEntryByName,
            self.handle.acEnumerationGetEntryAndAccessModeByName,
            self.handle.acEnumerationGetCurrentEntry,
            self.handle.acEnumerationGetCurrentEntryAndAccessMode,
            self.handle.acEnumerationGetCurrentSymbolic
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acEnumerationGetNumEntries(
        #   acNode hNode,
        #   size_t* pNumEntries)
        self.handle.acEnumerationGetNumEntries.argtypes = [
            acNode,
            POINTER(size_t)]

        # AC_ERROR acEnumerationGetEntryByIndex(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phEntryNode)
        self.handle.acEnumerationGetEntryByIndex.argtypes = [
            acNode,
            size_t,
            POINTER(acNode)]

        # AC_ERROR acEnumerationGetEntryAndAccessModeByIndex(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phEntryNode,
        #   AC_ACCESS_MODE* pAccessMode)
        self.handle.acEnumerationGetEntryAndAccessModeByIndex.argtypes = [
            acNode,
            size_t,
            POINTER(acNode),
            POINTER(ac_access_mode)]

        # AC_ERROR acEnumerationGetNumSymbolics(
        #   acNode hNode,
        #   size_t* pNumSymbolics)
        self.handle.acEnumerationGetNumSymbolics.argtypes = [
            acNode,
            POINTER(size_t)]

        # AC_ERROR acEnumerationGetSymbolicByIndex(
        #   acNode hNode,
        #   size_t index,
        #   char* pSymbolicBuf,
        #   size_t* pBufLen)
        self.handle.acEnumerationGetSymbolicByIndex.argtypes = [
            acNode,
            size_t,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acEnumerationSetByIntValue(
        #   acNode hNode,
        #   int64_t value)
        self.handle.acEnumerationSetByIntValue.argtypes = [
            acNode,
            int64_t]

        # AC_ERROR acEnumerationSetBySymbolic(
        #   acNode hNode,
        #   const char* pSymbolic)
        self.handle.acEnumerationSetBySymbolic.argtypes = [
            acNode,
            char_ptr]

        # AC_ERROR acEnumerationGetEntryByName(
        #   acNode hNode,
        #   const char* pEntryName,
        #   acNode* phEntryNode)
        self.handle.acEnumerationGetEntryByName.argtypes = [
            acNode,
            char_ptr,
            acNode]

        # AC_ERROR acEnumerationGetEntryAndAccessModeByName(
        #   acNode hNode,
        #   char* pEntryName,
        #   acNode* phEntryNode,
        #   AC_ACCESS_MODE* pAccessMode)
        self.handle.acEnumerationGetEntryAndAccessModeByName.argtypes = [
            acNode,
            char_ptr,
            POINTER(acNode),
            ac_access_mode]

        # AC_ERROR acEnumerationGetCurrentEntry(
        #   acNode hNode,
        #   acNode* phEntryNode)
        self.handle.acEnumerationGetCurrentEntry.argtypes = [
            acNode,
            POINTER(acNode)]

        # AC_ERROR acEnumerationGetCurrentEntryAndAccessMode(
        #   acNode hNode,
        #   acNode* phEntryNode,
        #   AC_ACCESS_MODE* pAccessMode)
        self.handle.acEnumerationGetCurrentEntryAndAccessMode.argtypes = [
            acNode,
            POINTER(acNode),
            POINTER(ac_access_mode)]

        # AC_ERROR acEnumerationGetCurrentSymbolic(
        #   acNode hNode,
        #   char* pSymbolicBuf,
        #   size_t* pBufLen)
        self.handle.acEnumerationGetCurrentSymbolic.argtypes = [
            acNode,
            char_ptr,
            POINTER(size_t)]

    def _configure_enumentry(self):

        c_funcs_list = [
            self.handle.acEnumEntryGetIntValue,
            self.handle.acEnumEntryGetNumericValue,
            self.handle.acEnumEntryGetSymbolic,
            self.handle.acEnumEntryIsSelfClearing
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acEnumEntryGetIntValue(
        #   acNode hNode,
        #   int64_t* pValue)
        self.handle.acEnumEntryGetIntValue.argtypes = [
            acNode,
            POINTER(int64_t)]

        # AC_ERROR acEnumEntryGetNumericValue(
        #   acNode hNode,
        #   double* pValue)
        self.handle.acEnumEntryGetNumericValue.argtypes = [
            acNode,
            POINTER(double)]

        # AC_ERROR acEnumEntryGetSymbolic(
        #   acNode hNode,
        #   char* pSymbolicBuf,
        #   size_t* pBufLen)
        self.handle.acEnumEntryGetSymbolic.argtypes = [
            acNode,
            char_ptr,
            POINTER(size_t)]

        # AC_ERROR acEnumEntryIsSelfClearing(
        #   acNode hNode,
        #   bool8_t* pIsSelfClearing)
        self.handle.acEnumEntryIsSelfClearing.argtypes = [
            acNode,
            POINTER(bool8_t)]

    def _configure_selector(self):

        c_funcs_list = [
            self.handle.acSelectorIsSelector,
            self.handle.acSelectorGetNumSelectingFeatures,
            self.handle.acSelectorGetSelectingFeature,
            self.handle.acSelectorGetSelectingFeatureAndAccessMode,
            self.handle.acSelectorGetNumSelectedFeatures,
            self.handle.acSelectorGetSelectedFeature,
            self.handle.acSelectorGetSelectedFeatureAndAccessMode
        ]
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # AC_ERROR acSelectorIsSelector(
        #   acNode hNode,
        #   bool8_t* pIsSelector)
        self.handle.acSelectorIsSelector.argtypes = [
            acNode,
            POINTER(bool8_t)]

        # AC_ERROR acSelectorGetNumSelectingFeatures(
        #   acNode hNode,
        #   size_t* pNumSelectingFeatures)
        self.handle.acSelectorGetNumSelectingFeatures.argtypes = [
            acNode,
            POINTER(size_t)]

        # AC_ERROR acSelectorGetSelectingFeature(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phSelectingFeatureNode)
        self.handle.acSelectorGetSelectingFeature.argtypes = [
            acNode,
            size_t,
            POINTER(acNode)]

        # AC_ERROR acSelectorGetSelectingFeatureAndAccessMode(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phSelectingFeatureNode,
        #   AC_ACCESS_MODE* pAccessMode)
        self.handle.acSelectorGetSelectingFeatureAndAccessMode.argtypes = [
            acNode,
            size_t,
            POINTER(acNode),
            POINTER(ac_access_mode)]

        # AC_ERROR acSelectorGetNumSelectedFeatures(
        #   acNode hNode,
        #   size_t* pNumSelectedFeatures)
        self.handle.acSelectorGetNumSelectedFeatures.argtypes = [
            acNode,
            POINTER(size_t)]

        # AC_ERROR acSelectorGetSelectedFeature(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phSelectedFeatureNode)
        self.handle.acSelectorGetSelectedFeature.argtypes = [
            acNode,
            size_t,
            POINTER(acNode)]

        # AC_ERROR acSelectorGetSelectedFeatureAndAccessMode(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phSelectedFeatureNode,
        #   AC_ACCESS_MODE* pAccessMode)
        self.handle.acSelectorGetSelectedFeatureAndAccessMode.argtypes = [
            acNode,
            size_t,
            POINTER(acNode),
            POINTER(ac_access_mode)]
