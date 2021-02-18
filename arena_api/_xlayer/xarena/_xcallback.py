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
from arena_api._xlayer.xarena.arenac_types import (acCallback,
                                                   acCallbackFunction, acNode)


class _xCallback():
    def __init__(self):
        pass

    def xCallbackRegister(self, h_node, py_callback_function, args_and_kwargs):

        handle = acCallback(None)
        node = acNode(h_node)
        c_callback_function = acCallbackFunction(py_callback_function)
        args_and_kwargs_as_py_object = py_object(args_and_kwargs)

        #
        # arenac dll
        #
        # AC_ERROR acCallbackRegister(
        #   acCallback* phCallback,
        #   acNode hNode,
        #   acCallbackFunction callbackFunction,
        #   void* pUserData)

        #
        # configured
        #
        # harenac.acCallbackRegister.argtypes = [
        #   POINTER(acCallback),
        #   acNode,
        #   acCallbackFunction,
        #   # ArenaC API takes void* but we pass a py_object to
        #   # receive it in the callback.
        #   py_object]

        harenac.acCallbackRegister(
            byref(handle),
            node,
            c_callback_function,
            args_and_kwargs_as_py_object)

        # needs to be taken out because ref count must stay positive until
        # the callback is called
        to_add_to_registry_entry = {
            '_c_callback_function': c_callback_function,
            '_args_and_kwargs_as_py_object': args_and_kwargs_as_py_object
        }
        return handle.value, to_add_to_registry_entry

    def xCallbackDeregister(self, handle):

        handle = acCallback(handle)
        #
        # arenac dll
        #
        # AC_ERROR acCallbackDeregister(
        #   acCallback hCallback)

        #
        # configured
        #
        # harenac.acCallbackDeregister.argtypes = [
        #   acCallback]
        harenac.acCallbackDeregister(handle)
