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

from ctypes import POINTER
from enum import Enum, unique

from arena_api._xlayer.binary.binary_function_return_value_checker import \
    BinaryFunctionReturnValueChecker
from arena_api._xlayer.info import Info
from arena_api._xlayer.xsave.savec_types import (char_ptr, double, saveReader,
                                                 saveRecorder, saveWriter,
                                                 sc_error, size_t, uint8_t,
                                                 uint64_t, wchar_ptr, bool8_t,
                                                 savePlyParams)

_info = Info()


@unique
class _SaveCError(Enum):
    SC_ERR_SUCCESS = 0
    SC_ERR_ERROR = -1001
    SC_ERR_NOT_INITIALIZED = -1002
    SC_ERR_NOT_IMPLEMENTED = -1003
    SC_ERR_RESOURCE_IN_USE = -1004
    SC_ERR_ACCESS_DENIED = -1005

    SC_ERR_INVALID_HANDLE = -1006
    SC_ERR_INVALID_ID = -1007
    SC_ERR_NO_DATA = -1008
    SC_ERR_INVALID_PARAMETER = -1009

    SC_ERR_IO = -1010
    SC_ERR_TIMEOUT = -1011
    SC_ERR_ABORT = -1012
    SC_ERR_INVALID_BUFFER = -1013
    SC_ERR_NOT_AVAILABLE = -1014

    SC_ERR_INVALID_ADDRESS = -1015
    SC_ERR_BUFFER_TOO_SMALL = -1016
    SC_ERR_INVALID_INDEX = -1017
    SC_ERR_PARSING_CHUNK_DATA = -1018
    SC_ERR_INVALID_VALUE = -1019
    SC_ERR_RESOURCE_EXHAUSTED = -1020
    SC_ERR_OUT_OF_MEMORY = -1021
    SC_ERR_BUSY = -1022
    SC_ERR_CUSTOM_ID = -10000


_error_to_exception_dict = {
    # success
    _SaveCError.SC_ERR_SUCCESS.value: None,

    # general
    _SaveCError.SC_ERR_ERROR.value: Exception,
    _SaveCError.SC_ERR_NOT_INITIALIZED.value: Exception,
    _SaveCError.SC_ERR_RESOURCE_IN_USE.value: Exception,
    _SaveCError.SC_ERR_BUSY.value: Exception,
    _SaveCError.SC_ERR_CUSTOM_ID.value: Exception,
    _SaveCError.SC_ERR_INVALID_ID.value: Exception,
    _SaveCError.SC_ERR_NO_DATA.value: Exception,
    _SaveCError.SC_ERR_ABORT.value: Exception,
    _SaveCError.SC_ERR_NOT_AVAILABLE.value: Exception,
    _SaveCError.SC_ERR_INVALID_ADDRESS.value: Exception,
    _SaveCError.SC_ERR_BUFFER_TOO_SMALL.value: Exception,
    _SaveCError.SC_ERR_PARSING_CHUNK_DATA.value: Exception,
    _SaveCError.SC_ERR_RESOURCE_EXHAUSTED.value: Exception,
    _SaveCError.SC_ERR_ACCESS_DENIED.value: Exception,

    # type error
    _SaveCError.SC_ERR_INVALID_HANDLE.value: TypeError,
    _SaveCError.SC_ERR_INVALID_PARAMETER.value: TypeError,

    # different
    _SaveCError.SC_ERR_NOT_IMPLEMENTED.value: NotImplementedError,
    _SaveCError.SC_ERR_IO.value: IOError,
    _SaveCError.SC_ERR_TIMEOUT.value: TimeoutError,
    _SaveCError.SC_ERR_INVALID_BUFFER.value: BufferError,
    _SaveCError.SC_ERR_INVALID_INDEX.value: IndexError,
    _SaveCError.SC_ERR_INVALID_VALUE.value: ValueError,
    _SaveCError.SC_ERR_OUT_OF_MEMORY.value: MemoryError,
}


