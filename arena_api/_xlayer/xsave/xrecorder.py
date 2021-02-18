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

from ctypes import byref, create_string_buffer, create_unicode_buffer

from arena_api._xlayer.info import Info
from arena_api._xlayer.xsave.savec import hsavec
from arena_api._xlayer.xsave.savec_types import (
    char_ptr, double, saveRecorder, size_t, uint8_t, uint64_t, wchar_ptr)
from arena_api._xlayer.xsave.xsave_defaults import XSAVE_STR_BUF_SIZE_DEFAULT

_info = Info()


class xRecorder:
    '''
    direct mapping for c functions exclude __init__ and __del__

    '''

    def __init__(self, width=None, height=None, fps=None):
        self.recorder = None
        self.hRecorder = None

        if all([width, height, fps]):  # all param passed
            self.recorder = self._Create(width, height, fps)
        elif not any([width, height, fps]):  # no param passed
            self.recorder = self._CreateEmpty()
        else:  # some param passed
            raise ValueError('xInternal : not all args have been passed')

        self.hRecorder = saveRecorder(self.recorder)

        # redirect functions on windows to use the Unicode SaveC function
        # WINDOWS ONLY: UNICODE handling
        # in __init__ function this function will be assigned to
        # self.SetExtension so the upper levels have on function to call
        # and the unicode for windows is handled in the __init__
        if _info.is_windows:
            self.SetFileNamePattern = self._SetFileNamePatternU
            self.UpdateTag = self._UpdateTagU
            self.GetFileNamePattern = self._GetFileNamePatternU
            self.GetExtension = self._GetExtensionU
            self.GetLastFileName = self._GetLastFileNameU
            self.PeekFileName = self._PeekFileNameU

    def __del__(self):
        if self.hRecorder:
            return self._Destroy()

    # only call from __init__
    @staticmethod
    def _CreateEmpty():

        hRecorder = saveRecorder(None)

        # SC_ERROR saveRecorderCreateEmpty(
        #   saveRecorder* phRecorder)
        hsavec.saveRecorderCreateEmpty(byref(
            hRecorder))

        return hRecorder.value

    # only call from __init__
    @staticmethod
    def _Create(width, height, fps):

        width = size_t(width)
        height = size_t(height)
        fps = double(fps)
        hRecorder = saveRecorder(None)

        # SC_ERROR saveRecorderCreate(
        #   size_t width,
        #   size_t height,
        #   double fps,
        #   saveRecorder* phRecorder)
        hsavec.saveRecorderCreate(
            width,
            height,
            fps,
            byref(hRecorder))

        return hRecorder.value

    def _Destroy(self):

        # SC_ERROR saveRecorderDestroy(
        #   saveRecorder hRecorder)
        hsavec.saveRecorderDestroy(
            self.hRecorder)

    def SetRaw(self):

        # SC_ERROR saveRecorderSetRaw(
        #   saveRecorder hRecorder)
        hsavec.saveRecorderSetRaw(
            self.hRecorder)

    def SetRawAviBGR8(self):

        # SC_ERROR saveRecorderSetRawAviBGR8(
        #   saveRecorder hRecorder)
        hsavec.saveRecorderSetRawAviBGR8(
            self.hRecorder)

    def SetRawMovRGB8(self):

        # SC_ERROR saveRecorderSetRawMovRGB8(
        #   saveRecorder hRecorder)
        hsavec.saveRecorderSetRawMovRGB8(
            self.hRecorder)

    def SetH264MovRGB8(self):

        # SC_ERROR saveRecorderSetH264MovRGB8(
        #   saveRecorder hRecorder)
        hsavec.saveRecorderSetH264MovRGB8(
            self.hRecorder)

    def SetH264MovBGR8(self):

        # SC_ERROR saveRecorderSetH264MovBGR8(
        #   saveRecorder hRecorder)
        hsavec.saveRecorderSetH264MovBGR8(
            self.hRecorder)

    def SetH264Mp4RGB8(self):

        # SC_ERROR saveRecorderSetH264Mp4RGB8(
        #   saveRecorder hRecorder)
        hsavec.saveRecorderSetH264Mp4RGB8(
            self.hRecorder)

    def SetH264Mp4BGR8(self):

        # SC_ERROR saveRecorderSetH264Mp4BGR8(
        #   saveRecorder hRecorder)
        hsavec.saveRecorderSetH264Mp4BGR8(
            self.hRecorder)

    def SetParams(self, width, height, fps):

        width = size_t(width)
        height = size_t(height)
        fps = double(fps)

        # SC_ERROR  saveRecorderSetParams(
        #   saveRecorder hRecorder,
        #   size_t width,
        #   size_t height,
        #   double fps)
        hsavec.saveRecorderSetParams(
            self.hRecorder,
            width,
            height,
            fps)

    def SetFileNamePattern(self, file_name_pattern):

        file_name_pattern_p = char_ptr(file_name_pattern.encode())

        # SC_ERROR saveRecorderSetFileNamePattern(
        #   saveRecorder hRecorder,
        #   const char* pFileNamePattern)
        hsavec.saveRecorderSetFileNamePattern(
            self.hRecorder,
            file_name_pattern_p)

    # WINDOWS ONLY: UNICODE handling
    # in __init__ function this function will be assigned to
    # self.SetExtension so the upper levels have on function to call
    # and the unicode for windows is handled in the __init__
    def _SetFileNamePatternU(self, file_name_pattern):

        file_name_pattern_p = wchar_ptr(file_name_pattern)
        # SC_ERROR saveRecorderSetFileNamePatternU(
        #   saveRecorder hRecorder,
        #   const wchar_t* pFileNamePattern);
        hsavec.saveRecorderSetFileNamePatternU(
            self.hRecorder,
            file_name_pattern_p)

    def UpdateTag(self, tag, value):

        tag_p = char_ptr(tag.encode())
        value_p = char_ptr(value.encode())

        # SC_ERROR saveRecorderUpdateTag(
        #   saveRecorder hRecorder,
        #   const char* pTag,
        #   const char* pValue)
        hsavec.saveRecorderUpdateTag(
            self.hRecorder,
            tag_p, value_p)

    # WINDOWS ONLY: UNICODE handling
    # in __init__ function this function will be assigned to
    # self.SetExtension so the upper levels have on function to call
    # and the unicode for windows is handled in the __init__
    def _UpdateTagU(self, tag, value):

        tag_p = wchar_ptr(tag)
        value_p = wchar_ptr(value)

        # SC_ERROR saveRecorderUpdateTagU(
        #   saveRecorder hRecorder,
        #   const wchar_t* pTag,
        #   const wchar_t* pValue)
        hsavec.saveRecorderUpdateTagU(
            self.hRecorder,
            tag_p, value_p)

    def SetCount(self, count):

        count = uint64_t(count)

        # SC_ERROR saveRecorderSetCount(
        #   saveRecorder hRecorder,
        #   uint64_t count)
        hsavec.saveRecorderSetCount(
            self.hRecorder,
            count)

    def SetCountPath(self, count):

        count = uint64_t(count)

        # SC_ERROR saveRecorderSetCountPath(
        #   saveRecorder hRecorder,
        #   uint64_t count)
        hsavec.saveRecorderSetCountPath(
            self.hRecorder,
            count)

    def SetCountGlobal(self, count):

        count = uint64_t(count)

        # SC_ERROR saveRecorderSetCountGlobal(
        #   saveRecorder hRecorder,
        #   uint64_t count)
        hsavec.saveRecorderSetCountGlobal(
            self.hRecorder,
            count)

    def SetTimestamp(self, timestamp):

        timestamp = uint64_t(timestamp)

        # SC_ERROR saveRecorderSetTimestamp(
        #   saveRecorder hRecorder,
        #   uint64_t timestamp)
        hsavec.saveRecorderSetTimestamp(
            self.hRecorder,
            timestamp)

    def GetParams(self):

        width = size_t(0)
        height = size_t(0)
        fps = double(0.0)

        # SC_ERROR saveRecorderGetParams(
        #   saveRecorder hRecorder,
        #   size_t* pWidth,
        #   size_t* pHeight,
        #   double* pFps)
        hsavec.saveRecorderGetParams(
            self.hRecorder,
            byref(width),
            byref(height),
            byref(fps))

        return width.value, height.value, fps.value

    def GetFileNamePattern(self):

        file_name_pattern_p = create_string_buffer(
            XSAVE_STR_BUF_SIZE_DEFAULT)
        length = size_t(XSAVE_STR_BUF_SIZE_DEFAULT)

        # SC_ERROR saveRecorderGetFileNamePattern(
        #   saveRecorder hRecorder,
        #   char* pFileNamePattern,
        #   size_t* pLen)
        hsavec.saveRecorderGetFileNamePattern(
            self.hRecorder,
            file_name_pattern_p,
            byref(length))

        return file_name_pattern_p.value.decode()

    # WINDOWS ONLY: UNICODE handling
    # in __init__ function this function will be assigned to
    # self.SetExtension so the upper levels have on function to call
    # and the unicode for windows is handled in the __init__
    def _GetFileNamePatternU(self):

        file_name_pattern_p = create_unicode_buffer(
            XSAVE_STR_BUF_SIZE_DEFAULT)
        length = size_t(XSAVE_STR_BUF_SIZE_DEFAULT)

        # SC_ERROR saveRecorderGetFileNamePatternU(
        #   saveRecorder hRecorder,
        #   wchar_t* pFileNamePattern,
        #   size_t* pLen)
        hsavec.saveRecorderGetFileNamePatternU(
            self.hRecorder,
            file_name_pattern_p,
            byref(length))
        return file_name_pattern_p.value

    def GetExtension(self):

        extension_p = create_string_buffer(
            XSAVE_STR_BUF_SIZE_DEFAULT)
        length = size_t(XSAVE_STR_BUF_SIZE_DEFAULT)

        # SC_ERROR saveRecorderGetExtension(
        #   saveRecorder hRecorder,
        #   char * pExtension,
        #   size_t * pLen)
        hsavec.saveRecorderGetExtension(
            self.hRecorder,
            extension_p,
            byref(length))

        return extension_p.value.decode()

    # WINDOWS ONLY: UNICODE handling
    # in __init__ function this function will be assigned to
    # self.SetExtension so the upper levels have on function to call
    # and the unicode for windows is handled in the __init__
    def _GetExtensionU(self):

        extension_p = create_unicode_buffer(
            XSAVE_STR_BUF_SIZE_DEFAULT)
        length = size_t(XSAVE_STR_BUF_SIZE_DEFAULT)

        # SC_ERROR saveRecorderGetExtensionU(
        #   saveRecorder hRecorder,
        #   wchar_t* pExtension,
        #   size_t* pLen)
        hsavec.saveRecorderGetExtensionU(
            self.hRecorder,
            extension_p,
            byref(length))

        return extension_p.value

    def PeekFileName(self):

        file_name_p = create_string_buffer(
            XSAVE_STR_BUF_SIZE_DEFAULT)
        length = size_t(XSAVE_STR_BUF_SIZE_DEFAULT)

        # SC_ERROR saveRecorderPeekFileName(
        #   saveRecorder hRecorder,
        #   char* pFileName,
        #   size_t* pLen)
        hsavec.saveRecorderPeekFileName(
            self.hRecorder,
            file_name_p,
            byref(length))

        return file_name_p.value.decode()

    # WINDOWS ONLY: UNICODE handling
    # in __init__ function this function will be assigned to
    # self.SetExtension so the upper levels have on function to call
    # and the unicode for windows is handled in the __init__
    def _PeekFileNameU(self):

        file_name_p = create_unicode_buffer(
            XSAVE_STR_BUF_SIZE_DEFAULT)
        length = size_t(XSAVE_STR_BUF_SIZE_DEFAULT)

        # SC_ERROR saveRecorderPeekFileNameU(
        #   saveRecorder hRecorder,
        #   wchar_t* pFileName,
        #   size_t* pLen)
        hsavec.saveRecorderPeekFileNameU(
            self.hRecorder,
            file_name_p,
            byref(length))

        return file_name_p.value

    def PeekCount(self):

        count = uint64_t(0)

        # SC_ERROR saveRecorderPeekCount(
        #   saveRecorder hRecorder,
        #   uint64_t* pCount)
        hsavec.saveRecorderPeekCount(
            self.hRecorder,
            byref(count))

        return count.value

    def PeekCountPath(self):

        count = uint64_t(0)

        # SC_ERROR saveRecorderPeekCountPath(
        #   saveRecorder hRecorder,
        #   uint64_t* pCount)
        hsavec.saveRecorderPeekCountPath(
            self.hRecorder,
            byref(count))

        return count.value

    def PeekCountGlobal(self):

        count = uint64_t(0)

        # SC_ERROR saveRecorderPeekCountGlobal(
        #   saveRecorder hRecorder,
        #   uint64_t* pCount)
        hsavec.saveRecorderPeekCountGlobal(
            self.hRecorder,
            byref(count))

        return count.value

    def GetLastFileName(self):

        file_name_p = create_string_buffer(
            XSAVE_STR_BUF_SIZE_DEFAULT)
        length = size_t(XSAVE_STR_BUF_SIZE_DEFAULT)

        # SC_ERROR saveRecorderGetLastFileName(
        #   saveRecorder hRecorder,
        #   char* pLastFileName,
        #   size_t* pLen)
        hsavec.saveRecorderGetLastFileName(
            self.hRecorder,
            file_name_p,
            byref(length))

        return file_name_p.value.decode()

    # WINDOWS ONLY: UNICODE handling
    # in __init__ function this function will be assigned to
    # self.SetExtension so the upper levels have on function to call
    # and the unicode for windows is handled in the __init__
    def _GetLastFileNameU(self):

        file_name_p = create_unicode_buffer(
            XSAVE_STR_BUF_SIZE_DEFAULT)
        length = size_t(XSAVE_STR_BUF_SIZE_DEFAULT)

        # SC_ERROR saveRecorderGetLastFileNameU(
        #   saveRecorder hRecorder,
        #   wchar_t* pLastFileName,
        #   size_t* pLen)
        hsavec.saveRecorderGetLastFileNameU(
            self.hRecorder,
            file_name_p,
            byref(length))

        return file_name_p.value

    def Open(self):

        # SC_ERROR saveRecorderOpen(
        #   saveRecorder hRecorder)
        hsavec.saveRecorderOpen(
            self.hRecorder)

    def AppendImage(self, pdata):

        # SC_ERROR saveRecorderAppendImage(
        #   saveRecorder hRecorder,
        #   uint8_t* pImageData)
        hsavec.saveRecorderAppendImage(
            self.hRecorder,
            pdata)

    def Close(self):

        # SC_ERROR saveRecorderClose(
        #   saveRecorder hRecorder)
        hsavec.saveRecorderClose(
            self.hRecorder)
