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
from arena_api._xlayer.xarena.arenac_defaults import (
    XARENA_STR_BUFFER_SIZE_1000, XARENA_STR_BUFFER_SIZE_DEFAULT)
from arena_api._xlayer.xarena.arenac_types import (acNode, acSystem, bool8_t,
                                                   size_t)


class _xGlobal():

    @staticmethod
    def xOpenSystem():
        hxsystem = acSystem(None)
        # AC_ERROR acOpenSystem(
        #   acSystem* phSystem)
        harenac.acOpenSystem(
            byref(hxsystem))

        if not hxsystem.value:
            raise TypeError(
                f'failed : system return as None')

        return hxsystem.value

    @staticmethod
    def xCloseSystem(hxsystem):
        system = acSystem(hxsystem)
        # AC_ERROR acCloseSystem(
        #   acSystem hSystem)
        harenac.acCloseSystem(system)

        if not system.value:
            raise TypeError(
                f'failed : system return as None')

    # ---------------------------------------------------------------------

    @staticmethod
    def xIsReadable(h_node):
        node = acNode(h_node)
        is_readable = bool8_t(False)
        # AC_ERROR acIsReadable(
        #   acNode hNode,
        #   bool8_t* pIsReadable)
        harenac.acIsReadable(
            node,
            byref(is_readable))

        return is_readable.value

    @staticmethod
    def xIsWritable(h_node):
        node = acNode(h_node)
        is_writable = bool8_t(False)
        # AC_ERROR acIsWritable(
        #   acNode hNode,
        #   bool8_t* pIsWritable)

        harenac.acIsWritable(
            node,
            byref(is_writable))

        return is_writable.value

    @staticmethod
    def xGetLastErrorMessage():
        error_msg_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_1000)
        error_msg_len = size_t(XARENA_STR_BUFFER_SIZE_1000)

        # AC_ERROR acGetLastErrorMessage(
        #   char* pMessageBuf,
        #   size_t* pBufLen)
        harenac.acGetLastErrorMessage(
            error_msg_p,
            byref(error_msg_len))

        return error_msg_p.value.decode()

    # ---------------------------------------------------------------------

    # TODO SFW-2193
    # TODO SFW-2191
    # TODO SFW-2192
