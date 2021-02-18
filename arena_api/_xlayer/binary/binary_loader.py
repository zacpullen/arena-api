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

import os
from ctypes import CDLL, RTLD_GLOBAL

from arena_api._xlayer.info import Info

_info = Info()

if _info.is_linux:
    from pathlib import Path


class BinaryLoaderWindows:

    def load(self, pathname,
             config):  # config would not be used; it is there for linux

        original_work_dir = os.getcwd()
        os.chdir(pathname.parent)

        handle = CDLL(str(pathname))

        os.chdir(original_work_dir)

        return handle


class BinaryLoaderLinux:

    def load(self, pathname, config):

        global _info
        dependencies_sos = None

        # linux 64
        if not _info.is_arm:  # 32 linux is only arm
            dependencies_sos = config['dependencies_sos_lin']

        # arm 64
        elif _info.is_arm and _info.is_py64:
            dependencies_sos = config['dependencies_sos_arm64']

        # arm 32
        elif _info.is_arm and not _info.is_py64:
            dependencies_sos = config['dependencies_sos_armhf']

        bin_root = pathname.parent
        for so_relative_pathname in dependencies_sos:
            so_relative_pathname = (bin_root/so_relative_pathname).resolve()
            CDLL(str(so_relative_pathname), mode=RTLD_GLOBAL)

        handle = CDLL(pathname, mode=RTLD_GLOBAL)
        return handle


class BinaryLoader:
    def __init__(self, config):

        global _info
        self._config = config
        self._loader = None

        if _info.is_windows:
            self._loader = BinaryLoaderWindows()
        else:
            self._loader = BinaryLoaderLinux()

    def load(self, pathname):
        return self._loader.load(pathname, self._config)
