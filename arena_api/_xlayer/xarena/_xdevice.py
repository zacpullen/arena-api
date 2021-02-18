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

from ctypes import byref, py_object

from arena_api._xlayer.xarena.arenac import harenac
from arena_api._xlayer.xarena.arenac_types import (acBuffer, acCallback,
                                                   acDevice,
                                                   acImageCallbackFunction,
                                                   acNodeMap, size_t, uint64_t)


class _xDevice():

    def __init__(self, hxdevice):
        # TODO SFW-2546
        if not hxdevice:
            raise TypeError('xDevice handle is None')
        self.hxdevice = acDevice(hxdevice)

    # Stream ------------------------------------------------------------------

    def xDeviceStartStream(self):

        # AC_ERROR acDeviceStartStream(
        #   acDevice hDevice)
        harenac.acDeviceStartStream(self.hxdevice)

    def xDeviceStartStreamNumBuffersAndFlags(self, num_of_buffers):

        num_of_buffers = size_t(num_of_buffers)
        # AC_ERROR acDeviceStartStreamNumBuffersAndFlags(
        #   acDevice hDevice,
        #   size_t numBuffers);
        harenac.acDeviceStartStreamNumBuffersAndFlags(
            self.hxdevice,
            num_of_buffers)

    def xDeviceStopStream(self):

        # AC_ERROR acDeviceStopStream(
        #   acDevice hDevice)
        harenac.acDeviceStopStream(self.hxdevice)

    # Buffer ------------------------------------------------------------------

    def xDeviceGetBuffer(self, timeout):

        timeout = uint64_t(timeout)
        h_buffer = acBuffer(None)
        # AC_ERROR acDeviceGetBuffer(
        #   acDevice hDevice,
        #   uint64_t timeout,
        #   acBuffer* phBuffer)

        harenac.acDeviceGetBuffer(self.hxdevice,
                                  timeout,
                                  byref(h_buffer))

        return h_buffer.value

    def xDeviceRequeueBuffer(self,  buffer_p):

        h_buffer = acBuffer(buffer_p)
        # AC_ERROR acDeviceRequeueBuffer(
        #   acDevice hDevice,
        #   acBuffer pBuffer);
        harenac.acDeviceRequeueBuffer(self.hxdevice, h_buffer)

    # Event -------------------------------------------------------------------

    def xDeviceInitializeEvents(self):

        # AC_ERROR acDeviceInitializeEvents(
        #   acDevice hDevice)
        harenac.acDeviceInitializeEvents(self.hxdevice)

    def xDeviceDeinitializeEvents(self):

        # AC_ERROR acDeviceDeinitializeEvents(
        #   acDevice hDevice)
        harenac.acDeviceDeinitializeEvents(self.hxdevice)

    def xDeviceWaitOnEvent(self, timeout):

        # AC_ERROR acDeviceWaitOnEvent(
        #   acDevice hDevice,
        #   int64_t timeout)
        harenac.acDeviceWaitOnEvent(self.hxdevice, timeout)

    # NodeMaps ----------------------------------------------------------------

    def xDeviceGetNodeMap(self):

        h_nodemap = acNodeMap(None)
        # AC_ERROR acDeviceGetNodeMap(
        #   acDevice hDevice,
        #   acNodeMap* phNodeMap)
        harenac.acDeviceGetNodeMap(self.hxdevice,
                                   byref(h_nodemap))

        return h_nodemap.value

    def xDeviceGetTLDeviceNodeMap(self):

        h_tl_device_nodemap = acNodeMap(None)
        # AC_ERROR acDeviceGetTLDeviceNodeMap(
        #   acDevice hDevice,
        #   acNodeMap* phNodeMap)

        harenac.acDeviceGetTLDeviceNodeMap(
            self.hxdevice,
            byref(h_tl_device_nodemap))

        return h_tl_device_nodemap.value

    def xDeviceGetTLStreamNodeMap(self):

        h_tl_stream_nodemap = acNodeMap(None)
        # AC_ERROR acDeviceGetTLStreamNodeMap(
        #   acDevice hDevice,
        #   acNodeMap* phNodeMap)
        harenac.acDeviceGetTLStreamNodeMap(self.hxdevice,
                                           byref(h_tl_stream_nodemap))

        return h_tl_stream_nodemap.value

    def xDeviceGetTLInterfaceNodeMap(self):

        h_tl_interface_nodemap = acNodeMap(None)
        # AC_ERROR acDeviceGetTLInterfaceNodeMap(
        #   acDevice hDevice,
        #   acNodeMap* phNodeMap)
        harenac.acDeviceGetTLInterfaceNodeMap(
            self.hxdevice,
            byref(h_tl_interface_nodemap))

        return h_tl_interface_nodemap.value

    def xDeviceRegisterImageCallback(self, py_callback_function,
                                     args_and_kwargs):

        handle = acCallback(None)
        c_callback_function = acImageCallbackFunction(
            py_callback_function)
        args_and_kwargs_as_py_object = py_object(args_and_kwargs)
        #
        # arenac dll
        #
        # AC_ERROR acDeviceRegisterImageCallback(
        #   acDevice hDevice,
        #   acCallback* phCallback,
        #   acImageCallbackFunction callbackFn,
        #   void* pUserData)

        #
        # configured
        #
        # harenac.acDeviceRegisterImageCallback.argtypes = [
        #    acDevice,
        #    POINTER(acCallback),
        #    acImageCallbackFunction,
        #    # ArenaC API takes void* but we pass a py_object to
        #    # receive it in the callback.
        #    py_object]

        harenac.acDeviceRegisterImageCallback(
            self.hxdevice,
            byref(handle),
            c_callback_function,
            args_and_kwargs_as_py_object
        )

        # needs to be taken out because ref count must stay positive until
        # the callback is called
        to_add_to_registry_entry = {
            '_c_callback_function': c_callback_function,
            '_args_and_kwargs_as_py_object': args_and_kwargs_as_py_object
        }
        return handle.value, to_add_to_registry_entry

    def xDeviceDeregisterImageCallback(self, handle):

        handle = acCallback(handle)
        #
        # arenacc dll
        #
        # AC_ERROR acDeviceDeregisterImageCallback(
        #   acDevice hDevice,
        #   acCallback* phCallback)

        #
        # configured
        #
        # harenac.acDeviceDeregisterImageCallback.argtypes = [
        #    acDevice,
        #    POINTER(acCallback)]
        harenac.acDeviceDeregisterImageCallback(
            self.hxdevice,
            byref(handle)
        )
