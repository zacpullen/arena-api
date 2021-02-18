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

from arena_api import enums as _enums
from arena_api._node_helpers import \
    cast_from_general_node_to_specific_node_type as \
    _cast_from_general_node_to_specific_node_type
from arena_api._xlayer.xarena._xbuffer import _xBuffer
from arena_api._xlayer.xarena._ximagefactory import _xImagefactory
from arena_api._node import Node as _Node


class _Buffer():
    '''
    Buffers are the most generic form of acquisition engine data \
    retrieved from a device. They are acquired and requeued \
    via ``Device`` instances. Buffers with image data are referred \
    to as image, image data, image buffer.\n

    >>> # retrieving a buffer after starting the stream
    >>> # requeuing it before stopping the stream
    >>> device.start_stream()
    >>> buffer = device.get_buffer()
    >>> device.requeue_buffer(buffer)
    >>> device.stop_stream()

    Buffers can hold image data, chunk data or both. buffer class provides:\n
    - buffer and payload information like \
    payload ``buffer.data``,\
    payload and buffer size ``buffer.size_filled``,\
    ``buffer.buffer_size``, and\
    frame ID ``buffer.frame_id``.\n
    - type information like payload type ``buffer.payload_type`` and\
    whether the payload has image and/or chunk data\
    ``buffer.has_imagedata``, ``buffer.has_chunkdata``.\n
    - error information ``buffer.is_incomplete`` and \
    ``buffer.is_data_larger_than_buffer``.\n
    - size information ``buffer.width``, ``buffer.height``, \
    ``buffer.offset_x``, and ``buffer.offset_y``.\n
    - padding ``buffer.padding_x`` and ``buffer.padding_y``.\n
    - pixel information ``buffer.pixel_format``, ``buffer.pixel_endianness``\n
    , and ``buffer.timestamp_ns``.\n


    # images:
    Image buffers are the most common form of data \
    retrieved in ``_Buffer``.\
    Image data can be copied, and converted via the ``BufferFactory``.\
    It is important to note that images retrieved from the camera must be\
    requeued ``buffer.requeue_buffer()`` whereas images created using the\
    image factory must be destroyed ``BufferFactory.destroy()``.

    # chunk:
    The concept of chunk data is a method of adding extra data (such as CRC,\
    width, height, etc.) to an image. A nuance of this concept is whether the\
    additional information is appended to the back of the image or the image is\
    treated as part of the chunk data. This is important for parsing the data.\
    Lucid devices create chunk data by appending it to the payload.\
    In order to receive chunk data with an image, chunk data must be enabled\
    and configured on node map ``device.nodemap``.\
    Chunk data must first be activated ``ChunkModeActive``. Each specific\
    chunk must then be selected and enabled ``ChunkSelector``\
    and ``ChunkEnable``.\n

    >>> # enabling pixel format chunk data
    >>> device.nodemap.get_node('ChunkModeActive').value = True
    >>> device.nodemap.get_node('ChunkSelector').value = 'PixelFormat'
    >>> # another syntax for get_node is []
    >>> device.nodemap['ChunkEnable'].value = True

    chunk data objects provide the ability to get chunks\
    ``buffer.get_chunk()``. Other wise a exception will rise.\n

    :warning:\n
    - should be requeued; otherwise, acquisition engine may starve.\n
    - properties lazily instantiated if buffer retrieved from device.\n
    - Chunk buffers:\n
        - Should be requeued; same as other buffers\
        ``buffer.requeue_buffer()``.\n
    - Image buffers:\n
        - should be requeued if retrieved from the device.\n
        - must be destroyed if created by the image factory.\n
        - properties of images from the image factory may be unavailable.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''

    def __init__(self, hxbuffer):
        self.xbuffer = _xBuffer(hxbuffer)

    def __str__(self):
        return f'{self.width} {self.height} {str(self.pixel_format)}'
    # ---------------------------------------------------------------------

    def __get_size_filled(self):
        return self.xbuffer.xBufferGetSizeFilled()

    size_filled = property(__get_size_filled)
    '''
    Size of the received payload.\n

    :getter: size of the received payload.\n
    :type: ``int``.\n
    :unit: bytes\n

    Retrieves the size of the payload data, excluding transport layer\
    protocol leaders. The payload data may include image data,\
    chunk data, or both.\n

    **size_filled vs buffer_size**\n
        The size filled is often same as the size of the buffer\
        ``buffer.buffer_size``, but not because they are one and the\
        same. ``buffer.size_filled`` returns the number of bytes\
        received whereas ``buffer.buffer_size`` returns the size of the\
        buffer, which can either be allocated by the user or calculated\
        by Arena ``nodemap.get_node('PayloadSize')``.\n

    **size_filled vs payload_size**\n
        Retrieves the intended size of the payload. This is similar\
        to the retrieved payload size ``buffer.size_filled`` but \
        different in that missed data is included. This returns the same\
        as the SFNC feature by the same name ('PayloadSize').\n

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------

    def __get_payload_size(self):
        return self.xbuffer.xBufferGetPayloadSize()

    payload_size = property(__get_payload_size)
    '''
    Size of the intended payload.\n

    :getter: size of the intended payload.\n
    :type: ``int``.\n
    :unit: bytes.\n

    **payload_size vs size_filled**\n
        Retrieves the intended size of the payload. This is similar\
        to the retrieved payload size ``buffer.size_filled`` but \
        different in that missed data is included. This returns the same\
        as the SFNC feature by the same name ('PayloadSize').\n

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''

    # ---------------------------------------------------------------------

    def __get_buffer_size(self):
        return self.xbuffer.xBufferGetSizeOfBuffer()

    buffer_size = property(__get_buffer_size)

    '''
    Retrieves the size of a buffer.\n

    :getter: retrieves the size of a buffer.\n
    :type: ``int``.\n
    :unit: bytes\n

    The payload size is calculated at the beginning of the stream\
    ``device.start_stream()`` and cannot be recalculated until\
    the stream has stopped ``device.stop_stream()``. Because of this,\
    features that can affect payload size ``Width``, ``Height``,\
    ``PixelFormat`` become unwritable when the stream has started.

    **buffer_size vs size_filled**\n
        The size filled is often same as the size of the buffer\
        ``buffer.buffer_size``, but not because they are one and the\
        same. ``buffer.size_filled`` returns the number of bytes\
        received whereas ``buffer.buffer_size`` returns the size of the\
        buffer, which can either be allocated by the user or calculated\
        by Arena.\n

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''

    # ---------------------------------------------------------------------

    def __get_frame_id(self):
        return self.xbuffer.xBufferGetFrameId()

    frame_id = property(__get_frame_id)
    '''

    Gets the frame ID, a sequential identifier for buffers.

    :getter: gets the frame ID.
    :type: ``int``.\n

    Frame IDs start at ``1`` and continue until either ``65535`` (16-bit)\
    or ``2^64-1`` (64-bit), at which point they roll over back to ``1``.\
    The frame ID should never be ``0``. In order to use 64-bit \
    frame IDs, the device must support ``GigE Vision 2.0``.\
    Simply enable the extended ID mode feature ``GevGVSPExtendedIDMode``.\n

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**

    '''
    # ---------------------------------------------------------------------

    def __get_payload_type(self):
        payload_type = self.xbuffer.xBufferGetPayloadType()
        return _enums.PayloadType(payload_type)

    payload_type = property(__get_payload_type)
    '''
    The buffer's payload type as an enum, as defined by the\
    GigE Vision specification.\n

    :getter: the buffer's payload.\n
    :type: enums.PayloadType\n

    The payload type indicates how to interpret the data stored\
    in the buffer ``buffer.data`` or ``buffer.pdata``. Lucid \
    devices may provide three ways to interpret the data:\n
    - as an image ``enums.PayloadType.IMAGE``.\n
    - as an image with chunk data appended to the end\
    ``enums.PayloadType.IMAGE_EXTENDED_CHUNK``.\n
    - as chunk data, which may or may not include image data as\
    a chunk ``enums.PayloadType.CHUNKDATA``.\n

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------

    def __get_has_chunkdata(self):
        return self.xbuffer.xBufferHasChunkData()

    has_chunkdata = property(__get_has_chunkdata)
    '''
    Returns whether or not a buffer's payload that may be \
    interpreted as chunk data. ``True`` if the payload has \
    chunk data otherwise, ``False``.\n

    :getter: returns whether or not a buffer's payload that may be \
    interpreted as chunk data.\n
    :type: ``bool``.\n

    Returns ``True`` if the payload type is:\n
    - ``enums.PayloadType.CHUNKDATA``.\n
    - ``enums.PayloadType.IMAGE_EXTENDED_CHUNK``.\n

    Returns ``False`` if the payload type is:\n
    - ``enums.PayloadType.IMAGE``.\n

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------

    def __get_has_imagedata(self):
        return self.xbuffer.xBufferHasImageData()

    has_imagedata = property(__get_has_imagedata)
    '''
    Returns whether or not a buffer's payload has data that may \
    be interpreted as image data. ``True`` if the payload has \
    image data otherwise, ``False``.\n

    :getter: returns whether or not a buffer's payload that may be \
    interpreted as image data.\n
    :type: ``bool``.\n

    Returns ``True`` if the payload type is:\n
    - ``enums.PayloadType.IMAGE``.\n
    - ``enums.PayloadType.IMAGE_EXTENDED_CHUNK``.\n

    Returns ``False`` if the payload type is:\n
    - ``enums.PayloadType.CHUNKDATA``.\n

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------

    def __get_is_incomplete(self):
        return self.xbuffer.xBufferIsIncomplete()

    is_incomplete = property(__get_is_incomplete)
    '''
    Returns whether or not the payload is complete.\n

    :getter: returns whether or not the payload is complete.\n
    :type: ``bool``.\n

    Error handling may be required in the case that the data is \
    incomplete. An incomplete image signifies that the data size\
    ``buffer.size_filled`` does not match the expected data size\
    ``PayloadSize``. This is either due to missed packets\
    or a small buffer.\n

    The number of missed packets may be discovered through the \
    stream node map ``device.tl_stream_nodemap``. The missed\
    packet count feature ``StreamMissedPacketCount`` is a\
    cumulative count of all missed packets, and does not \
    necessarily reflect the number of missed packets for \
    any given buffer.\n

    A buffer may be missing data if the buffer to hold the data\
    is too small. This happens when the size of the buffer \
    ``buffer.buffer_size`` does not match the expected data size\
    ``PayloadSize``. This will also return ``True`` when \
    checking whether the data is larger than the buffer \
    ``buffer.is_data_larger_than_buffer``.\n

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------

    def __get_is_data_larger_than_buffer(self):
        return self.xbuffer.xBufferDataLargerThanBuffer()

    is_data_larger_than_buffer = property(__get_is_data_larger_than_buffer)
    '''
    Returns whether or not a buffer's payload data is larger\
    than the buffer.\n

    :getter: returns whether or not  a buffer's payload data is\
    too large for the buffer.\n
    :type: ``bool``.\n

    A buffer may be missing data if the buffer to hold the data\
    is too small. This happens when the size of the buffer \
    ``buffer.buffer_size`` does not match the expected data size\
    ``PayloadSize``. This will also return ``True`` when \
    checking whether the data is larger than the buffer \
    ``buffer.is_data_larger_than_buffer``.\n

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------
    # TODO SFW-2027

    def __get_is_valid_crc(self):
        return self.xbuffer.xBufferVerifyCRC()

    is_valid_crc = property(__get_is_valid_crc)
    '''
    Returns whether or not a buffer data has a matching crc value\
    as that which was received from the device.\n

    :getter: returns whether or not a buffer data has a matching \n
    crc value as that which was received from the device.\n

    :type: ``bool``.\n

    Returns  ``True`` if the calculated CRC value equals the one \
    sent from the device, otherwise, ``False``.\n

    Calculates the CRC of a buffer's data and verifies it\
    against the CRC value sent from the device. This helps verify\
    that no data has been changed or missed during a transmission.\
    This calls a global helper function to calculate the CRC.\
    A CRC is performed by running a set of calculations on a \
    dataset both before and after a transmission. \
    The two calculated values are then compared for equality.\
    If the values are the same, then the transmission is deemed \
    successful; if different, then something in the transmission\
    went wrong.\n

    A device can be set to send a CRC value by enabling its \n
    chunk data setting.
    >>> nodemap.get_node('ChunkModeActive').value = True
    >>> nodemap.get_node('ChunkSelector').value = 'CRC'
    >>> nodemap.get_node('ChunkEnable').value = True

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n
    - if crc chunk is not enabled, calling ``buffer.is_valid_crc``\
    will raise an exception.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------

    def __get_width(self):
        return self.xbuffer.xImageGetWidth()

    width = property(__get_width)
    '''
    Width of the image buffer.\n

    :getter: gets the width of the image buffer.\n
    :type: ``int``.\n
    :unit: pixels.\n

    Gets the width of the image buffer in pixels. Images are \
    self-describing, so the device does not need to be queried to\
    get this information.\n

    Image buffers are either retrieved from a ``Device`` instance or created\
    by the factory ``BufferFactory``. If the image was retrieved \
    from a device, the width is populated by the acquisition engine\
    payload leader. The device itself is not queried as this data\
    is present in the image data. If the image was created by the\
    ``BufferFactory``, the width is populated by the arguments.\n

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**

    '''
    # ---------------------------------------------------------------------

    def __get_height(self):
        return self.xbuffer.xImageGetHeight()

    height = property(__get_height)
    '''
    Height of the image.\n

    :getter: gets the height of the image buffer.\n
    :type: ``int``.\n
    :unit: pixels\n

    Gets the height of the image buffer in pixels. Images are \
    self-describing, so the device does not need to be queried to\
    get this information.\n

    Image buffers are either retrieved from a ``Device`` instance or created\
    by the factory ``BufferFactory``. If the image was retrieved \
    from a device, the height is populated by the acquisition engine\
    payload leader. The device itself is not queried as this data\
    is present in the image data. If the image was created by the\
    ``BufferFactory``, the height is populated by the arguments.\n

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------

    def __get_offset_x(self):
        return self.xbuffer.xImageGetOffsetX()

    offset_x = property(__get_offset_x)
    '''
    Offset X of the image buffer.\n

    :getter: gets the offset X of the image buffer.\n
    :type: ``int``.\n
    :unit: pixels\n

    Gets the offset of the image along the X-axis. Images are \
    self-describing, so the device does not need to be queried to\
    get this information.\n

    Image buffers are either retrieved from a ``Device`` instance or created\
    by the factory ``BufferFactory``. If the image was retrieved \
    from a device, the height is populated by the acquisition engine\
    payload leader. The device itself is not queried as this data\
    is present in the image data. If the image was created by the\
    ``BufferFactory``, the height is populated by the arguments.\n

    The ``BufferFactory`` can create an image buffer from another image buffer\
    or from a minimal set of parameters ``buffer.data``, \
    ``buffer.width``, ``buffer.height``, ``buffer.pixel_format``.\
    If the image buffer is created from parameters, the offset X will\
    be set to ``0``, no matter its original value.\n

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------

    def __get_offset_y(self):
        return self.xbuffer.xImageGetOffsetY()

    offset_y = property(__get_offset_y)
    '''
    Offset Y of the image buffer.\n

    :getter: gets the offset Y of the image buffer.\n
    :type: ``int``.\n
    :unit: pixels\n

    Gets the offset of the image along the Y-axis. Images are \
    self-describing, so the device does not need to be queried to\
    get this information.\n

    Image buffers are either retrieved from a ``Device`` instance or created\
    by the factory ``BufferFactory``. If the image was retrieved \
    from a device, the height is populated by the acquisition engine\
    payload leader. The device itself is not queried as this data\
    is present in the image data. If the image buffer was created by the\
    ``BufferFactory``, the height is populated by the arguments.\n

    The ``BufferFactory`` can create an image buffer from another image buffer\
    or from a minimal set of parameters ``buffer.data``, \
    ``buffer.width``, ``buffer.height``, ``buffer.pixel_format``.\
    If the image buffer is created from parameters, the offset Y will\
    be set to ``0``, no matter its original value.\n

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------

    def __get_padding_x(self):
        return self.xbuffer.xImageGetPaddingX()

    padding_x = property(__get_padding_x)
    '''
    Padding X of the image.\n

    :getter: gets the padding of the image along the X-axis..\n
    :type: ``int``.\n
    :unit: pixels\n

    gets the padding of the image along the X-axis.. Images are \
    self-describing, so the device does not need to be queried to\
    get this information.\n

    Image buffers are either retrieved from a ``Device`` instance or created\
    by the factory ``BufferFactory``. If the image was retrieved \
    from a device, the height is populated by the acquisition engine\
    payload leader. The device itself is not queried as this data\
    is present in the image data. If the image buffer was created by the\
    ``BufferFactory``, the height is populated by the arguments.\n

    The ``BufferFactory`` can create an image buffer from another image buffer\
    or from a minimal set of parameters ``buffer.data``, \
    ``buffer.width``, ``buffer.height``, ``buffer.pixel_format``.\
    If the image buffer is created from parameters, the padding X will\
    be set to ``0``, no matter its original value.\n

    Padding X specifically refers to the number of bytes padding the end of\
    each line. This number will affect the pitch/stride/step of an image.\n

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------

    def __get_padding_y(self):
        return self.xbuffer.xImageGetPaddingY()

    padding_y = property(__get_padding_y)
    '''
    Padding Y of the image.\n

    :getter: gets the padding of the image along the Y-axis..\n
    :type: ``int``.\n
    :unit: pixels\n

    gets the padding of the image along the Y-axis.. Images are \
    self-describing, so the device does not need to be queried to\
    get this information.\n

    Image buffers are either retrieved from a ``Device`` instance or created\
    by the factory ``BufferFactory``. If the image was retrieved \
    from a device, the height is populated by the acquisition engine\
    payload leader. The device itself is not queried as this data\
    is present in the image data. If the image buffer was created by the\
    ``BufferFactory``, the height is populated by the arguments.\n

    The ``BufferFactory`` can create an image buffer from another image buffer\
    or from a minimal set of parameters ``buffer.data``, \
    ``buffer.width``, ``buffer.height``, ``buffer.pixel_format``.\
    If the image buffer is created from parameters, the padding Y will\
    be set to ``0``, no matter its original value.\n

    Padding Y specifically refers to the number of bytes padding the end of\
    each line. This number will affect the pitch/stride/step of an image.\n

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------

    def __get_pixel_format(self):
        pixel_format = self.xbuffer.xImageGetPixelFormat()
        return _enums.PixelFormat(pixel_format)

    pixel_format = property(__get_pixel_format)
    '''
    The buffer's pixel format as an enum, as defined by the\
    PFNC specification.\n

    :getter: the buffer's pixel format.\n
    :type: enums.PixelFormat\n

    Gets the pixel format (PfncFormat) of the image, as defined by the \
    PFNC (Pixel Format Naming Convention). Images are self-describing, \
    so the device does not need to be queried to get this information.\n

    Image buffers are either retrieved from a ``Device`` instance or created\
    by the factory ``BufferFactory``. If the image was retrieved \
    from a device, the height is populated by the acquisition engine\
    payload leader. The device itself is not queried as this data\
    is present in the image data. If the image buffer was created by the\
    ``BufferFactory``, the height is populated by the arguments.\n

    Pixel format value are determined by the PFNC (Pixel Format Naming\
    Convention) specification. The PFNC assigns a name and number to each\
    pixel format helping to standardize pixel formats. The number of bits per\
    pixel can be found in each integer at bytes 5 and 6 (mask 0x00FF0000). The\
    pixel format can be determined by the integer using the GetPixelFormatName\
    function provided by the PFNC.\n

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**

    '''
    # ---------------------------------------------------------------------

    def __get_bits_per_pixel(self):
        return self.xbuffer.xImageGetBitsPerPixel()

    bits_per_pixel = property(__get_bits_per_pixel)
    '''
    Bits per pixel of the image.\n

    :getter: ets the number of bits per pixel of the image buffer\
    from the integer value of the ``buffer.pixel_format`` (PfncFormat)..\n
    :type: ``int``.\n
    :unit: pixels

    Gets the number of bits per pixel of the image buffer\
    from the integer value of the ``buffer.pixel_format`` (PfncFormat).\
    Internally, a public helper funciton is called ``get_bits_per_pixel()``.
    Pixel format value are determined by the PFNC (Pixel Format Naming\
    Convention) specification. The PFNC assigns a name and number to each\
    pixel format helping to standardize pixel formats. The number of bits per\
    pixel can be found in each integer at bytes 5 and 6
    (mask 0x00FF0000).

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------

    def __get_pixel_endianness(self):
        pixel_endianness = self.xbuffer.xImageGetPixelEndianness()
        return _enums.PixelEndianness(pixel_endianness)

    pixel_endianness = property(__get_pixel_endianness)
    '''
    Endianness of the pixels of the image.\n

    :getter: gets the pixel endianness of the image data.\n
    :type: enums.PixelEndianness\n

    Gets the pixel endianness of the image data. Images are self-describing, \
    so the device does not need to be queried to get this information.\n

    Image buffers are either retrieved from a ``Device`` instance or created\
    by the factory ``BufferFactory``. If the image was retrieved \
    from a device, the height is populated by the acquisition engine\
    payload leader. The device itself is not queried as this data\
    is present in the image data. If the image buffer was created by the\
    ``BufferFactory``, the height is populated by the arguments.\n

    The image factory can create an image from another image (Arena::IImage)
    or from a minimal set of parameters (data, width, height, pixel format).
    If the image was created from parameters, the pixel endianness will be set
    to 0 (EPixelEndianness::PixelEndiannessUnknown), no matter its original
    value.

    The ``BufferFactory`` can create an image buffer from another image buffer\
    or from a minimal set of parameters ``buffer.data``, \
    ``buffer.width``, ``buffer.height``, ``buffer.pixel_format``.\
    If the image buffer is created from parameters, the pixel endianness will\
    be set to ``0`` which is enums.PixelEndianness.UNKNOWN , no matter its \
    original value.\n

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------

    def __get_timestamp_ns(self):
        return self.xbuffer.xImageGetTimestampNs()

    timestamp_ns = property(__get_timestamp_ns)
    '''
    Timestamp of the image buffer in nanoseconds.\n

    :getter: gets the timestamp of the image in nanoseconds.\n
    :type: ``int``.\n
    :unit: nanoseconds/\n

    Gets the timestamp of the image in nanoseconds. Images are\
    self-describing, so the device does not need to be queried to get\
    this information.\n

    Image buffers are either retrieved from a ``Device`` instance or created\
    by the factory ``BufferFactory``. If the image was retrieved \
    from a device, the height is populated by the acquisition engine\
    payload leader. The device itself is not queried as this data\
    is present in the image data. If the image buffer was created by the\
    ``BufferFactory``, the height is populated by the arguments.\n

    The ``BufferFactory`` can create an image buffer from another image buffer\
    or from a minimal set of parameters ``buffer.data``, \
    ``buffer.width``, ``buffer.height``, ``buffer.pixel_format``.\
    If the image buffer is created from parameters, the timetamp will\
    be set to ``0`` which is enums.PixelEndianness.UNKNOWN , no matter its \
    original value.\n

    This is the same as the nanosecond timestamp property\
    ``buffer.timestamp`` (deprecated in 2.0.0).\n

    :warning:\n
    - causes undefined behavior if buffer requeued \
    ``device.requeue_buffer()``.\n
    - properties lazily instantiated if buffer retrieved from device.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------

    def __get_pdata(self):
        return self.xbuffer.xImageGetData()

    pdata = property(__get_pdata)
    # TODO SFW-2301

    '''
    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------

    def __get_data(self):
        return self.xbuffer.xImageGetData()[:self.xbuffer.xBufferGetPayloadSize()]

    data = property(__get_data)
    # TODO SFW-2301
    '''
    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    '''
    # ---------------------------------------------------------------------

    # TODO SFW-2187
    # TODO SFW-2188
    def get_chunk(self, chunk_names):
        '''
        Gets a specified chunk or multiple chunks, returning it as a node(s) \
        in order to preserve metadata related to the chunk.\n

        **Args**:\n
            chunk_names: it can be:\n
                - a ``str``.\n
                - a ``list`` of ``str``.\n
                - a ``tuple`` of ``str``.\n
            - str's value represents the name of the chunk to retrieve as a node.\
            the name is prefixed with 'Chunk'. for example the name of the CRC\
            chunk is 'ChunkCRC'\n

        **Raises**:
            - ``ValueError`` :
                - ``chunk_names`` is a ``list`` or ``tuple`` but has an\
                    element that is not a ``str``.\n
                - ``chunk_names`` value does not match a valid chunk name.\n
            - ``TypeError`` :
                - ``chunk_names`` type is not ``list``, ``tuple`` nor ``str``.\n

        **Returns**:
            - a ``dict``, that has chunk name as a key and the node\
            is the value, if ``chunk_names`` is a ``list``.\n
            - a ``node`` instance when ``chunk_names`` is a str.\

        Internally, chunk data objects have an internal node map and \
        a chunk adapter. These allow chunk information to be processed\
        and read as ``Node`` instances.

        There is a chance that incomplete images have garbage data in \
        place of expected chunk data. If this is the case, it is still\
        possible to attempt chunk retrieval. Invalid chunks raise a\
        ``ValueError``.\n

        >>> # enabling timestamp chunk data
        >>> device.nodemap.get_node('ChunkModeActive').value = True
        >>> device.nodemap.get_node('ChunkSelector').value = 'CRC'
        >>> device.nodemap.get_node('ChunkEnable').value = True
        >>> device.start_stream()
        >>> buffer_with_chunk_data = device.get_buffer()
        >>> if buffer_with_chunk_data.is_incomplete:
        >>>     print('Chunks might contain garbage values')
        >>> else:
        >>>     chunk_crc_node = buffer_with_chunk_data.get_chunk('ChunkCRC')
        >>>     print(chunk_crc_node.value)
        >>> device.stop_stream()


        Chunk data must meet three criteria to provide relevant data.\
        Chunk mode must be activated ``ChunkModeActive``, the chunk must\
        be enabled ``ChunkSelector`` value is ``ChunkEnable``, and the node\
        must exist:\n
        - if chunk mode is inactive, the buffer will not contain chunk data\
        - if chunk does not exist, returns null \
        - if chunk is not enabled, returned node will be unavailable

        :warning:\n
        - causes undefined behavior if buffer requeued \
        ``device.requeue_buffer()``.\n
        - properties lazily instantiated if buffer retrieved from device.\n

        **--------------------------------------------------------------**\
        **---------------------------------------------------------------**
        '''

        # list
        if isinstance(chunk_names, list):
            return self.__get_chunks_as_dict(chunk_names)

        # tuple
        elif isinstance(chunk_names, tuple):
            return self.__get_chunks_as_dict(list(chunk_names))

        elif isinstance(chunk_names, str):
            # get one from node name
            return self.__get_chunk(chunk_names)
        else:
            raise ValueError(f'expected list, tuple , or str '
                             f'instead of {type(chunk_names).__name__}')

    def __get_chunks_as_dict(self, chunk_names):

        self.__check__get_chunks_as_dict_input_parameter_chunk_names(
            chunk_names)

        specific_chunks = {}
        for name in chunk_names:
            specific_chunks[name] = self.__get_chunk(name)
        return specific_chunks

    def __check__get_chunks_as_dict_input_parameter_chunk_names(self,
                                                                chunk_names):
        for name in chunk_names:
            if not isinstance(name, str):
                raise ValueError('expected list/tuple str elements instead of '
                                 f'{type(chunk_names).__name__}')

    def __get_chunk(self, chunk_names):

        # input is already checked if it is a str or not
        chunk_node = self.xbuffer.xChunkDataGetChunk(chunk_names)
        if not chunk_node:
            raise ValueError(
                f'\'{chunk_names}\' Chunk is not found in the buffer')

        node_ = _Node(chunk_node)
        specific_chunk = _cast_from_general_node_to_specific_node_type(node_)

        return specific_chunk


class BufferFactory():
    '''
    A static class responsible for the copying, conversion, \
    and destruction of buffers with image data --Image buffers.\n
    The factory allocates and deallocates memory for its images.\
    Memory is allocated when an image is copied ``BufferFactory.Copy()``or \
    converted ``BufferFactory.Convert()``. To clean up memory, all images\
    created by ``BufferFactory`` must be destroyed via\
    ``BufferFactory.Destroy()``.\n

    Images from the this factory are treated noticeably different from those\
    from a ``Device`` instance. Retrieving an image from a device grabs a\
    buffer that had its memory preallocated when the device started streaming;\
    retrieving and requeuing does not allocate or deallocate memory, but\
    simply moves buffers around the acquisition engine. Copying, and
    converting an image with the this factory allocates and deallocates memory
    as needed. This is why images from a device must be requeued\
    ``device.requeue_buffer()`` while images from the image \
    factory must be destroyed via ``BufferFactory.Destroy()``.\n

    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**

    '''

    # create ----------------------------------------------------------------
    @ staticmethod
    def create(pdata, data_size, width, height, pixel_format):

        # TODO check pdata type
        '''
        if not isinstance(buffer, Buffer):
            raise TypeError(f'Buffer expected instead '
                            f'of {type(buffer).__name__}')
        '''

        # pixel_format (str, int, enums.PixelFormat) ----------------------
        if isinstance(pixel_format, str):
            pixel_format = int(enums.PixelFormat[pixel_format])
        elif isinstance(pixel_format, int):
            pixel_format = int(pixel_format)
        else:
            raise TypeError(f'PixelFormat expected instead of '
                            f'{type(pixel_format).__name__} for '
                            f'pixel_format parameter')

        hxbuffer_value = _xImagefactory.xImageFactoryCreate(
            pdata, data_size, width, height, pixel_format)
        return _Buffer(hxbuffer_value)

    # copy ----------------------------------------------------------------

    @ staticmethod
    def copy(buffer):
        '''
        Creates a deep copy of an image buffer from another image buffer.\

        **Args**:\n
            buffer:\n
            - a ``_Buffer`` instance to copy.\n

        **Raises**:\n
            - ``TypeError``:\n
                - ``buffer`` is not of type ``_Buffer``.\n

        **Returns**:\n
            - ``_Buffer`` instance.\n

        Images from this method factory must be destroyed via\
        ``BufferFactory.Destroy()``.\n

        When copying an image, the ``BufferFactory`` allocates memory \
        for the new image. As such, images created by copying an image\
        with the image factory must be destroyed; otherwise, memory will leak.\n

        >>> image = device.get_buffer()
        >>> image_copy = BufferFactory.copy(image)
        >>> # must use requeue_buffer for image from device
        >>> device.requeue_buffer(image)
        >>> # proccess image_copy then destroy image from factory
        >>> BufferFactory.destroy(image_copy)

        :warning:\n
        - images from the image factory must be destroyed.\n
        - images from a device should be requeued.\n
        - instantiates all lazy properties of the original image.\n

        **--------------------------------------------------------------**\
        **---------------------------------------------------------------**
        '''
        if not isinstance(buffer, _Buffer):
            raise TypeError(f'Buffer expected instead '
                            f'of {type(buffer).__name__}')

        hxbuffer_value = _xImagefactory.xImageFactoryCopy(
            buffer.xbuffer.hxbuffer.value)
        return _Buffer(hxbuffer_value)

    # convert -------------------------------------------------------------
    # TODO SFW-2189
    # TODO SFW-2533 # also update docs
    @ staticmethod
    def convert(buffer, new_pixel_format, bayer_algorithm=None):
        '''
        Converts an image buffer to a select pixel format. In doing\
        so, it creates a completely new image, similar to a deep\
        copy but with a different pixel format.\n

        **Args**:\n
            - buffer:\n
                - a ``_Buffer`` instance to convert.\n
            - new_pixel_format:\n
                - ``enums.PixelFormat`` to convert to.

            - bayer_algorithm:\n
                - ``enums.BayerAlgorithm`` type. this is the Bayer\
                conversion algorithm to use. Only applicable when\
                converting from bayer.\n
                - ``None``. for no conversion algorithm

        **Raises**:\n
            - ``TypeError``:\n
                - ``buffer`` is not of ``_Buffer`` type.
                - ``new_pixel_format`` type is not a ``str``, ``int``, nor \
                ``enum.PixelFormat``.\n
                - ``bayer_algorithm`` type is not a ``str``, ``int``, nor \
                ``enum.BayerAlgorithm``.\n

        **Returns**:\n
            - ``_Buffer`` instance with new pixel format. This is a new\
            instance.\n

        Images from this method factory must be destroyed via\
        ``BufferFactory.Destroy()``.\n

        >>> image = device.get_buffer()
        >>> image_BGRa8 = None
        >>> if image.pixel_format != enums.PixelFormat.BGRa8:
        >>>     image_BGRa8 = BufferFactory.covert(image, enums.PixelFormat.BGRa8)
        >>> else:
        >>>     image_BGRa8 = BufferFactory.copy(image)
        >>> device.requeue_buffer(image)
        >>> # proccess image_BRGa8 then destroy image from factory
        >>> BufferFactory.destroy(image_BGRa8)

        The list of supported pixel formats can be found in\
        ``enums.PixelFormat``. The list of supported conversion.
        pixel formats is difference from a device's pixel formats
        ``PixelFormat`` node. In order for conversion to succeed, \
        both the source and destination pixel formats must be\
        supported. Bayer formats are supported as source formats only.\n

        :warning:\n
        - Images from the image factory must be destroyed.\n
        - Images from a device should be requeued.\n
        - Cannot convert to bayer formats.\n
        - Bayer conversion algorithm only necessary when converting from bayer
        formats.\n

        **--------------------------------------------------------------**\
        **---------------------------------------------------------------**
        '''
        # returns a new buffer copy

        # checks ----------------------

        # buffer --------------------------------------------------------------
        if not isinstance(buffer, _Buffer):
            raise TypeError(f'Buffer expected instead of '
                            f'{type(buffer).__name__} for '
                            f'buffer parameter')

        # new_pixel_format (str, int, enums.PixelFormat) ----------------------
        if isinstance(new_pixel_format, str):
            new_pixel_format = int(_enums.PixelFormat[new_pixel_format])

        elif isinstance(new_pixel_format, int):
            new_pixel_format = int(new_pixel_format)
        else:
            raise TypeError(f'PixelFormat expected instead of '
                            f'{type(new_pixel_format).__name__} for '
                            f'new_pixel_format parameter')

        # bayer_algorithm (none, str, int, enums.BayerAlgorithm) --------------
        if bayer_algorithm is None:
            pass
        elif isinstance(bayer_algorithm, str):
            bayer_algorithm = int(_enums.BayerAlgorithm[bayer_algorithm])
        elif isinstance(bayer_algorithm, int):  # ints and enums
            bayer_algorithm = int(bayer_algorithm)
        else:
            raise TypeError(f'BayerAlgorithm expected instead of '
                            f'{type(bayer_algorithm).__name__} for '
                            f'bayer_algorithm parameter')

        # convert -------------------------------------------------------------

        if bayer_algorithm is None:
            hxbuffer_value = _xImagefactory.xImageFactoryConvert(
                buffer.xbuffer.hxbuffer.value,
                new_pixel_format)
        else:
            hxbuffer_value = _xImagefactory.xImageFactoryConvertBayerAlgorithm(
                buffer.xbuffer.hxbuffer.value,
                new_pixel_format,
                bayer_algorithm)

        return _Buffer(hxbuffer_value)

    # destroy -------------------------------------------------------------
    # TODO SFW-2190
    @ staticmethod
    def destroy(buffer):
        '''
        Creates a deep copy of an image buffer from another image buffer.\n

        **Args**:\n
            buffer:\n
            - a ``_Buffer`` instance to destroy. it must be created by\
            ``BufferFactory``.\n

        **Raises**:\n
            - ``TypeError``:\n
                - ``buffer`` is not of type ``_Buffer``.\n

        **Returns**:\n
        - ``None``.\n

        Images from this method factory must be destroyed via\
        ``BufferFactory.Destroy()``.\n


        Cleans up an image buffer and deallocates its\
        memory. It must be called on any image created by\
        the buffer factory function ``BufferFactory.copy()``\
        ``BufferFactory.convert()``.\n

         Images from the buffer factory must be destroyed via\
        ``BufferFactory.Destroy()``.\n


        All images from the buffer factory, whether copied or converted,\
        must be destroyed to deallocate their memory; otherwise, \
        memory will leak. It is important that this method only be\
        called on image buffers from the image factory, and not on\
        those retrieved from a device.\n

        :warning:\n
        - images from the image factory must be destroyed.\n
        - images from a device should be requeued.\n

        **--------------------------------------------------------------**\
        **---------------------------------------------------------------**
        '''
        if not isinstance(buffer, _Buffer):
            raise TypeError(f'Buffer expected instead of '
                            f'{type(buffer).__name__}')

        _xImagefactory.xImageFactoryDestroy(buffer.xbuffer.hxbuffer.value)
