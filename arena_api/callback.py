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

from ctypes import cast, py_object
from functools import wraps

from arena_api import _node_helpers
from arena_api import buffer as _buffer
from arena_api._xlayer.xarena._xcallback import _xCallback
from arena_api._device import Device as _Device
from arena_api._node import Node as _Node


class _Callback:
    '''
    This class registers, deregisters, and maintain a record of all callbacks.
    The class is a singleton, and an instance gets created when arena_api
    module is imported. Use ``from arena_api.callback import
    callback`` to import the _Callback instance.

    :Warning:
    - The instance of the class ``_Callback``, ``callback`` is \
    created when ``arena_api.callback`` module is imported the first time. \
    Every other import after that would return the same instance.
    - Deregister handles before destroying it or memory will leak.
    - Import the instance ``callback`` not the class it self as this class \
    is not be instantiated by the user.

    *New in version 1.7.0*

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    __singleton = None
    __run_init = True

    def __new__(cls, *args, **kwargs):

        if not cls.__singleton:
            cls.__singleton = super(_Callback, cls).__new__(
                cls, *args, **kwargs)
        return cls.__singleton

    def __init__(self):

        if not self.__run_init:
            return
        else:
            self.__run_init = False

        self.xcb = _xCallback()
        self.registry = {}

        # TODO Make global to the file
        self._supported_objs = (
            _Device,
            _Node,
        )

        # TODO Make global to the file
        self._device_callback = _DeviceCallback()
        self._node_callback = _NodeCallback(self.xcb)
        self._supported_decorators = _CallbackFunction().supported_decorators

    def register(self, obj, callback_function, *args, **kwargs):
        '''
        Registers a python function as a callback function to an ``arena_api``\
         object. The supported objects are:
            - ``Device``
                - ``on_buffer`` event
            - ``Node``
                - ``on_update`` event

        **Args**:
            obj :
                - must be an instance of ``_Device`` or ``_Node``.
            callback_function :
                - A python function to callback.\n
                - A callback function must be decorated, and based on the \
                decorator it would have a specific signature that has \
                mandatory and optional parameters.\n

                For decorator ``@callback.device.on_buffer`` the \
                signature is ``callback_func(buffer , *args, **kwargs )``\n

                For decorator  ``@callback.node.on_update`` the \
                signature is ``callback_func(node , *args, **kwargs )``\n

                buffer and node will be passed to the callback function when \
                the event happen. The user should pass the optional arguments\
                when registering the callback function on the object so \
                the user will receive them at the callback later Example :
                    >>> from arena_api.callback import callback
                    >>> from arena_api.callback import callback_function
                    >>> 
                    >>> # create a callback function
                    >>> @callback_function.node.on_update
                    >>> def callback_print_node_value(node , *args , **kwargs):
                    >>>    print(f'{node.name} node value = {node.value}')
                    >>> 
                    >>> # create a device and get a node
                    >>> # <code here>
                    >>> # -------------------------------
                    >>>
                    >>> # register the callback on the node object
                    >>> handle = callback.register(my_node , callback_print_node_value, my_optional_argument)
                    >>> # no every time the node gets invalidated by modification or by parents and child nodes
                    >>> # the callback will ba called.
                    >>> my_node.value = 10000
                    >>> callback.deregister(handle)
                    >>> system.destroy_device()
                    >>>

            ``*args`` :
                optional positional arguments for the callback function.
                in the signature they are after the mandatory arg(s)\n
            ``**kwargs`` :
                optional positional arguments for the callback function.
                in the signature they are after the mandatory arg(s)\n

        **Raises**:
            - ``TypeError`` :
                - ``Obj`` is not an instance of ``_Device`` or ``_Node``.\n
            - ``ValueError``:
                - ``callback_function`` is not decorated or decorated with unsupported decorator
                - ``obj`` instance  and ``callback_function``combination is already registered

        **Returns**:
            - a handle to the callback which is used to deregister the
            callback later via ``callback.deregister()``.\n

        :warning:
        - Node registration:
            - register only on nodes from ``device.nodemap``. \
                ``device.tl_device_nodemap``, ``device.tl_stream_nodemap``, \
                    and ``device.tl_interface_nodemap`` nodes are \
                    not supported.
        - All callback function handles must be deregistered via \
        ``callback.deregister()`` or memory will leak.
        - The callback_function must be decorated.

        **------------------------------------------------------------------**\
        **-------------------------------------------------------------------**
        '''

        # input checks --------------------------------------------------------

        # Check Obj arg
        if not isinstance(obj, self._supported_objs):
            raise TypeError(f'\'{type(obj).__name__}\' type is not supported. '
                            f'The supported types ' f'are:\n{self._supported_objs}')

        # check function decorators
        # TODO dont have to check this change to try and catch
        decorated = hasattr(callback_function, '_decorator')

        if not decorated or callback_function._decorator not in self._supported_decorators:
            decorators_list_with_at = [
                f'@{deco}' for deco in self._supported_decorators]
            raise ValueError(f'\'{callback_function.__name__}\' must be decorated to be '
                             f'registered.\nThe available decorators are:\n'
                             f'{decorators_list_with_at}')

        # check if already registered
        for handle_info in self.registry.values():
            if handle_info['obj'] is obj and handle_info['callback_function'] is callback_function:
                raise ValueError(f'callback_function \'{callback_function.__name__}\' is already '
                                 f'registered for obj \'{obj}\'')

        # Check if the obj is good to access

        # register ------------------------------------------------------------

        # get handle
        registry_entry = None
        if isinstance(obj, _Device):
            registry_entry = self._device_callback.register(obj,
                                                            callback_function,
                                                            *args,
                                                            **kwargs)
        elif isinstance(obj, _Node):
            registry_entry = self._node_callback.register(obj,
                                                          callback_function,
                                                          *args,
                                                          **kwargs)
        else:
            raise ValueError(f'internal error : {obj} is not a supported type')

        # add to registry
        self.registry.update(registry_entry)
        callback_handle = list(registry_entry.keys())[0]
        return callback_handle

    def deregister(self, callback_handle):
        '''
        deregisters the callback function using the handle \
        returned form when the calls ``callback.register()``. \n

        **Args**:
            callback_handle :
                the value returned from ``callback.register()``.\n

        **Raises**:
            - ``ValueError`` :
                - callback_handle is already deregistered or never been \
                    associated with a callback.
                - callback_handle is not int or list/tuple of int
                - callback_handle is registered for a destroyed obj. \
                ``callback.deregister()`` should be called \
                    before destroying the obj instance.\n

        **Returns**:
            - ``None``\n

        **------------------------------------------------------------------**\
        **-------------------------------------------------------------------**
        '''

        # input checks --------------------------------------------------------
        callback_handle_list = []
        if isinstance(callback_handle, int):
            callback_handle_list.append(callback_handle)
        elif not isinstance(callback_handle, (list, tuple)):
            raise ValueError(
                f'expected list or tuple instead of {type(callback_handle).__name__}')
        elif not all(isinstance(handle, int) for handle in callback_handle):
            raise ValueError(f'expected list or tuple of int')
        else:
            callback_handle_list = callback_handle

        for handle in callback_handle_list:
            if not self._is_handle_in_registry(handle):
                raise ValueError('the callback_handle is not registered')

            self._deregister_handle(handle)

    def handle_info(self, handle):
        '''
        In case of a big collection of handles, it is useful to have
        information about the handles of the registered callbacks.\
            The returned dictionary has the following public keys: \n
        - ``obj`` the instance object that the callback function is registered on.
        - ``callback_function`` the callback function to call.
        - ``args_and_kwargs`` the optional arguments that was passed to ``callback.register()``

        **Args**:
            handle:
                the value returned from ``callback.register()``.\n

        **Raises**:
            - ``TypeError``:
                - handle is not of type int.\n
        **Returns**:
            - ``None`` if handle is not in ``callback.registry``.\n
            - ``dict`` if the handle is in ``callback.registry``

        **------------------------------------------------------------------**\
        **-------------------------------------------------------------------**
        '''

        if not isinstance(handle, int):
            raise TypeError(f'int expected instead '
                            f'of {type(handle).__name__}')

        if handle in self.registry.keys():
            return self.registry[handle]
        else:
            return None

    def _deregister_handle(self, callback_handle):

        # deregister ----------------------------------------------------------
        obj = self.registry[callback_handle]['obj']
        if isinstance(obj, _Device):
            self._device_callback.deregister(obj, callback_handle)
        elif isinstance(obj, _Node):
            self._node_callback.deregister(callback_handle)
        else:
            raise ValueError(f'internal error : {obj} is not a supported type')

        # remove from registry
        try:
            del self.registry[callback_handle]
        except KeyError:
            raise BaseException('internal error: handle is not in registry')

    def _is_handle_in_registry(self, callback_handle):
        try:
            self.registry[callback_handle]
        except KeyError:
            return False
        return True


class _DeviceCallback:

    @staticmethod
    def register(device, callback_function, *args, **kwargs):
        args_and_kwargs = [args, kwargs]
        registry_entry = {
            'obj': device,
            'callback_function': callback_function,
            'args_and_kwargs': args_and_kwargs
        }
        # xlayer call
        callback_handle, to_add_to_registry_entry = device._xdev.xDeviceRegisterImageCallback(
            callback_function,
            args_and_kwargs)
        registry_entry.update(to_add_to_registry_entry)
        return {callback_handle: registry_entry}

    @staticmethod
    def deregister(device, callback_handle):
        try:
            device._xdev.xDeviceDeregisterImageCallback(callback_handle)
        except OSError as os_error:
            if 'exception: access violation reading' in str(os_error):
                raise ValueError('handle is registered for a destroyed device. Please '
                                 'deregister the handle before destroying the device')
            else:
                raise os_error


class _NodeCallback:

    def __init__(self, _xcallback):
        self.xcb = _xcallback

    def register(self, node, callback_function, *args, **kwargs):
        '''
        # c callback and arguments are saved to keep a reference
        # (reference count > 0 ) so the data exists when the callback is
        # made and is not overwritten when the user registers a second callback.
        '''
        args_and_kwargs = [args, kwargs]
        registry_entry = {
            'obj': node,
            'callback_function': callback_function,
            'args_and_kwargs': args_and_kwargs
        }
        # xlayer call
        callback_handle, to_add_to_registry_entry = self.xcb.xCallbackRegister(node.xnode.hxnode.value,
                                                                               callback_function,
                                                                               args_and_kwargs)
        registry_entry.update(to_add_to_registry_entry)
        return {callback_handle: registry_entry}

    def deregister(self, callback_handle):
        try:
            self.xcb.xCallbackDeregister(callback_handle)
        except OSError as os_error:
            if 'exception: access violation reading' in str(os_error):
                raise ValueError('handle is registered for a node in a destroyed device. Please '
                                 'deregister the handle before destroying the device')
            else:
                raise os_error


###############################################################################
#
# Callback Decorators
#
###############################################################################


class _CallbackFunction:
    '''
    a decorator to convert a function to a recognizable arena_api
    callback function. A function decorated with this can be used
     with ``callback_register()``. List of available decorators:\n
    - ``Device`` callbacks:
        - ``@callback_function.device.on_buffer`` :
            decorates a function to be used for a callback when a buffer
            arrives to the device. A function decorated with this must have
            the following signature ``my_callback(buffer , *args, **kwargs)``
            where buffer is mandatory parameter.
    - ``Node`` callbacks:
        - ``@callback_function.node.on_update`` :
            decorates a function to be used for a callback when the node
            --which callback is registered on-- gets invalidated. A function
            decorated with this must have the following signature
            ``my_callback(node , *args, **kwargs)`` where node
            is mandatory parameter.
    :Warning:
    - Import the instance ``callback_function`` not the class it self.
    *New in version 1.7.0*

    '''
    __singleton = None
    __run_init = True

    def __new__(cls, *args, **kwargs):

        if not cls.__singleton:
            cls.__singleton = super(_CallbackFunction, cls).__new__(
                cls, *args, **kwargs)
        return cls.__singleton

    def __init__(self):

        if not self.__run_init:
            return
        else:
            self.__run_init = False

        self.device = _DeviceCallbackFunctionDecorator()
        self.node = _NodeCallbackFunctionDecorator()
        self.supported_decorators = self.device.supported_decorators + \
            self.node.supported_decorators

    def __getattr__(self, item):
        raise AttributeError(f'\'{item}\' is not supported. Try :'
                             f'\n {self.supported_decorators}')


class _DeviceCallbackFunctionDecorator:
    supported_decorators = ('callback_function.device.on_buffer',)

    def __getattr__(self, item):
        raise AttributeError(f'\'{item}\' is not supported. Try :'
                             f'\n {self.supported_decorators}')

    @staticmethod
    def on_buffer(callback_function):
        callback_function._decorator = f'callback_function.device.on_buffer'

        @wraps(callback_function)
        def wrapper_func(buffer_, user_data):
            buf = _buffer._Buffer(buffer_)

            var = cast(user_data, py_object).value
            positional_args = var[0]
            keyword_args = var[1]

            return callback_function(buf, *positional_args, **keyword_args)

        return wrapper_func


class _NodeCallbackFunctionDecorator:
    supported_decorators = ('callback_function.node.on_update',)

    def __getattr__(self, item):
        raise AttributeError(f'\'{item}\' is not supported. Try :'
                             f'\n {self.supported_decorators}')

    @staticmethod
    def on_update(callback_function):
        callback_function._decorator = f'callback_function.node.on_update'

        @wraps(callback_function)
        def wrapper_func(node_, user_data):
            var = cast(user_data, py_object).value

            base_node = _Node(node_)
            node = _node_helpers.cast_from_general_node_to_specific_node_type(
                base_node)

            positional_args = var[0]
            keyword_args = var[1]

            return callback_function(node, *positional_args, **keyword_args)

        return wrapper_func


###############################################################################
#
# Instances
#
###############################################################################

# new in 1.7.0
callback = _Callback()
callback_function = _CallbackFunction()
