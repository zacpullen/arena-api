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

from ctypes import POINTER, byref

from arena_api._xlayer.xarena.arenac import harenac
from arena_api._xlayer.xarena.arenac_types import (ac_access_mode,
                                                   ac_payload_type,
                                                   ac_pixel_endianness,
                                                   acBuffer, acNode, bool8_t,
                                                   char_ptr, size_t, uint8_t,
                                                   uint64_t)


class _xBuffer():

    def __init__(self, hxbuffer):
        # TODO SFW-2546
        if not hxbuffer:
            raise TypeError('xBuffer handle is None')
        self.hxbuffer = acBuffer(hxbuffer)

    def xBufferGetSizeFilled(self):

        size_filled = size_t(0)
        # AC_ERROR acBufferGetSizeFilled(
        #   acBuffer hBuffer,
        #   size_t * pSizeFilled)
        harenac.acBufferGetSizeFilled(
            self.hxbuffer, byref(size_filled))

        return size_filled.value

    def xBufferGetPayloadSize(self):

        payload_size = size_t(0)
        # AC_ERROR acBufferGetPayloadSize(
        #   acBuffer hBuffer,
        #   size_t * pPayloadSize)
        harenac.acBufferGetPayloadSize(
            self.hxbuffer,
            byref(payload_size))

        return payload_size.value

    def xBufferGetSizeOfBuffer(self):

        size_of_buffer = size_t(0)
        # AC_ERROR acBufferGetSizeOfBuffer(
        #   acBuffer hBuffer,
        #   size_t * pSizeOfBuffer)
        harenac.acBufferGetSizeOfBuffer(
            self.hxbuffer,
            byref(size_of_buffer))

        return size_of_buffer.value

    def xBufferGetFrameId(self):

        frame_id = uint64_t(0)
        # AC_ERROR acBufferGetFrameId(
        #   acBuffer hBuffer,
        #   uint64_t * pFrameId)
        harenac.acBufferGetFrameId(
            self.hxbuffer,
            byref(frame_id))

        return frame_id.value

    def xBufferGetPayloadType(self):

        payload_type = ac_payload_type(0)
        # AC_ERROR acBufferGetPayloadType(
        #   acBuffer hBuffer,
        #   AC_PAYLOAD_TYPE * pPayloadType)
        harenac.acBufferGetPayloadType(
            self.hxbuffer,
            byref(payload_type))

        return payload_type.value

    def xBufferHasChunkData(self):

        has_chunk_data = bool8_t(False)
        # AC_ERROR acBufferHasChunkData(
        #   acBuffer hBuffer,
        #   bool8_t * pHasChunkData)
        harenac.acBufferHasChunkData(
            self.hxbuffer,
            byref(has_chunk_data))

        return has_chunk_data.value

    def xBufferHasImageData(self):

        has_image_data = bool8_t(False)
        # AC_ERROR acBufferHasImageData(
        #   acBuffer hBuffer,
        #   bool8_t * pHasImageData)
        harenac.acBufferHasImageData(
            self.hxbuffer,
            byref(has_image_data))

        return has_image_data.value

    def xBufferIsIncomplete(self):

        is_incomplete = bool8_t(False)
        # AC_ERROR acBufferIsIncomplete(
        #   acBuffer hBuffer,
        #   bool8_t * pIsIncomplete)
        harenac.acBufferIsIncomplete(
            self.hxbuffer,
            byref(is_incomplete))

        return is_incomplete.value

    def xBufferDataLargerThanBuffer(self):

        is_data_larger_than_buffer = bool8_t(False)
        # AC_ERROR acBufferDataLargerThanBuffer(
        #   acBuffer hBuffer,
        #   bool8_t * pDataLargerThanBuffer)
        harenac.acBufferDataLargerThanBuffer(
            self.hxbuffer,
            byref(is_data_larger_than_buffer))

        return is_data_larger_than_buffer.value

    def xBufferVerifyCRC(self):

        is_correct_crc = bool8_t(False)
        # AC_ERROR acBufferVerifyCRC(
        #   acBuffer hBuffer,
        #   bool8_t * pVerifyCRC)
        harenac.acBufferVerifyCRC(
            self.hxbuffer,
            byref(is_correct_crc))

        return is_correct_crc.value

    # ---------------------------------------------------------------------

    def xImageGetWidth(self):

        width = size_t(0)
        # AC_ERROR acImageGetWidth(
        #   acBuffer hBuffer,
        #   size_t* pWidth)
        harenac.acImageGetWidth(
            self.hxbuffer,
            byref(width))

        return width.value

    def xImageGetHeight(self):

        height = size_t(0)
        # AC_ERROR acImageGetHeight(
        #   acBuffer hBuffer,
        #   size_t* pHeight)
        harenac.acImageGetHeight(
            self.hxbuffer,
            byref(height))

        return height.value

    def xImageGetOffsetX(self):

        offsetx = size_t(0)
        # AC_ERROR acImageGetOffsetX(
        #   acBuffer hBuffer,
        #   size_t* pOffsetX)
        harenac.acImageGetOffsetX(
            self.hxbuffer,
            byref(offsetx))

        return offsetx.value

    def xImageGetOffsetY(self):

        offsety = size_t(0)
        # AC_ERROR acImageGetOffsetY(
        #   acBuffer hBuffer,
        #   size_t* pOffsetY)
        harenac.acImageGetOffsetY(
            self.hxbuffer,
            byref(offsety))

        return offsety.value

    def xImageGetPaddingX(self):

        paddingx = size_t(0)
        # AC_ERROR acImageGetPaddingX(
        #   acBuffer hBuffer,
        #   size_t* pPaddingX)

        harenac.acImageGetPaddingX(
            self.hxbuffer,
            byref(paddingx))

        return paddingx.value

    def xImageGetPaddingY(self):

        paddingy = size_t(0)
        # AC_ERROR acImageGetPaddingY(
        #   acBuffer hBuffer,
        #   size_t* pPaddingY)

        harenac.acImageGetPaddingY(
            self.hxbuffer,
            byref(paddingy))

        return paddingy.value

    def xImageGetPixelFormat(self):

        pixel_format = uint64_t(0)
        # AC_ERROR acImageGetPixelFormat(
        #   acBuffer hBuffer,
        #   uint64_t* pPixelFormat)
        harenac.acImageGetPixelFormat(
            self.hxbuffer,
            byref(pixel_format))

        return pixel_format.value

    def xImageGetBitsPerPixel(self):

        bitsperpixel = size_t(0)
        # AC_ERROR acImageGetBitsPerPixel(
        #   acBuffer hBuffer,
        #   size_t* pBitsPerPixel)

        harenac.acImageGetBitsPerPixel(
            self.hxbuffer,
            byref(bitsperpixel))

        return bitsperpixel.value

    def xImageGetPixelEndianness(self):

        pixelendianness = ac_pixel_endianness()

        # AC_ERROR acImageGetPixelEndianness(
        #   acBuffer hBuffer,
        #   AC_PIXEL_ENDIANNESS* pPixelEndianness)
        harenac.acImageGetPixelEndianness(
            self.hxbuffer,
            byref(pixelendianness))

        return pixelendianness.value

    def xImageGetTimestamp(self):

        timestamp = uint64_t(0)
        # AC_ERROR acImageGetTimestamp(
        #   acBuffer hBuffer,
        #   uint64_t* pTimestamp)
        harenac.acImageGetTimestamp(
            self.hxbuffer,
            byref(timestamp))

        return timestamp.value

    def xImageGetTimestampNs(self):

        timestampns = uint64_t(0)
        # AC_ERROR acImageGetTimestampNs(
        #   acBuffer hBuffer,
        #   uint64_t* pTimestampNs)
        harenac.acImageGetTimestampNs(
            self.hxbuffer,
            byref(timestampns))

        return timestampns.value

    def xImageGetData(self):

        pdata = POINTER(uint8_t)(uint8_t(0))
        # AC_ERROR acImageGetData(
        #   acBuffer hBuffer,
        #   uint8_t** ppData)
        harenac.acImageGetData(self.hxbuffer, byref(pdata))

        return pdata

    # ---------------------------------------------------------------------

    def xChunkDataGetChunk(self, name):

        name_p = char_ptr(name.encode())
        hchunk_node = acNode(None)
        # AC_ERROR acChunkDataGetChunk(
        #   acBuffer hBuffer,
        #   const char* pName,
        #   acNode* phChunkNode)
        harenac.acChunkDataGetChunk(
            self.hxbuffer,
            name_p,
            byref(hchunk_node)
        )

        return hchunk_node.value

    def xChunkDataGetChunkAndAccessMode(self, name):

        name_p = char_ptr(name.encode())
        hchunk_node = acNode(None)
        access_mode = ac_access_mode(0)
        # AC_ERROR acChunkDataGetChunkAndAccessMode(
        #   acBuffer hBuffer,
        #   char* pName,
        #   acNode* phChunkNode,
        #   AC_ACCESS_MODE* pAccessMode)
        harenac.acChunkDataGetChunkAndAccessMode(
            self.hxbuffer,
            name_p,
            byref(hchunk_node),
            byref(access_mode)
        )

        return hchunk_node.value, access_mode.value
