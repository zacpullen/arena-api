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

from ctypes import POINTER, byref, create_string_buffer

from arena_api._xlayer.xarena.arenac import harenac
from arena_api._xlayer.xarena.arenac_defaults import \
    XARENA_STR_BUFFER_SIZE_DEFAULT
from arena_api._xlayer.xarena.arenac_types import *


class _xNodemap():

    def __init__(self, h_nodemap):
        # TODO SFW-2546
        if not h_nodemap:
            raise TypeError('h_nodemap handle is None')
        self.h_nodemap = acNodeMap(h_nodemap)

    def xNodeMapInvalidateNodes(self):

        # AC_ERROR acNodeMapInvalidateNodes(
        #   acNodeMap hNodeMap)
        harenac.acNodeMapInvalidateNodes(
            self.h_nodemap)

    def xNodeMapGetDeviceName(self):

        device_name_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_DEFAULT)
        buf_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acNodeMapGetDeviceName(
        #   acNodeMap hNodeMap,
        #   char* pDeviceNameBuf,
        #   size_t* pBufLen)
        harenac.acNodeMapGetDeviceName(
            self.h_nodemap,
            device_name_p,
            byref(buf_len))

        return device_name_p.value.decode()

    def xNodeMapPoll(self, elapsed_time_milsec):

        elapsed_time = int64_t(elapsed_time_milsec)
        # AC_ERROR acNodeMapPoll(
        #   acNodeMap hNodeMap,
        #   int64_t elapsedTime)
        harenac.acNodeMapPoll(
            self.h_nodemap,
            elapsed_time)

    # locking -------------------------------------------------------------

    def xNodeMapLock(self):

        # AC_ERROR acNodeMapLock(
        #   acNodeMap hNodeMap)
        harenac.acNodeMapLock(
            self.h_nodemap)

    def xNodeMapUnlock(self):

        # AC_ERROR acNodeMapUnlock(
        #   acNodeMap hNodeMap)
        harenac.acNodeMapUnlock(
            self.h_nodemap)

    def xNodeMapTryLock(self):

        is_locked = bool8_t(False)
        # AC_ERROR acNodeMapTryLock(
        #   acNodeMap hNodeMap,
        #   bool8_t* pLocked)
        harenac.acNodeMapTryLock(
            self.h_nodemap,
            byref(is_locked))

        return is_locked.value

    # node ----------------------------------------------------------------

    # Get node

    def xNodeMapGetNumNodes(self):

        num_nodes = uint64_t(0)
        # AC_ERROR acNodeMapGetNumNodes(
        #   acNodeMap hNodeMap,
        #   uint64_t* pNumNodes)
        harenac.acNodeMapGetNumNodes(
            self.h_nodemap,
            byref(num_nodes))

        return num_nodes.value

    def xNodeMapGetNode(self, node_name):

        node_name_p = char_ptr(node_name.encode())
        node = acNode(None)
        # AC_ERROR acNodeMapGetNode(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   acNode* phNode)
        harenac.acNodeMapGetNode(
            self.h_nodemap,
            node_name_p,
            byref(node))

        return node.value

    def xNodeMapGetNodeAndAccessMode(self, node_name):

        node_name_p = char_ptr(node_name.encode())
        node = acNode(None)
        access_mode = ac_access_mode(0)
        # AC_ERROR acNodeMapGetNodeAndAccessMode(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   acNode* phNode,
        #   AC_ACCESS_MODE* pAccessMode)
        harenac.acNodeMapGetNodeAndAccessMode(
            self.h_nodemap,
            node_name_p,
            byref(node),
            byref(access_mode))

        return node.value, access_mode.value

    def xNodeMapGetNodeByIndex(self, index):

        index = size_t(index)
        node = acNode(None)
        # AC_ERROR acNodeMapGetNodeByIndex(
        #   acNodeMap hNodeMap,
        #   size_t index,
        #   acNode* phNode)
        harenac.acNodeMapGetNodeByIndex(
            self.h_nodemap,
            index,
            byref(node))

        return node.value

    def xNodeMapGetNodeByIndexAndAccessMode(self, index):

        index = size_t(index)
        node = acNode(None)
        access_mode = ac_access_mode(0)
        # AC_ERROR acNodeMapGetNodeByIndexAndAccessMode(
        #   acNodeMap hNodeMap,
        #   size_t index,
        #   acNode* phNode,
        #   AC_ACCESS_MODE* pAccessMode)
        harenac.acNodeMapGetNodeByIndexAndAccessMode(
            self.h_nodemap,
            index,
            byref(node),
            byref(access_mode))

        return node.value, access_mode.value

    # Get node value

    def xNodeMapGetStringValue(self, node_name):

        node_name_p = char_ptr(node_name.encode())
        str_value_buf_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_DEFAULT)
        str_value_buf_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acNodeMapGetStringValue(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   char* pValueBuf,
        #   size_t* pBufLen)
        harenac.acNodeMapGetStringValue(
            self.h_nodemap,
            node_name_p,
            str_value_buf_p,
            byref(str_value_buf_len))

        return str_value_buf_p.value.decode()

    def xNodeMapGetIntegerValue(self, node_name):

        node_name_p = char_ptr(node_name.encode())
        int_value = int64_t(0)
        # AC_ERROR acNodeMapGetIntegerValue(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   int64_t* pValue)
        harenac.acNodeMapGetIntegerValue(
            self.h_nodemap,
            node_name_p,
            byref(int_value))

        return int_value.value

    def xNodeMapGetFloatValue(self, node_name):

        node_name_p = char_ptr(node_name.encode())
        float_value = double(0)  # double is float here
        # AC_ERROR acNodeMapGetFloatValue(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   double* pValue)
        harenac.acNodeMapGetFloatValue(
            self.h_nodemap,
            node_name_p,
            byref(float_value))

        return float_value.value

    def xNodeMapGetBooleanValue(self, node_name):

        node_name_p = char_ptr(node_name.encode())
        bool_value = bool8_t(False)
        # AC_ERROR acNodeMapGetBooleanValue(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   bool8_t* pValue)
        harenac.acNodeMapGetBooleanValue(
            self.h_nodemap,
            node_name_p,
            byref(bool_value))

        return bool_value.value

    def xNodeMapGetEnumerationValue(self, node_name):

        node_name_p = char_ptr(node_name.encode())
        symbolic_value_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_DEFAULT)
        symbolic_value_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acNodeMapGetEnumerationValue(
        #   acNodeMap hNodeMap,
        #   char * pNodeName,
        #   char* pSymbolicBuf,
        #   size_t* pBufLen)
        harenac.acNodeMapGetEnumerationValue(
            self.h_nodemap,
            node_name_p,
            symbolic_value_p,
            byref(symbolic_value_len))

        return symbolic_value_p.value.decode()

    # Set node value

    def xNodeMapSetStringValue(self, node_name, value):

        node_name_p = char_ptr(node_name.encode())
        value_p = char_ptr(value.encode())
        value_len = size_t(len(value))
        # AC_ERROR acNodeMapSetStringValue(
        #   acNodeMap hNodeMap,
        #   char * pNodeName,
        #   char* pSymbolicBuf,
        #   size_t* pBufLen)
        harenac.acNodeMapSetStringValue(
            self.h_nodemap,
            node_name_p,
            value_p,
            byref(value_len))

    def xNodeMapSetIntegerValue(self, node_name, value):

        node_name_p = char_ptr(node_name.encode())
        value = int64_t(value)
        # AC_ERROR acNodeMapSetIntegerValue(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   int64_t value)
        harenac.acNodeMapSetIntegerValue(
            self.h_nodemap,
            node_name_p,
            byref(value))

    def xNodeMapSetFloatValue(self, node_name, value):

        node_name_p = char_ptr(node_name.encode())
        value = double(value)
        # AC_ERROR acNodeMapSetFloatValue(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   double value)
        harenac.acNodeMapSetFloatValue(
            self.h_nodemap,
            node_name_p,
            value)

    def xNodeMapSetBooleanValue(self, node_name, value):

        node_name_p = char_ptr(node_name.encode())
        value = bool8_t(value)
        # AC_ERROR acNodeMapSetBooleanValue(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   bool8_t value)
        harenac.acNodeMapSetBooleanValue(
            self.h_nodemap,
            node_name_p,
            value)

        return node_name_p.value

    def xNodeMapSetEnumerationValue(self, node_name, value):

        node_name_p = char_ptr(node_name.encode())
        value_p = char_ptr(value.encode())
        # AC_ERROR acNodeMapSetEnumerationValue(
        #   acNodeMap hNodeMap,
        #   char* pNodeName,
        #   char* pSymbolic)
        harenac.acNodeMapSetEnumerationValue(
            self.h_nodemap,
            node_name_p,
            value_p)

    def xNodeMapExecute(self, node_name):

        node_name_p = char_ptr(node_name.encode())
        # AC_ERROR acNodeMapExecute(
        #   acNodeMap hNodeMap,
        #   char* pNodeName)
        harenac.acNodeMapExecute(
            self.h_nodemap,
            node_name_p)
