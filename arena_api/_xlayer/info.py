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

import platform
import struct
import subprocess


class Info():

    __singleton = None
    __run_init = True

    def __new__(cls, *args, **kwargs):

        if not cls.__singleton:
            cls.__singleton = super(Info, cls).__new__(
                cls, *args, **kwargs)
        return cls.__singleton

    def __init__(self):
        # load once
        if not self.__run_init:
            return
        else:
            self.__run_init = False

        self.is_windows = self._get_is_windows()
        self.is_linux = self._get_is_linux()
        self.is_arm = self._get_is_arm()
        self.is_py64 = self._get_is_py64()

    def _get_is_windows(self):
        return 'Windows' in platform.system()

    def _get_is_linux(self):
        # both arm and regular linux will return 'Linux'
        return 'Linux' in platform.system()

    def _get_is_arm(self):

        if not self.is_linux:
            return False

        cmd_str = 'cat /proc/cpuinfo | grep \'model name\''
        complete_process = subprocess.run(cmd_str,
                                          shell=True,
                                          stdout=subprocess.PIPE,
                                          encoding='utf-8')
        model_name_line = complete_process.stdout.split('\n')[0]

        # example format
        # model name      : Intel(R) Core(TM) i7-7700 CPU @ 3.60GHz

        # ['model name      ', ' Intel(R) Core(TM) i7-7700 CPU @ 3.60GHz']
        model_name_line_as_list = model_name_line.split(':')
        # 'Intel(R) Core(TM) i7-7700 CPU @ 3.60GHz'
        model_name_value = model_name_line_as_list[-1].strip()
        # ['Intel(R)', 'Core(TM) i7-7700 CPU @ 3.60GHz']
        model_name_value_split_by_space_list = model_name_value.split(' ', 1)
        # 'Intel(R)'
        model_name_value_first = model_name_value_split_by_space_list[0]

        return True if 'arm' in model_name_value_first.lower() else False

    def _get_is_py64(self):
        return False if ((struct.calcsize('P') * 8) == 32) else True

    # shared obj --------------------------------------------------------------
    def is_so_64(self, path_to_so):
        if not self.is_linux:
            return False

        cmd_str = f'file {path_to_so} -L'

        complete_process = subprocess.run(cmd_str,
                                          shell=True,
                                          stdout=subprocess.PIPE,
                                          encoding='utf-8')
        # output example
        # temp/lib/libarenac.so: ELF 64-bit LSB shared object, ARM
        # aarch64, version 1 (SYSV), dynamically linked, BuildID[sha1]=
        # 682bf5f106153a181e7a381512a442232348d935, not stripped
        output = complete_process.stdout
        return True if '64-bit' in output else False

    def is_so_64_arm(self, path_to_so):
        # file command runs on both. the platform does not have to be arm
        # to check the binary type
        if not self.is_linux:
            return False

        cmd_str = f'file {path_to_so} -L'

        complete_process = subprocess.run(cmd_str,
                                          shell=True,
                                          stdout=subprocess.PIPE,
                                          encoding='utf-8')
        # output example
        # temp/lib/libarenac.so: ELF 64-bit LSB shared object, ARM
        # aarch64, version 1 (SYSV), dynamically linked, BuildID[sha1]=
        # 682bf5f106153a181e7a381512a442232348d935, not stripped
        output = complete_process.stdout
        is_64 = True if ' 64-bit ' in output else False
        is_arm = True if ' ARM' in output else False
        return is_64 and is_arm

    def is_so_32_arm(self, path_to_so):
        # file command runs on both. the platform does not have to be arm
        # to check the binary type
        if not self.is_linux:
            return False

        cmd_str = f'file {path_to_so} -L'

        complete_process = subprocess.run(cmd_str,
                                          shell=True,
                                          stdout=subprocess.PIPE,
                                          encoding='utf-8')
        # output example
        # temp/lib/libarenac.so: ELF 64-bit LSB shared object, ARM
        # aarch64, version 1 (SYSV), dynamically linked, BuildID[sha1]=
        # 682bf5f106153a181e7a381512a442232348d935, not stripped
        output = complete_process.stdout
        is_32 = True if ' 32-bit ' in output else False
        is_arm = True if ' ARM' in output else False
        return is_32 and is_arm

    def is_so_arm(self, path_to_so):
        return True if self.is_so_64_arm(path_to_so) or self.is_so_32_arm(path_to_so) else False

    # dll ---------------------------------------------------------------------
    def is_dll_64(self, path_to_so):
        if not self.is_dll:
            return False
        # TODO

    def is_dll_32(self, path_to_so):
        if not self.is_dll:
            return False
        # TODO

    def is_dll(self, path_to_so):
        return True if '.dll' in path_to_so.name else False
