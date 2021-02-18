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

import ctypes as _ctypes

'''
#    C              | ArenaC  |  Py
# signed char         int8_t
# short               int16_t   c_short
# int                 int32_t   c_int
# long long           int64_t   c_longlong
# unsigned char       uint8_t   c_ubyte
# unsigned short      uint16_t  c_ushort
# unsigned int        uint32_t  c_uint
# unsigned long long  uint64_t  c_ulonglong
'''

# ctypes named to reflect Arenac types

void_ptr = _ctypes.c_void_p

bool8_t = _ctypes.c_bool

char = _ctypes.c_char
char_ptr = _ctypes.c_char_p

size_t = _ctypes.c_size_t

#int32_t = _ctypes.c_int
int64_t = _ctypes.c_longlong

uint8_t = _ctypes.c_ubyte
uint32_t = _ctypes.c_uint
uint64_t = _ctypes.c_ulonglong

double = _ctypes.c_double

acSystem = _ctypes.c_void_p
acDevice = _ctypes.c_void_p
acBuffer = _ctypes.c_void_p
acImage = _ctypes.c_void_p
acChunkdata = _ctypes.c_void_p
acNodeMap = _ctypes.c_void_p
acNode = _ctypes.c_void_p
acFeatureStream = _ctypes.c_void_p
acCallback = _ctypes.c_void_p
# the prototype of the function called by ArenaC when it makes the callback
acCallbackFunction = _ctypes.CFUNCTYPE(None, acNode, void_ptr)
# the prototype of the function called by ArenaC when it makes the callback
acImageCallbackFunction = _ctypes.CFUNCTYPE(None, acBuffer, void_ptr)

ac_error = _ctypes.c_int
ac_namespace = _ctypes.c_int
ac_visibility = _ctypes.c_int
ac_representation = _ctypes.c_int

ac_interface_type = _ctypes.c_int
ac_payload_type = _ctypes.c_int

ac_access_mode = _ctypes.c_int
ac_caching_mode = _ctypes.c_int
ac_inc_mode = _ctypes.c_int

ac_pixel_endianness = _ctypes.c_int
ac_bayer_algorithm = _ctypes.c_int
ac_display_notation = _ctypes.c_int
