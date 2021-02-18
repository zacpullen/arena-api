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

import math  # math.inf
import socket  # converts int ip to 'xxx,xxx,xxx' format
import struct  # converts int ip to 'xxx,xxx,xxx' format

from arena_api import buffer as _buffer
from arena_api import _nodemap as _nodemap
from arena_api._xlayer.xarena._xdevice import _xDevice
from arena_api._xlayer.xarena.arenac_defaults import \
    AC_INFINITE as _AC_INFINITE
from arena_api._xlayer.xarena.arenac_defaults import \
    GET_BUFFER_TIMEOUT_MILLISEC_DEFAULT as _GET_BUFFER_TIMEOUT_MILLISEC_DEFAULT
from arena_api._xlayer.xarena.arenac_defaults import \
    NUM_OF_BUFFERS_DEFAULT as _NUM_OF_BUFFERS_DEFAULT
from arena_api._xlayer.xarena.arenac_defaults import \
    WAIT_ON_EVENT_TIMEOUT_MILLISEC_DEFAULT as \
    _WAIT_ON_EVENT_TIMEOUT_MILLISEC_DEFAULT


class Device():

    '''
    Devices constitute the core of the ``Arena SDK``, providing the means to
    interacting with physical devices. They are created and
    destroyed via ``system.create_device()``
    and ``system.destroy_device()``.

    A device manages its images and chunk data , events,
    and node maps by:\n
    - starting and stopping the stream (``device.start_stream()``,\
    ``device.stop_stream()``),\n
    - retrieving and requeuing image buffers and chunk data buffers\
    (``device.get_buffer()``, ``device.requeue_buffer()``). ``Buffer``\
    instances could contain image data only or image data appended\
    with chunkdata,\n
    - handling events (``device.initialize_events()``,\
    ``device.deinitialize_events()``, ``device.wait_on_event()``),\n
    - and providing access to its node maps (``tl_device_nodemap``,\
    ``tl_stream_nodemap`` , ``tl_interface_nodemap``),\n

    :warning:\n
    - Must be destroyed; otherwise, memory will leak.
    - You may not import ``Device`` nor create it directly. Instead, use \
    ``system.create_device()`` to retreave ``Device`` instances.

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------
    # TODO SFW-2115

    def __init__(self, hxdevice):
        self._xdev = _xDevice(hxdevice)
        self.__number_of_buffers_when_stream_started = -1
        self.__GET_BUFFER_TIMEOUT_MILLISEC = _GET_BUFFER_TIMEOUT_MILLISEC_DEFAULT
        self.__WAIT_ON_EVENT_TIMEOUT_MILLISEC = _WAIT_ON_EVENT_TIMEOUT_MILLISEC_DEFAULT
        self.__DEFAULT_NUM_BUFFERS = _NUM_OF_BUFFERS_DEFAULT

    def __str__(self):

        ip_int = self.tl_device_nodemap.get_node('GevDeviceIPAddress').value
        ip = socket.inet_ntoa(struct.pack("!I", ip_int))

        mac_int = self.tl_device_nodemap.get_node('GevDeviceMACAddress').value
        mac_hex = "{:012x}".format(mac_int)
        mac_str = ":".join(mac_hex[i:i+2] for i in range(0, len(mac_hex), 2))

        model_name = self.nodemap.get_node('DeviceModelName').value
        user_id_name = self.tl_device_nodemap.get_node('DeviceUserID').value

        return f'{mac_str, model_name, user_id_name, ip}'

    # DEFAULT_NUM_BUFFERS -------------------------------------------------

    def __get_DEFAULT_NUM_BUFFERS(self):
        return self.__DEFAULT_NUM_BUFFERS

    def __set_DEFAULT_NUM_BUFFERS(self, value):

        if not isinstance(value, int):
            raise TypeError(f'expected int value instead of '
                            f'{type(value).__name__}')
        elif value < 1:
            raise ValueError(f'DEFAULT_NUM_BUFFERS must be set'
                             f' to a value > 0')
        else:
            self.__DEFAULT_NUM_BUFFERS = value

    DEFAULT_NUM_BUFFERS = property(
        __get_DEFAULT_NUM_BUFFERS,
        __set_DEFAULT_NUM_BUFFERS)

    '''
    Number of internal buffers to use in the acquisition engine. The
    default value is ``10``, and the minimum accepted value is ``1``.

    :getter: Returns the current default number of buffers.
    :setter: Sets the default number of buffers.
    :type: int

    The streaming underlying engine has an input and an output queue.
    The size of both queues is determined by
    ``device.DEFAULT_NUM_BUFFERS``.

    :warning:\n
    - It is recommended to keep this value relatively small.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''

    # GET_BUFFER_TIMEOUT_MILLISEC -----------------------------------------

    def __get_GET_BUFFER_TIMEOUT_MILLISEC(self):
        return self.__GET_BUFFER_TIMEOUT_MILLISEC

    def __set_GET_BUFFER_TIMEOUT_MILLISEC(self, value):
        is_int = isinstance(value, int)
        is_inf = math.isinf(value)
        if not is_int and not is_inf:
            raise TypeError(f'expected int or math.inf instead of '
                            f'{type(value).__name__}')
        elif value < 0:
            raise ValueError(f'GET_BUFFER_TIMEOUT_MILLISEC must be set'
                             f' to a value >= 0 or math.inf')
        else:
            self.__GET_BUFFER_TIMEOUT_MILLISEC = value

    GET_BUFFER_TIMEOUT_MILLISEC = property(
        __get_GET_BUFFER_TIMEOUT_MILLISEC,
        __set_GET_BUFFER_TIMEOUT_MILLISEC)
    '''
    Maximum time to wait for a buffer. The default value is
    ``math.inf``, and the minimum accepted value is ``0``.

    :getter: Returns the current default number of buffers.
    :setter: Sets the default number of buffers.
    :type: int , float infinity

    The value zero will return a buffer(s) if there is a ready buffer(s)
    in the output queue, otherwise, a ``TimeoutError`` will rise.
    ``device.GET_BUFFER_TIMEOUT_MILLISEC`` initial value is ``math.inf``
    which is a float; however ``device.GET_BUFFER_TIMEOUT_MILLISEC`` only
    accepts ``int`` or ``math.inf`` values.

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''

    # WAIT_ON_EVENT_TIMEOUT_MILLISEC --------------------------------------

    def __get_WAIT_ON_EVENT_TIMEOUT_MILLISEC(self):
        return self.__WAIT_ON_EVENT_TIMEOUT_MILLISEC

    def __set_WAIT_ON_EVENT_TIMEOUT_MILLISEC(self, value):
        is_int = isinstance(value, int)
        is_inf = math.isinf(value)
        if not is_int and not is_inf:
            raise TypeError(f'expected int or math.inf instead of '
                            f'{type(value).__name__}')
        elif value < 0:
            raise ValueError(f'WAIT_ON_EVENT_TIMEOUT_MILLISEC must be set'
                             f' to a value >= 0 or math.inf')
        else:
            self.__WAIT_ON_EVENT_TIMEOUT_MILLISEC = value

    WAIT_ON_EVENT_TIMEOUT_MILLISEC = property(
        __get_WAIT_ON_EVENT_TIMEOUT_MILLISEC,
        __set_WAIT_ON_EVENT_TIMEOUT_MILLISEC)

    '''
    Maximum time to wait for an event to occur. The default value is
    ``math.inf``, and the minimum accepted value is ``0``.

    :getter: Returns the current default timeout to wait for an event.
    :setter: Sets the default timeout to wait for an event.
    :type: int , float infinity

    The value zero will return an event if there is a ready event
    in the events output queue, otherwise, a ``TimeoutError`` will rise.
    ``device.WAIT_ON_EVENT_TIMEOUT_MILLISEC`` initial value is ``math.inf``
    which is a float; however ``device.WAIT_ON_EVENT_TIMEOUT_MILLISEC`` only
    accepts ``int`` or ``math.inf`` values.
    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''

    # start_stream --------------------------------------------------------

    def start_stream(self, number_of_buffers=None):
        '''
        Causes the device to begin streaming image/chunk data buffers.
        It must be called before image or chunk data buffers are
        retrieved via ``device.get_buffer()`` otherwise, a ``BaseException``
        will rise.

        **Args**:
            number_of_buffers :\n
            \tNumber of internal buffers to use in the acquisition engine.\
            The default value is ``None``, and the minimum accepted\
            value is ``1``. It can be:\n
                - a positive integer. Relatively small numbers are \
                recommended. Zero or a negative int values will raise\
                ``ValueError`` exception.\n
                - ``None``. This is the default value, which is \
                equivalent to\
                ``device.start_stream(device.DEFAULT_NUM_BUFFERS)``.\n

        **Raises**:
            - ``ValueError`` :
                - ``number_of_buffers`` is zero or a negative intger.
            - ``TypeError`` :
                - ``number_of_buffers`` type is not int.
        **Returns**:
            - None

        Basically, this method prepares and starts the
        underlying streaming engine. The streaming engine primarily
        consists of a number of buffers, an input and an output queue,
        and a worker thread to run off of the main thread.
        All buffers are first placed in the input queue. When a
        buffer reaches its turn, it is filled with data.
        Once complete, it is moved to the output queue.
        At this point a buffer might be retrieved by the user by
        calling ``device.get_buffer()`` and then returned
        to the input queue by calling ``device.requeue_buffer()``.
        More specifically: \n
        - allocates and announces a number of buffers according to\
        the ``number_of_buffers`` parameter.\n
        - pushes all buffers to the input queue.\n
        - opens a stream channel socket.\n
        - configures the destination IP and port on the device.\n
        - fires a dummy packet to help with firewalls.\n
        - requests a test packet to ensure configured packet size is\
        appropriate.\n
        - starts the worker thread and begins listening for packets\
        related to the acquisition engine.\n
        - has the device lock out certain features\
        (e.g. 'Width', 'Height') that cannot be changed during the stream.\n
        - executes the ``AcquisitionStart`` feature in order to have the\
        device start sending packets.\n

        All stream configurations must be completed before starting\
        the stream. This includes, among other things, the buffer\
        handling mode ``StreamBufferHandlingMode`` node found on the\
        stream node map ``device.tl_stream_nodemap``. Setting the\
        buffer handling mode configures what the streaming engine\
        does with buffers as they are filled and moved between\
        queues. There are three modes to choose from:\n
        - ``OldestFirst`` node is the default buffer handling mode.\
        As buffers are filled with data, they get pushed to the back\
        of the output queue. When a buffer is requested\
        ``device.get_buffer()``, the buffer at the front of the queue is\
        returned. If there are no input buffers available, the next\
        incoming buffer is dropped and the lost frame count\
        ``StreamLostFrameCount`` node value is incremented.\n
        - ``OldestFirstOverwrite`` node is similar to ``OldestFirst``\
        except for what happens when there are no input buffers.\
        Instead of dropping a buffer, the oldest buffer in the\
        output queue gets returned to the input queue so that its data\
        can be overwritten.\n
        - ``NewestOnly`` node only ever has a single buffer in the output\
        queue. If a second buffer gets placed into the output\
        queue, the older buffer gets returned to the back of the input\
        queue. If there are no input buffers available, the next image\
        is dropped and the lost frame count ``StreamLostFrameCount``\
        node value is incremented.\n

        There are three ways to start and stop stream:\n
            - as regular function call:
                This way the user has control over when to call\
                ``device.stop_stream()``. For example:\n
                >>> device.start_stream()
                >>> # do something like grab a buffer
                >>> buffer = device.get_buffer()
                >>> device.requeue_buffer(buffer)
                >>> # do more stuff
                >>> device.stop_stream()

            - as a context manager:\n
                This will call ``device.stop_stream()`` automatically\
                when the context manager exits. For example:\n
                >>> with device.start_stream():
                >>>     # do something like grab a buffer
                >>>     buffer = device.get_buffer()
                >>>     device.requeue_buffer(buffer)
                >>>     # do more stuff
                >>> # device.stop_stream() is already call at this point

            - as regular function call but without calling stopping the\
            stream:\n
                This will call ``device.stop_stream()``\
                automatically when ``system.destroy_device()`` is called.\
                For example:\n
                >>> from arena_api.system import system
                >>> devices = system.create_device()
                >>> my_device = devices[0]
                >>> device.start_stream()
                >>> # do something like grab a buffer
                >>> buffer = device.get_buffer()
                >>> device.requeue_buffer(buffer)
                >>> system.destory_device(my_device)
                >>> # device.stop_stream() is already call at this point

        :warning:\n
        - Stream must already be configured prior to call.
        - Updates write access to certain nodes.
        - May only be called once per stream without stopping.
        - Minimum number of buffers is ``1``.

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''

        # input checks ----------------------------------------------------

        if number_of_buffers is None:
            number_of_buffers = self.DEFAULT_NUM_BUFFERS

        if not isinstance(number_of_buffers, int):
            raise TypeError(f'expected int instead of'
                            f' {type(number_of_buffers).__name__}')

        if number_of_buffers < 1:
            raise ValueError(f'number_of_buffers must be > 0')

        # save the member functions to be used so they can be used
        # in the cntxmngr
        device_start_stream = self._xdev.xDeviceStartStreamNumBuffersAndFlags
        device_stop_stream = self.stop_stream
        # dont move into the __init__ of the cntxmngr because self will
        # refer to the cntxmngr class instead of device
        self.__number_of_buffers_when_stream_started = number_of_buffers

        class start_stream_cntxmngr():

            def __init__(self, number_of_buffer):
                # code that will be used if this function is called
                # regardless of the way it is called
                device_start_stream(number_of_buffers)

            def __enter__(self):
                # code that will execute only if the function is
                # used with 'with' statement
                pass

            def __exit__(self, *exc):
                # code that will execute only if the function is
                # used with 'with' statement
                device_stop_stream()

        return start_stream_cntxmngr(number_of_buffers)

    # stop_stream ---------------------------------------------------------

    def stop_stream(self):
        '''
        Stops the device from streaming image/chunk data buffers and
        cleans up the stream. Reverses the set up of the stream:\n
        - stops the worker thread.\n
        - shuts down the stream channel socket.\n
        - executes the ``AcquisitionStop`` feature in order to stop\
        the device from sending packets.\n
        - has the device unlock features that had been locked\
        for streaming (e.g. ``Width``, ``Height``).\n
        - revokes all buffers and cleans up their allocated memory\n

        **Args**:
            - ``None``
        **Returns**:
            - ``None``

        Buffers used internally are allocated when the stream has
        started ``device.start_stream()`` and deallocated when it
        has stopped ``device.stop_stream()``. If an image has been
        retrieved ``device.get_buffer()``, it can be copied
        ``BufferFactory.copy()`` or saved before stopping the
        stream. If image data were accessed after stopping the
        stream, the memory would be deallocated and the behavior
        undefined.\n

        :warning:\n
        - Is an optional to call. Check ``device.start_stream()``\
        documentation.\n
        - Updates write access to certain nodes.\n
        - Disallows retrieval of image/chunk data from device.\n
        - Deallocates image/chunk data that has not been copied to\
        memory or disk.\n


        **------------------------------------------------------------------**\
        **-------------------------------------------------------------------**
        '''
        if self.__number_of_buffers_when_stream_started != -1:
            self._xdev.xDeviceStopStream()
            self.__number_of_buffers_when_stream_started = -1

    # get_buffer ----------------------------------------------------------

    def __throw_if_get_buffer_is_called_before_start_stream(self):
        if self.__number_of_buffers_when_stream_started == -1:
            raise BaseException(
                f'device.start_stream() must be called'
                f'before device.get_buffer()')

    def __check_get_buffer_parameter_number_of_buffers(self,
                                                       number_of_buffers):

        # check type
        if not isinstance(number_of_buffers, int):
            raise TypeError(f'expected int instead of '
                            f'{type(number_of_buffers).__name__}')

        # check value
        if (number_of_buffers <= 0) or \
           (number_of_buffers > self.__number_of_buffers_when_stream_started):
            raise ValueError(
                f'\nnum_of_buffers = {number_of_buffers}\n'
                f'start_stream was called with '
                f'{self.__number_of_buffers_when_stream_started}\n'
                f'number of buffers must be > 0 and <= '
                f'{self.__number_of_buffers_when_stream_started}')

    def __check_get_buffer_parameter_timeout(self, timeout):

        # check types
        if timeout is None:
            timeout = self.GET_BUFFER_TIMEOUT_MILLISEC

        is_int = isinstance(timeout, int)
        is_inf = math.isinf(timeout)
        if not is_int and not is_inf:
            raise TypeError(f'expected int or math.inf instead of '
                            f'{type(timeout).__name__}')

        if timeout < 0:
            raise ValueError('timeout must be >= 0 or math.inf')

        if timeout is math.inf:
            timeout = _AC_INFINITE

        return timeout

    def get_buffer(self, number_of_buffers=1, timeout=None):
        '''
        Retrieves, from the device, a ``Buffer`` instance from the\
        buffer output queue. The function must be called after the\
        stream has started ``device.start_stream()``\
        and before the stream has stopped ``device.stop_stream()``.\
        Retrieved buffers must be requeued ``device.requeue_buffer()``.\n

        **Args**:\n
            number_of_buffers:\n
                an ``int`` value that represents the number of\
                ``Buffer`` instances to retrieve. The default value\
                is ``1``. Zero or a negative integer will cause a \
                ``ValueError`` to throw.\n
            timeout: can be\n
                - a positive ``int`` value that represents\
                the maximum time, in millisec, to wait for a buffer. \
                The value zero will return a buffer(s) if there is a\
                ready buffer(s) \in the output queue, otherwise, a \
                ``TimeoutError`` will rise.\n
                - ``None``. This is the parameter's default value. The\
                function will use ``device.GET_BUFFER_TIMEOUT_MILLISEC``\
                value instead --which has a default value of ``10000``.\n

        **Raises**:\n
        - ``ValueError`` :\n
            - ``number_of_buffers`` parameter is less than ``1`` \
            or greater than the number of buffers with which the stream\
            has started.\n
            - ``timeout`` is a negative integer.
        - ``TypeError`` :\n
            - ``number_of_buffers`` type is not ``int``.
            - ``timeout`` type is not ``int``
        - ``TimeoutError``:\n
            - ``ArenaSDK`` is not able to get a buffer(s) before \
            the timeout expiration.
        - ``BaseException`` :\n
            - ``device.get_buffer()`` is called before starting the\
            stream ``device.start_stream()``.
            - if the returned buffer list size is < ``number_of_buffers``

        **Returns**:\n
        - a ``Buffer`` instance, to manage the next buffer in the\
        output queue, if ``number_of_buffers`` is ``1``.\n
        - a list of ``Buffer`` instances, to manage the next buffers\
        in the output queue, The list size is equal to\
        ``number_of_buffers``.\n

        Retrieving multiple buffers by setting ``number_of_buffers``\
        to > ``1``, is the same as calling ``device.get_buffer()``\
        in a for loop and getting one buffer in each iteration.\n

        Retrieving multiple buffers will use the same timeout to wait\
        for each buffer.\n

        The data returned may represents different payload types:\n
        - an image without chunk,\n
        - an image with chunk, or\n
        - just chunk data.\n

        Note that a buffer of chunk data payload type may contain\
        image data, but cannot be cast to an image because the image\
        data is treated as a chunk.\n

        The payload type can be retrieved via ``Buffer.payload_type``,\
        which returns an enum ``enums.PayloadType``.\n

        When called, ``device.get_buffer()`` checks the output queue\
        for image/chunk data, grabbing the first buffer(s) in the queue.\
        If nothing is in the output queue, the call will wait\
        until something arrives. If nothing arrives before expiration\
        of the timeout, a ``TimeoutError`` is thrown.

        This method is a blocking call. If it is called with a timeout of\
        20 seconds and nothing arrives in the output queue, then\
        its thread will be blocked for the full 20 seconds.\
        However, as the timeout is a maximum, as soon as\
        something arrives in the output queue, it will be returned,\
        not waiting for the full timeout. A timeout \
        value of ``0`` ensures the call will not block, throwing instead\
        of waiting if nothing is in the output queue.\n

        Best practices recommends that buffers be requeued\
        ``device.requeue_buffer()`` as soon as they are no longer needed.\
        If image data is needed for a longer period of\
        time (i.e. for processing), it is recommended to copy \
        the data ``BufferFactory.copy()`` and requeue the buffer.


        ** -------------------------------------------------\n
        ``Device.start_stream()`` number of buffers parameter
                               VS
        ``Device.get_buffer()`` number of buffers parameter\n
        ------------------------------------------------- **

        A user can start stream with 30 buffers:

             buffer available without requeue           = 30 buffers
             buffers taken out and needs to be requeued = 0  buffers

        - user calls ``Device.get_buffer()`` with no arguments to get one buffer then:

             buffer available without requeue           = 29 buffers
             buffers taken out and needs to be requeued = 1 buffer

        - user calls ``Device.requeue_buffer(buffer)`` passing one buffer:

             buffer available without requeue           = 30 buffers
             buffers taken out and needs to be requeued = 0 buffers

        - user calls ``Device.get_buffer(5)`` to get 5 buffers then:

             buffer available without requeue           = 25 buffers
             buffers taken out and needs to be requeued = 5 buffer

        - user calls ``Device.requeue_buffer(list_of_4_buffers)`` then:

             buffer available without requeue           = 29 buffers
             buffers taken out and needs to be requeued = 1 buffers

        - user calls ``Device.get_buffer(29)`` to get 29 buffers then:

             buffer available without requeue           = 0 buffers
             buffers taken out and needs to be requeued = 30 buffer

        - user calls ``Device.get_buffer(_)`` with any number of buffers then:

             the call to to the function will wait forever for a
             buffer to be requeued :(

        :warning:\n
        - Does not guarantee valid data.\n
        - ``Buffer`` instance(s) should be requeued\
        ``device.requeue_buffer()``.\n


        **-----------------------------------------------------------------** \
        **-------------------------------------------------------------------**
        '''

        self.__throw_if_get_buffer_is_called_before_start_stream()

        # input checks
        self.__check_get_buffer_parameter_number_of_buffers(number_of_buffers)
        timeout = self.__check_get_buffer_parameter_timeout(timeout)

        all_buffers = []
        for _ in range(number_of_buffers):
            hxbuffer = self._xdev.xDeviceGetBuffer(timeout)
            buf = _buffer._Buffer(hxbuffer)
            all_buffers.append(buf)

        if number_of_buffers == 1:
            return all_buffers[0]
        else:
            return all_buffers

    # ---------------------------------------------------------------------
    def __check_requeue_buffer_list_input(self, buffers_list):

        if len(buffers_list) == 0:
            raise ValueError(
                'requeue_buffer argument can not be an empty list')

        for buf in buffers_list:
            is_instance = isinstance(buf, _buffer._Buffer)
            if not is_instance:
                raise TypeError('argument list has element(s) that is not '
                                'of Buffer type')

    def requeue_buffer(self, buffers):
        '''
        Relinquishes control of a buffer(s) back to Arena. \
        It must be called after a buffer(s) has been retrieved \
        ``device.get_buffer()``.\n

        **Args**:
            buffers:\n
                the buffer(s) to requeue. It can be:\n
                - a list of ``Buffer`` instances\n
                - a ``Buffer`` instance.\n

        **Raises**:\n
        - ``ValueError`` :\n
            - ``buffers`` is an empty list.\n
        - ``TypeError`` :\n
            - ``buffers`` is not a list of ``Buffer`` nor a ``Buffer`` \
            instance.\n
            - ``buffers`` is a list but one or more element is not\
            of ``Buffer`` type.\n

        **Returns**:\n
        - ``None``.\n

        When called, ``device.get_buffer()`` deallocates any lazily\
        instantiated memory and returns the internal buffer\
        to the acquisition engine's input queue, where it can be\
        filled with new data. If enough buffers have been removed from\
        the acquisition engine (i.e. not requeued), it is possible to
        starve the acquisition engine. If this happens and depending\
        on the buffer handling mode ``StreamBufferHandlingMode`` node,\
        data may start being dropped or buffers may start being recycled.\n

        Best practices recommends that buffers be requeued as soon\
        as they are no longer needed. If image data is needed for\
        a longer period of time (i.e. for processing), it is \
        recommended to copy the data ``BufferFactory.copy()`` \
        and requeue the buffer.\n

        It is important to only call ``device.requeue_buffer()`` \
        on buffers retrieved from a ``Device`` instance , and\
        not on images created through ``BufferFactory.copy()``.\n

        :warning:\n
        - Used only on buffers retrieved from a device, not on \
        buffers created through the buffer factory ``BufferFactory``.\n

        **------------------------------------------------------------------**\
        **-------------------------------------------------------------------**
        '''
        if isinstance(buffers, list):
            self.__check_requeue_buffer_list_input(buffers)
            for index in range(len(buffers)):
                self._xdev.xDeviceRequeueBuffer(
                    buffers[index].xbuffer.hxbuffer.value)

        elif isinstance(buffers, _buffer._Buffer):
            self._xdev.xDeviceRequeueBuffer(buffers.xbuffer.hxbuffer.value)
        else:
            raise TypeError(f'expected Buffer or list of Buffers type.'
                            f'{type(buffers).__name__} type was passed')

    # ---------------------------------------------------------------------
    # TODO SFW-2178
    def initialize_events(self):
        '''
        Causes the underlying events engine to start listening for\
        events. It must be called before waiting on events\
        ``device.wait_on_event()``. The event infrastructure must be\
        turned off ``device.deinitialize_events()`` when no longer needed.\n

        **Args**:\n
        - ``None``\n

        **Returns**:\n
        - ``None``.\n

        The underlying events engine works very similarly to the \
        acquisition engine, except that event data is processed \
        instead of image data. It consists of 100 buffers, an input \
        and an output queue, and event registration information. \
        When an event fires, the events engine takes an event buffer\
        from the input queue, stores all relevant data, and\
        places it in the output queue. When ``device.wait_on_event()`` \
        is called, the engine takes the buffer from the output queue, \
        processes its data, and returns it to the input queue.\n

        More specifically, ``device.initialize_events()``:\n
        - allocates and registers 100 buffers for the events engine\
        - places all buffers into the input queue.\n
        - opens a message channel socket.\n
        - configures the IP and port, and sets the packet size.\n
        - fires a dummy packet to help with firewalls.\n
        - starts the worker thread listening for event packets.\n

        Events are transmitted from the device through the \
        ``GigE Vision`` message channel. Arena processes event data\
        internally, which it attaches to ``device.tl_device_nodemap`` \
        using a ``GenApi::EventAdapter``. The appropriate nodes are \
        then updated in the node map. It can be helpful to incorporate\
        callbacks to be notified when these events occur.

        :warning:\n
        - Event infrastructure must be deinitialized via \
        ``device.deinitialize_events``\n

        **------------------------------------------------------------------**\
        **-------------------------------------------------------------------**
        '''
        self._xdev.xDeviceInitializeEvents()

    # ---------------------------------------------------------------------

    def deinitialize_events(self):
        '''
        Stops the underlying events engine from listening for \
        messages, shutting it down and cleaning it up.\
        It should be called only after the events infrastructure \
        has been initialized ``device.initialize_events()`` and after\
        all events have been processed ``device.wait_on_event()``.\n

        **Args**:\n
        - ``None``.\n

        **Returns**:\n
        - ``None``.\n

        Roughly speaking, ``device.deinitialize_events()`` takes all \
        necessary steps to undoing and cleaning up the event\
        infrastructure's initialization. This includes:\n
        - stop the listening thread\n
        - closes the message channel socket\n
        - unregisters all event buffers and deallocates their memory\n

        :warning:\n
        - Event infrastructure must be deinitialized.\n
        - Stops events processing.\n
        - Deallocates event data that has not yet been processed.\n

        **------------------------------------------------------------------**\
        **-------------------------------------------------------------------**
        '''

        self._xdev.xDeviceDeinitializeEvents()

    # ---------------------------------------------------------------------
    def __check_wait_on_event_input_timeout(self, timeout):
        # non blocking call so timeout can be zero
        # input checks
        if timeout is None:
            timeout = self.WAIT_ON_EVENT_TIMEOUT_MILLISEC

        is_int = isinstance(timeout, int)
        is_inf = math.isinf(timeout)
        if not is_int and not is_inf:
            raise TypeError(f'expected int or math.inf instead of '
                            f'{type(timeout).__name__}')

        if timeout < 0:
            raise ValueError('timeout must be >= 0 or math.inf')

        if timeout is math.inf:
            timeout = _AC_INFINITE

        return timeout

    def wait_on_event(self, timeout=None):
        '''
        Waits for an event to occur in order to process its
        data. It must be called after the event infrastructure has been
        initialized ``device.initialize_events()`` and before it is
        deinitialized ``device.deinitialize_events()``

        **Args**:\n
        - timeout: can be\n
            - a positive ``int`` value that represents\
            the maximum time, in millisec, to wait for an event.\
            The value zero will return an event if there is a\
            ready event in the output queue, otherwise, a \
            ``TimeoutError`` will rise.\n
            - ``None``. This is the parameter's default value. The\
            function will use ``device.WAIT_ON_EVENT_TIMEOUT_MILLISEC``\
            value instead --which has a default value of ``10000``.\n

        **Raises**:\n
        - ``TimeoutError``:\n
            - ``ArenaSDK`` is not able to get an event before \
            the timeout expiration\n

        **Returns**:\n
        - ``None``.\n

        Event processing has been designed to largely abstract away its
        complexities. When an event occurs, the data is stored\
        in an event buffer and placed on the output queue. This\
        method causes the data to be processed, updating all relevant\
        nodes appropriately. This is why ``device.wait_on_event()`` \
        does not return any event data; when the data is processed, \
        nodes are updated, which can then be queried for\
        information through the node map. This is also why callbacks\
        work so well with the events infrastructure; they provide a\
        method of accessing nodes of interest as they change.\n

        When called, ``device.wait_on_event()`` checks the output \
        queue for event data to process, grabbing the first buffer \
        from the queue. If nothing is in the output queue, the call \
        will wait until an event arrives. If nothing arrives before \
        expiration of the timeout, a GenICam::TimeoutException is thrown.\n

        This method is a blocking call. If it is called with a\
        timeout of 20 seconds and nothing arrives in the output queue, \
        then its thread will  be blocked for the full 20 seconds. \
        However, as the timeout is a maximum, when an event arrives in\
        the output queue, the event will process, not waiting for the \
        full timeout. A timeout value of 0 ensures the call will not\
        block, throwing instead of waiting if nothing is in the\
        output queue.\n

        :warning:\n
        - Event data processed internally.

        **------------------------------------------------------------------**\
        **-------------------------------------------------------------------**
        '''
        timeout = self.__check_wait_on_event_input_timeout(timeout)

        self._xdev.xDeviceWaitOnEvent(timeout)

    # ---------------------------------------------------------------------

    def __get_nodemap(self):
        hxnodemap = self._xdev.xDeviceGetNodeMap()
        return _nodemap.Nodemap(hxnodemap)

    nodemap = property(__get_nodemap)
    '''
    used to access a device's complete feature set of nodes.\n

    :getter: Returns main node map for the device.\n
    :type: ``arena_api._nodemap.Nodemap`` instance.\n

    The node map is built from XMLs stored on the device itself. \
    The XML is downloaded and parsed before constructing and \
    initializing the node map. This node map describes and provides\
    access to all device features, and may vary from device to\
    device. Lucid products conform to the SFNC 2.3 specification.\
    Note that both chunk data and event data are updated on\
    this node map.\n

    -----------------------------------------------------------------------
    Retrieves this node map without doing anything to initialize, \
    manage, or maintain it. This node map is initialized when the \
    device is created ``system.create_device()`` and deinitialized\
    when the device is destroyed ``system.destroy_device()``.\
    All available nodes can be viewed in ``ArenaView`` software \
    or run ``py_nodemaps_exploration.py``.\n

    ``arena_api`` package provides access to five different node maps that\
    can be splitted into two groups:\n
        - Software:\n
            The following node maps describe and provide access\
            to information and settings through the software rather\
            than the device:\n
                - ``system.tl_system_nodemap``\n
                - ``system.tl_interface_nodemap``\n
                - ``device.tl_device_nodemap``\n
                - ``device.tl_stream_nodemap``\n
                - ``device.tl_interface_nodemap``\n
        - Device:\n
            The following node maps describe and provide access to\
            information and settings through the device:\n
                - ``device.nodemap``\n

    **device.tl_device_nodemap vs device.nodemap**:\n
        The most noticeable difference between the two device node maps\
        is that the ``GenTL`` device node map ``device.tl_device_nodemap`` \
        has only a small set of features compared to the main node map \
        ``device.nodemap``. There are a few features that overlap. \
        For example, the difference between retrieving the serial number\
        ``DeviceSerialNumber`` is that using the main node map queries\
        the camera directly whereas the ``GenTL`` node map queries a set of \
        information cached at device creation. The result, however, \
        should be the same. Basically, the ``GenTL`` node map queries the \
        software for information whereas the main node map queries\
        the device.\n
    -----------------------------------------------------------------------

    :warning:\n
    - Provides access to main node map ``device.nodemap``, not to be \
    confused with the ``GenTL`` device node map ``device.tl_device_nodemap``.

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''

    # ---------------------------------------------------------------------

    def __get_tl_device_nodemap(self):
        hxnodemap = self._xdev.xDeviceGetTLDeviceNodeMap()
        return _nodemap.Nodemap(hxnodemap)

    tl_device_nodemap = property(__get_tl_device_nodemap)
    '''
    used to access a subset of cached device related nodes.\n

    :getter: Returns ``GenTL`` node map for the device\n
    :type: ``arean_api._nodemap.Nodemap`` instance.\n

    Nodes in this node map include nodes related to:\n
       - device discovery information.\n
       - GigE Vision IP configuration information.\n
       - the ability to select streams.\n

    -----------------------------------------------------------------------
    Retrieves this node map without doing anything to initialize, \
    manage, or maintain it. This node map is initialized when the \
    device is created ``system.create_device()`` and deinitialized\
    when the device is destroyed ``system.destroy_device()``.\
    All available nodes can be viewed in ``ArenaView`` software \
    or run ``py_nodemaps_exploration.py``.\n

    ``arena_api`` package provides access to five different node maps that\
    can be splitted into two groups:\n
        - Software:\n
            The following node maps describe and provide access\
            to information and settings through the software rather\
            than the device:\n
                - ``system.tl_system_nodemap``\n
                - ``system.tl_interface_nodemap``\n
                - ``device.tl_device_nodemap``\n
                - ``device.tl_stream_nodemap``\n
                - ``device.tl_interface_nodemap``\n
        - Device:\n
            The following node maps describe and provide access to\
            information and settings through the device:\n
                - ``device.nodemap``\n

    **device.tl_device_nodemap vs device.nodemap**:\n
        The most noticeable difference between the two device node maps\
        is that the ``GenTL`` device node map ``device.tl_device_nodemap`` \
        has only a small set of features compared to the main node map \
        ``device.nodemap``. There are a few features that overlap. \
        For example, the difference between retrieving the serial number\
        ``DeviceSerialNumber`` is that using the main node map queries\
        the camera directly whereas the ``GenTL`` node map queries a set of \
        information cached at device creation. The result, however, \
        should be the same. Basically, the ``GenTL`` node map queries the \
        software for information whereas the main node map queries\
        the device.\n
    -----------------------------------------------------------------------

    :warning:\n
    - Provides access to the ``GenTL`` device node map, not to be confused with
        the main device node map ``device.nodemap``.

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''

    # ---------------------------------------------------------------------

    def __get_tl_stream_nodemap(self):
        hxnodemap = self._xdev.xDeviceGetTLStreamNodeMap()
        return _nodemap.Nodemap(hxnodemap)

    tl_stream_nodemap = property(__get_tl_stream_nodemap)
    '''
    used to access stream related nodes.\n

    :getter: Returns ``GenTL`` node map for the stream\n
    :type: ``arena_api._nodemap.Nodemap`` instance.\n

    Nodes in this node map include nodes related to:\n
        - stream ID and type.\n
        - buffer handling mode.\n
        - stream information such as the payload size or whether\
        the device is currently streaming.\n
        - stream statistics such as lost frames, announced buffers,\
        or missed packets.\n

    -----------------------------------------------------------------------
    Retrieves this node map without doing anything to initialize, \
    manage, or maintain it. This node map is initialized when the \
    device is created ``system.create_device()`` and deinitialized\
    when the device is destroyed ``system.destroy_device()``.\
    All available nodes can be viewed in ``ArenaView`` software \
    or run ``py_nodemaps_exploration.py``.\n

    ``arena_api`` package provides access to five different node maps that\
    can be splitted into two groups:\n
        - Software:\n
            The following node maps describe and provide access\
            to information and settings through the software rather\
            than the device:\n
                - ``system.tl_system_nodemap``\n
                - ``system.tl_interface_nodemap``\n
                - ``device.tl_device_nodemap``\n
                - ``device.tl_stream_nodemap``\n
                - ``device.tl_interface_nodemap``\n
        - Device:\n
            The following node maps describe and provide access to\
            information and settings through the device:\n
                - ``device.nodemap``\n
    -----------------------------------------------------------------------


    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------

    def __get_tl_interface_nodemap(self):
        hxnodemap = self._xdev.xDeviceGetTLInterfaceNodeMap()
        return _nodemap.Nodemap(hxnodemap)

    tl_interface_nodemap = property(__get_tl_interface_nodemap)
    '''
    used to access interface related nodes.\n

    :getter: Returns ``GenTL`` node map for the interface\n
    :type: ``arena_api._nodemap.Nodemap`` instance.\n

    Nodes in this node map include nodes related to:\n
       - interface discovery information\n
       - interface IP configuration information\n
       - ability to update and select devices\n
       - device discovery and IP configuration information\n

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
                - ``system.tl_system_nodemap``\n
                - ``system.tl_interface_nodemap``\n
                - ``device.tl_device_nodemap``\n
                - ``device.tl_stream_nodemap``\n
                - ``device.tl_interface_nodemap``\n
        - Device:\n
            The following node maps describe and provide access to\
            information and settings through the device:\n
                - ``device.nodemap``\n
    -----------------------------------------------------------------------

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