def _get_msg_func(err):
    err = _SaveCError(err)
    error_msg = f'\t{err.name} {err.value}'
    boarder = '\n' + '*' * 100 + '\n'
    full_msg = f'\n\nSaveC ERROR :\n{error_msg}\n\n'
    return full_msg


class SaveCConfigurator:
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
        self._configure_reader()
        self._configure_writer()
        self._configure_recorder()
        # self._raiseifnotconfigured()

    #
    # reader
    #
    def _configure_reader(self):

        c_funcs_list = [
            self.handle.saveReaderCreate,
            self.handle.saveReaderCreateBottomToTop,
            self.handle.saveReaderDestroy,
            self.handle.saveReaderGetParams,
            self.handle.saveReaderGetData,
            self.handle.saveReaderLoadRawData
        ]

        # WINDOWS ONLY:
        #   These functions exists only in windows dlls
        #   handle UNICODE
        # self.handle.saveReaderCreateU
        # self.handle.saveReaderCreateBottomToTopU
        # self.handle.saveReaderLoadRawDataU
        if _info.is_windows:
            c_funcs_list.extend([
                self.handle.saveReaderCreateU,
                self.handle.saveReaderCreateBottomToTopU,
                self.handle.saveReaderLoadRawDataU,
            ])

        if _info.is_windows:
            # SC_ERROR saveReaderCreateU(
            #   saveReader* phReader,
            #   const wchar_t* pFileName)

            self.handle.saveReaderCreateU.argtypes = [
                POINTER(saveReader),
                wchar_ptr,
            ]

            # SC_ERROR saveReaderCreateBottomToTopU(
            #   saveReader* phReader,
            #   const wchar_t* pFileName)
            self.handle.saveReaderCreateBottomToTopU.argtypes = [
                POINTER(saveReader),
                wchar_ptr,
            ]

            # SC_ERROR saveReaderLoadRawDataU(
            #   const wchar_t* pFileName,
            #   uint8_t* pImageData,
            #   const size_t size);
            self.handle.saveReaderLoadRawDataU.argtypes = [
                wchar_ptr,
                POINTER(uint8_t),
                size_t,
            ]

        # ---------------------------------------------------------------------
        # DONE
        # ---------------------------------------------------------------------

        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        # SC_ERROR saveReaderCreate(
        #   saveReader* phReader,
        #   const char* pFileName)
        self.handle.saveReaderCreate.argtypes = [
            POINTER(saveReader),
            char_ptr
        ]

        # SC_ERROR saveReaderCreateBottomToTop(
        #   saveReader* phReader,
        #   const char* pFileName)
        self.handle.saveReaderCreateBottomToTop.argtypes = [
            POINTER(saveReader),
            char_ptr
        ]

        # SC_ERROR saveReaderDestroy(
        #   saveReader hReader)
        self.handle.saveReaderDestroy.argtypes = [
            saveReader
        ]

        # SC_ERROR saveReaderGetParams(
        #   saveReader hReader,
        #   size_t* pWidth,
        #   size_t* pHeight,
        #   size_t* pBitsPerPixel)
        self.handle.saveReaderGetParams.argtypes = [
            saveReader,
            POINTER(size_t),
            POINTER(size_t),
            POINTER(size_t)
        ]

        # SC_ERROR saveReaderGetData(
        #   saveReader hReader,
        #   uint8_t** ppData)
        self.handle.saveReaderGetData.argtypes = [
            saveReader,
            POINTER(POINTER(uint8_t))
        ]

        # SC_ERROR saveReaderLoadRawData(
        #   const char * pFileName,
        #   uint8_t * pImageData,
        #   const size_t size)
        self.handle.saveReaderLoadRawData.argtypes = [
            char_ptr,
            POINTER(uint8_t),
            size_t
        ]

    #
    # writer
    #
    def _configure_writer(self):
        c_funcs_list = [
            self.handle.saveWriterCreateEmpty,
            self.handle.saveWriterCreate,
            self.handle.saveWriterDestroy,
            self.handle.saveWriterSetJpeg,
            self.handle.saveWriterSetBmp,
            self.handle.saveWriterSetRaw,
            self.handle.saveWriterSetPly,
            # NOTE : saveWriterSetPlyAndConfig is ignored and this does its job
            self.handle.saveWriterSetPlyAndConfigExtended,
            self.handle.saveWriterSetTiff,
            self.handle.saveWriterSetPng,
            self.handle.saveWriterSetExtension,
            self.handle.saveWriterSetParams,
            self.handle.saveWriterSetFileNamePattern,
            self.handle.saveWriterUpdateTag,
            self.handle.saveWriterSetCount,
            self.handle.saveWriterSetCountPath,
            self.handle.saveWriterSetCountGlobal,
            self.handle.saveWriterSetTimestamp,
            self.handle.saveWriterGetParams,
            self.handle.saveWriterGetFileNamePattern,
            self.handle.saveWriterGetExtension,
            self.handle.saveWriterPeekFileName,
            self.handle.saveWriterPeekCount,
            self.handle.saveWriterPeekCountPath,
            self.handle.saveWriterPeekCountGlobal,
            self.handle.saveWriterGetLastFileName,
            self.handle.saveWriterSave,
            self.handle.saveWriterSaveWithColor,
            self.handle.saveWriterSaveBottomToTop
        ]
        # WINDOWS ONLY:
        #   These functions exists only in windows dlls
        #   handle UNICODE
        #   self.handle.saveWriterSetExtensionU
        #   self.handle.saveWriterSetFileNamePatternU
        #   self.handle.saveWriterUpdateTagU
        #   self.handle.saveWriterGetFileNamePatternU
        #   self.handle.saveWriterGetExtensionU
        #   self.handle.saveWriterPeekFileNameU
        #   self.handle.saveWriterGetLastFileNameU
        if _info.is_windows:
            c_funcs_list.extend([
                self.handle.saveWriterSetExtensionU,
                self.handle.saveWriterSetFileNamePatternU,
                self.handle.saveWriterUpdateTagU,
                self.handle.saveWriterGetFileNamePatternU,
                self.handle.saveWriterGetExtensionU,
                self.handle.saveWriterPeekFileNameU,
                self.handle.saveWriterGetLastFileNameU,
            ])

        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        if _info.is_windows:
            # SC_ERROR saveWriterSetExtensionU(
            #   saveWriter hWriter,
            #   const wchar_t* pExtension)
            self.handle.saveWriterSetExtensionU.argtypes = [
                saveWriter,
                wchar_ptr,
            ]

            # SC_ERROR saveWriterSetFileNamePatternU(
            #   saveWriter hWriter,
            #   const wchar_t* pFileNamePattern)
            self.handle.saveWriterSetFileNamePatternU.argtypes = [
                saveWriter,
                wchar_ptr,
            ]

            # SC_ERROR saveWriterUpdateTagU(
            #   saveWriter hWriter,
            #   const wchar_t* pTag,
            #   const wchar_t* pValue)
            self.handle.saveWriterUpdateTagU.argtypes = [
                saveWriter,
                wchar_ptr,
                wchar_ptr,
            ]

            # SC_ERROR saveWriterGetFileNamePatternU(
            #   saveWriter hWriter,
            #   wchar_t* pFileNamePattern,
            #   size_t* pLen)
            self.handle.saveWriterGetFileNamePatternU.argtypes = [
                saveWriter,
                wchar_ptr,
                POINTER(size_t),
            ]

            # SC_ERROR saveWriterGetExtensionU(
            #   saveWriter hWriter,
            #   wchar_t* pExtension,
            #   size_t* pLen)
            self.handle.saveWriterGetExtensionU.argtypes = [
                saveWriter,
                wchar_ptr,
                POINTER(size_t),
            ]

            # SC_ERROR saveWriterPeekFileNameU(
            #   saveWriter hWriter,
            #   wchar_t* pFileName,
            #   size_t* pLen)
            self.handle.saveWriterPeekFileNameU.argtypes = [
                saveWriter,
                wchar_ptr,
                POINTER(size_t),
            ]

            # SC_ERROR saveWriterGetLastFileNameU(
            #   saveWriter hWriter,
            #   wchar_t* pFileName,
            #   size_t* pLen)
            self.handle.saveWriterGetLastFileNameU.argtypes = [
                saveWriter,
                wchar_ptr,
                POINTER(size_t),
            ]

        # SC_ERROR saveWriterCreateEmpty(
        #   saveWriter* phWriter)
        self.handle.saveWriterCreateEmpty.argtypes = [
            POINTER(saveWriter)
        ]

        # SC_ERROR saveWriterCreate(
        #   size_t width,
        #   size_t height,
        #   size_t bitsPerPixel,
        #   saveWriter* phWriter)
        self.handle.saveWriterCreate.argtypes = [
            size_t,
            size_t,
            size_t,
            POINTER(saveWriter)
        ]

        # SC_ERROR saveWriterDestroy(
        #   saveWriter hWriter)
        self.handle.saveWriterDestroy.argtypes = [
            saveWriter
        ]

        # SC_ERROR saveWriterSetJpeg(
        #   saveWriter hWriter)
        self.handle.saveWriterSetJpeg.argtypes = [
            saveWriter
        ]

        # SC_ERROR saveWriterSetBmp(
        #   saveWriter hWriter)
        self.handle.saveWriterSetBmp.argtypes = [
            saveWriter
        ]

        # SC_ERROR saveWriterSetRaw(
        #   saveWriter hWriter)
        self.handle.saveWriterSetRaw.argtypes = [
            saveWriter
        ]

        # SC_ERROR saveWriterSetPly(
        #   saveWriter hWriter)
        self.handle.saveWriterSetPly.argtypes = [
            saveWriter
        ]

        # NOTE : saveWriterSetPlyAndConfig is ignored and this does its job
        # SC_ERROR saveWriterSetPlyAndConfigExtended(
        #   saveWriter hWriter
        #   savePlyParams params)
        self.handle.saveWriterSetPlyAndConfigExtended.argtypes = [
            saveWriter,
            savePlyParams
        ]

        # SC_ERROR saveWriterSetTiff(
        #   saveWriter hWriter)
        self.handle.saveWriterSetTiff.argtypes = [
            saveWriter
        ]

        # SC_ERROR saveWriterSetPng(
        #   saveWriter hWriter)
        self.handle.saveWriterSetPng.argtypes = [
            saveWriter
        ]

        # SC_ERROR saveWriterSetExtension(
        #   saveWriter hWriter,
        #   const char* pExtension)
        self.handle.saveWriterSetExtension.argtypes = [
            saveWriter,
            char_ptr
        ]

        # SC_ERROR saveWriterSetParams(
        #   saveWriter hWriter,
        #   size_t width,
        #   size_t height,
        #   size_t bitsPerPixel)
        self.handle.saveWriterSetParams.argtypes = [
            saveWriter,
            size_t,
            size_t,
            size_t
        ]

        # SC_ERROR saveWriterSetFileNamePattern(
        #   saveWriter hWriter,
        #   const char* pFileNamePattern)
        self.handle.saveWriterSetFileNamePattern.argtypes = [
            saveWriter,
            char_ptr
        ]

        # SC_ERROR saveWriterUpdateTag(
        #   saveWriter hWriter,
        #   const char* pTag,
        #   const char* pValue)
        self.handle.saveWriterUpdateTag.argtypes = [
            saveWriter,
            char_ptr,
            char_ptr
        ]

        # SC_ERROR saveWriterSetCount(
        #   saveWriter hWriter,
        #   uint64_t count)
        self.handle.saveWriterSetCount.argtypes = [
            saveWriter,
            uint64_t
        ]

        # SC_ERROR saveWriterSetCountPath(
        #   saveWriter hWriter,
        #   uint64_t count)
        self.handle.saveWriterSetCountPath.argtypes = [
            saveWriter,
            uint64_t

        ]

        # SC_ERROR saveWriterSetCountGlobal(
        #   saveWriter hWriter,
        #   uint64_t count)
        self.handle.saveWriterSetCountGlobal.argtypes = [
            saveWriter,
            uint64_t

        ]

        # SC_ERROR saveWriterSetTimestamp(
        #   saveWriter hWriter,
        #   uint64_t timestamp)
        self.handle.saveWriterSetTimestamp.argtypes = [
            saveWriter,
            uint64_t

        ]

        # SC_ERROR saveWriterGetParams(
        #   saveWriter hWriter,
        #   size_t* pWidth,
        #   size_t* pHeight,
        #   size_t* pBitsPerPixel)
        self.handle.saveWriterGetParams.argtypes = [
            saveWriter,
            POINTER(size_t),
            POINTER(size_t),
            POINTER(size_t),
        ]

        # SC_ERROR saveWriterGetFileNamePattern(
        #   saveWriter hWriter,
        #   char* pFileNamePattern,
        #   size_t* pLen)
        self.handle.saveWriterGetFileNamePattern.argtypes = [
            saveWriter,
            char_ptr,
            POINTER(size_t)
        ]

        # SC_ERROR saveWriterGetExtension(
        #   saveWriter hWriter,
        #   char* pExtension,
        #   size_t* pLen)
        self.handle.saveWriterGetExtension.argtypes = [
            saveWriter,
            char_ptr,
            POINTER(size_t)
        ]

        # SC_ERROR saveWriterPeekFileName(
        #   saveWriter hWriter,
        #   char* pFileName,
        #   size_t* pLen)
        self.handle.saveWriterPeekFileName.argtypes = [
            saveWriter,
            char_ptr,
            POINTER(size_t)
        ]

        # SC_ERROR saveWriterPeekCount(
        #   saveWriter hWriter,
        #   uint64_t* pCount)
        self.handle.saveWriterPeekCount.argtypes = [
            saveWriter,
            POINTER(uint64_t)
        ]

        # SC_ERROR saveWriterPeekCountPath(
        #   saveWriter hWriter,
        #   uint64_t* pCount)
        self.handle.saveWriterPeekCountPath.argtypes = [
            saveWriter,
            POINTER(uint64_t)
        ]

        # SC_ERROR saveWriterPeekCountGlobal(
        #   saveWriter hWriter,
        #   uint64_t* pCount)
        self.handle.saveWriterPeekCountGlobal.argtypes = [
            saveWriter,
            POINTER(uint64_t)
        ]

        # SC_ERROR saveWriterGetLastFileName(
        #   saveWriter hWriter,
        #   char* pFileName,
        #   size_t* pLen)
        self.handle.saveWriterGetLastFileName.argtypes = [
            saveWriter,
            char_ptr,
            POINTER(size_t)
        ]

        # SC_ERROR saveWriterSave(
        #   saveWriter hWriter,
        #   const uint8_t* pData)
        self.handle.saveWriterSave.argtypes = [
            saveWriter,
            POINTER(uint8_t)
        ]

        # SC_ERROR saveWriterSaveWithColor(
        #   saveWriter hWriter,
        #   const uint8_t* pData,
        #   const uint8_t* pColor,
        #   bool createDirectories)
        self.handle.saveWriterSaveWithColor.argtypes = [
            saveWriter,
            POINTER(uint8_t),
            POINTER(uint8_t),
            bool8_t
        ]

        # SC_ERROR saveWriterSaveBottomToTop(
        #   saveWriter hWriter,
        #   const uint8_t* pData)
        self.handle.saveWriterSaveBottomToTop.argtypes = [
            saveWriter,
            POINTER(uint8_t)
        ]

    #
    # recorder
    #
    def _configure_recorder(self):
        c_funcs_list = [
            self.handle.saveRecorderCreateEmpty,
            self.handle.saveRecorderCreate,
            self.handle.saveRecorderDestroy,
            self.handle.saveRecorderSetRaw,
            self.handle.saveRecorderSetRawAviBGR8,
            self.handle.saveRecorderSetRawMovRGB8,
            self.handle.saveRecorderSetH264MovRGB8,
            self.handle.saveRecorderSetH264MovBGR8,
            self.handle.saveRecorderSetH264Mp4RGB8,
            self.handle.saveRecorderSetH264Mp4BGR8,
            self.handle.saveRecorderSetParams,
            self.handle.saveRecorderSetFileNamePattern,
            self.handle.saveRecorderUpdateTag,
            self.handle.saveRecorderSetCount,
            self.handle.saveRecorderSetTimestamp,
            self.handle.saveRecorderGetParams,
            self.handle.saveRecorderGetFileNamePattern,
            self.handle.saveRecorderGetExtension,
            self.handle.saveRecorderPeekFileName,
            self.handle.saveRecorderPeekCount,
            self.handle.saveRecorderPeekCountPath,
            self.handle.saveRecorderPeekCountGlobal,
            self.handle.saveRecorderGetLastFileName,
            self.handle.saveRecorderOpen,
            self.handle.saveRecorderAppendImage,
            self.handle.saveRecorderClose
        ]

        # WINDOWS ONLY:
        #   These functions exists only in windows dlls
        #   handle UNICODE
        #   self.handle.saveRecorderSetFileNamePatternU,
        #   self.handle.saveRecorderUpdateTagU,
        #   self.handle.saveRecorderGetFileNamePatternU,
        #   self.handle.saveRecorderGetExtensionU,
        #   self.handle.saveRecorderPeekFileNameU,
        #   self.handle.saveRecorderGetLastFileNameU,
        if _info.is_windows:
            c_funcs_list.extend([
                self.handle.saveRecorderSetFileNamePatternU,
                self.handle.saveRecorderUpdateTagU,
                self.handle.saveRecorderGetFileNamePatternU,
                self.handle.saveRecorderGetExtensionU,
                self.handle.saveRecorderPeekFileNameU,
                self.handle.saveRecorderGetLastFileNameU,
            ])
        for func_ptr in c_funcs_list:
            func_ptr.errcheck = self.raise_if_error

        if _info.is_windows:
            # SC_ERROR saveRecorderSetFileNamePatternU(
            #   saveRecorder hRecorder,
            #   const wchar_t* pFileNamePattern);
            self.handle.saveRecorderSetFileNamePatternU.argtypes = [
                saveRecorder,
                wchar_ptr,
            ]

            # SC_ERROR saveRecorderUpdateTagU(
            #   saveRecorder hRecorder,
            #   const wchar_t* pTag,
            #   const wchar_t* pValue)
            self.handle.saveRecorderUpdateTagU.argtypes = [
                saveRecorder,
                wchar_ptr,
                wchar_ptr,
            ]

            # SC_ERROR saveRecorderGetFileNamePatternU(
            #   saveRecorder hRecorder,
            #   wchar_t* pFileNamePattern,
            #   size_t* pLen)
            self.handle.saveRecorderGetFileNamePatternU.argtypes = [
                saveRecorder,
                wchar_ptr,
                POINTER(size_t),
            ]

            # SC_ERROR saveRecorderGetExtensionU(
            #   saveRecorder hRecorder,
            #   wchar_t* pExtension,
            #   size_t* pLen)
            self.handle.saveRecorderGetExtensionU.argtypes = [
                saveRecorder,
                wchar_ptr,
                POINTER(size_t),
            ]

            # SC_ERROR saveRecorderPeekFileNameU(
            #   saveRecorder hRecorder,
            #   wchar_t* pFileName,
            #   size_t* pLen)
            self.handle.saveRecorderPeekFileNameU.argtypes = [
                saveRecorder,
                wchar_ptr,
                POINTER(size_t),
            ]

            # SC_ERROR saveRecorderGetLastFileNameU(
            #   saveRecorder hRecorder,
            #   wchar_t* pLastFileName,
            #   size_t* pLen)
            self.handle.saveRecorderGetLastFileNameU.argtypes = [
                saveRecorder,
                wchar_ptr,
                POINTER(size_t),
            ]
        # SC_ERROR saveRecorderCreateEmpty(
        #   saveRecorder* phRecorder)
        self.handle.saveRecorderCreateEmpty.argtypes = [
            POINTER(saveRecorder)
        ]

        # SC_ERROR saveRecorderCreate(
        #   size_t width,
        #   size_t height,
        #   double fps,
        #   saveRecorder* phRecorder)
        self.handle.saveRecorderCreate.argtypes = [
            size_t,
            size_t,
            double,
            POINTER(saveRecorder)
        ]

        # SC_ERROR saveRecorderDestroy(
        #   saveRecorder hRecorder)
        self.handle.saveRecorderDestroy.argtypes = [
            saveRecorder
        ]

        # SC_ERROR saveRecorderSetRaw(
        #   saveRecorder hRecorder,
        #   uint64_t pixelFormat)
        self.handle.saveRecorderSetRaw.argtypes = [
            saveRecorder,
            uint64_t
        ]

        # SC_ERROR saveRecorderSetRawAviBGR8(
        #   saveRecorder hRecorder)
        self.handle.saveRecorderSetRawAviBGR8.argtypes = [
            saveRecorder
        ]

        # SC_ERROR saveRecorderSetRawMovRGB8(
        #   saveRecorder hRecorder)
        self.handle.saveRecorderSetRawMovRGB8.argtypes = [
            saveRecorder
        ]

        # SC_ERROR saveRecorderSetH264MovRGB8(
        #   saveRecorder hRecorder)
        self.handle.saveRecorderSetH264MovRGB8.argtypes = [
            saveRecorder
        ]

        # SC_ERROR saveRecorderSetH264MovBGR8(
        #   saveRecorder hRecorder)
        self.handle.saveRecorderSetH264MovBGR8.argtypes = [
            saveRecorder
        ]

        # SC_ERROR saveRecorderSetH264Mp4RGB8(
        #   saveRecorder hRecorder)
        self.handle.saveRecorderSetH264Mp4RGB8.argtypes = [
            saveRecorder
        ]

        # SC_ERROR saveRecorderSetH264Mp4BGR8(
        #   saveRecorder hRecorder)
        self.handle.saveRecorderSetH264Mp4BGR8.argtypes = [
            saveRecorder
        ]

        # SC_ERROR saveRecorderSetParams(
        #   saveRecorder hRecorder,
        #   size_t width,
        #   size_t height,
        #   double fps)
        self.handle.saveRecorderSetParams.argtypes = [
            saveRecorder,
            size_t,
            size_t,
            double,
        ]

        # SC_ERROR saveRecorderSetFileNamePattern(
        #   saveRecorder hRecorder,
        #   const char* pFileNamePattern)
        self.handle.saveRecorderSetFileNamePattern.argtypes = [
            saveRecorder,
            char_ptr
        ]

        # SC_ERROR saveRecorderUpdateTag(
        #   saveRecorder hRecorder,
        #   const char* pTag,
        #   const char* pValue)
        self.handle.saveRecorderUpdateTag.argtypes = [
            saveRecorder,
            char_ptr,
            char_ptr
        ]

        # SC_ERROR saveRecorderSetCount(
        #   saveRecorder hRecorder,
        #   uint64_t count)
        self.handle.saveRecorderSetCount.argtypes = [
            saveRecorder,
            uint64_t
        ]

        #
        # TODO CHECK if this NEEDED
        #
        # SC_ERROR saveRecorderSetCountPath(
        #   saveRecorder hRecorder,
        #   uint64_t count)
        # self.handle.saveRecorderSetCountPath.argtypes = [
        #   saveRecorder
        #
        # ]

        #
        # TODO CHECK IF THIS NEEDED
        #
        # SC_ERROR saveRecorderSetCountGlobal(
        #   saveRecorder hRecorder,
        #   uint64_t count)
        # self.handle.saveRecorderSetCountGlobal.argtypes = [
        #
        # ]

        # SC_ERROR saveRecorderSetTimestamp(
        #   saveRecorder hRecorder,
        #   uint64_t timestamp)
        self.handle.saveRecorderSetTimestamp.argtypes = [
            saveRecorder,
            uint64_t
        ]

        # SC_ERROR saveRecorderGetParams(
        #   saveRecorder hRecorder,
        #   size_t* pWidth,
        #   size_t* pHeight,
        #   double* pFps)
        self.handle.saveRecorderGetParams.argtypes = [
            saveRecorder,
            POINTER(size_t),
            POINTER(size_t),
            POINTER(double)
        ]

        # SC_ERROR saveRecorderGetFileNamePattern(
        #   saveRecorder hRecorder,
        #   char* pFileNamePattern,
        #   size_t* pLen)
        self.handle.saveRecorderGetFileNamePattern.argtypes = [
            saveRecorder,
            char_ptr,
            POINTER(size_t)
        ]

        # SC_ERROR saveRecorderGetExtension(
        #   saveRecorder hRecorder,
        #   char* pExtension,
        #   size_t* pLen)
        self.handle.saveRecorderGetExtension.argtypes = [
            saveRecorder,
            char_ptr,
            POINTER(size_t)
        ]

        # SC_ERROR saveRecorderPeekFileName(
        #   saveRecorder hRecorder,
        #   char* pFileName,
        #   size_t* pLen)
        self.handle.saveRecorderPeekFileName.argtypes = [
            saveRecorder,
            char_ptr,
            POINTER(size_t)
        ]

        # SC_ERROR saveRecorderPeekCount(
        #   saveRecorder hRecorder,
        #   uint64_t* pCount)
        self.handle.saveRecorderPeekCount.argtypes = [
            saveRecorder,
            POINTER(uint64_t)
        ]

        # SC_ERROR saveRecorderPeekCountPath(
        #   saveRecorder hRecorder,
        #   uint64_t* pCount)
        self.handle.saveRecorderPeekCountPath.argtypes = [
            saveRecorder,
            POINTER(uint64_t)
        ]

        # SC_ERROR saveRecorderPeekCountGlobal(
        #   saveRecorder hRecorder,
        #   uint64_t* pCount)
        self.handle.saveRecorderPeekCountGlobal.argtypes = [
            saveRecorder,
            POINTER(uint64_t)
        ]

        # SC_ERROR saveRecorderGetLastFileName(
        #   saveRecorder hRecorder,
        #   char* pLastFileName,
        #   size_t* pLen)
        self.handle.saveRecorderGetLastFileName.argtypes = [
            saveRecorder,
            char_ptr,
            POINTER(size_t)
        ]

        # SC_ERROR saveRecorderOpen(
        #   saveRecorder hRecorder)
        self.handle.saveRecorderOpen.argtypes = [
            saveRecorder
        ]

        # SC_ERROR saveRecorderAppendImage(
        #   saveRecorder hRecorder,
        #   uint8_t* pImageData)
        self.handle.saveRecorderAppendImage.argtypes = [
            saveRecorder,
            POINTER(uint8_t)
        ]

        # SC_ERROR saveRecorderClose(
        #   saveRecorder hRecorder)
        self.handle.saveRecorderClose.argtypes = [
            saveRecorder
        ]
