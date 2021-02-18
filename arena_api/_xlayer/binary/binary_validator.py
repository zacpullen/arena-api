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

from arena_api._xlayer.info import Info

_info = Info()

'''


import subprocess



from arena_api import version
'''


if _info.is_windows:
    try:
        # pip install pywin32
        from win32api import (GetFileVersionInfo,
                              LOWORD,
                              HIWORD)
    except ImportError:
        raise ImportError(f'Please install packages in the requirements.txt\n'
                          f'run \'pip install pywin32\'')

if _info.is_linux:
    import os
    import subprocess
    from pathlib import Path


# path ------------------------------------------------------------------------


class PathValidator:
    #
    # cross platform
    #

    @staticmethod
    def validate(pathname):
        # checks needed to give correct error

        if not pathname:
            raise ValueError('pathname is None')

        # is dir
        if pathname.is_dir():
            raise ValueError(f'{pathname} is a directory path not a pathname to '
                             f'the binary file')

        # final does not exits
        if not pathname.is_file():  # checks if an existing file
            raise ValueError(
                f'{pathname} does not exist or is no a pathname to the binary file')

        # has correct extension and compatible with platform
        if (
            (_info.is_windows and pathname.suffixes[0] != '.dll') or
            (_info.is_linux and pathname.suffixes[0] != '.so')
        ):
            raise ValueError(f'{pathname} is not a binary file type ')


# platform --------------------------------------------------------------------


class PlatformValidatorWindows:
    def __init__(self):
        pass

    def validate(self, pathname):
        # TODO SFW-2813
        # win32 loads win64
        # https://github.com/tgandor/meats/blob/master/missing/arch_of.py
        # for now it fails to load only
        pass


class PlatformValidatorLinux:

    def validate(self, pathname):

        is_py64 = _info.is_py64
        is_arm = _info.is_arm
        is_arm64 = is_arm and is_py64
        is_arm32 = is_arm and not is_py64
        # shared obj

        is_arm64_binary = self._is_arm64_binary(pathname)
        is_arm32_binary = self._is_arm32_binary(pathname)
        is_arm_binary = is_arm64_binary or is_arm32_binary

        # regular linux loads arm64 or arm32
        if not is_arm and is_arm_binary:
            raise ValueError(f'\'{pathname}\' is an ARM binary.')

        # arm64 loads non arm
        elif is_arm64 and not is_arm_binary:
            raise ValueError(f'\'{pathname}\' is not an ARM binary.')

        # arm64 loads arm32
        elif is_arm64 and is_arm32_binary:
            raise ValueError(f'\'{pathname}\' is not a 64-bits ARM binary.')

        # arm32 loads non arm
        elif is_arm32 and not is_arm_binary:
            raise ValueError(f'\'{pathname}\' is not an ARM binary.')

        # arm32 loads arm64
        elif is_arm32 and is_arm64_binary:
            raise ValueError(f'\'{pathname}\' is not a 32-bits ARM binary.')

    def _is_arm64_binary(self, pathname):

        cmd_str = f'file {pathname} -L'

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

    def _is_arm32_binary(self, pathname):

        cmd_str = f'file {pathname} -L'

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

        # version ---------------------------------------------------------------------


# version ---------------------------------------------------------------------


class VersionValidatorWindows:

    def __init__(self, config):

        self._config = config

        self._USER_MIN_VERSION = self._config['user_min_version_win']
        self._USER_MAX_VERSION = self._config['user_max_version_win']

        self._CUSTOM_MIN_VERSION = self._config['custom_build_min_version_win']
        self._CUSTOM_MAX_VERSION = self._config['custom_build_max_version_win']

        self._LOCAL_VERSION = self._config['local_version_win']

    def validate(self, pathname):

        version_info = GetFileVersionInfo(str(pathname), '\\')
        ms = version_info['FileVersionMS']
        ls = version_info['FileVersionLS']
        arenac_version = (HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls))

        is_less_than_supported = arenac_version < self._USER_MIN_VERSION
        is_more_than_supported = arenac_version > self._USER_MAX_VERSION
        is_local_version = arenac_version == self._LOCAL_VERSION
        is_more_than_custom_min = arenac_version >= self._CUSTOM_MIN_VERSION
        is_less_than_custom_max = arenac_version <= self._CUSTOM_MAX_VERSION
        is_custom_version = is_more_than_custom_min and is_less_than_custom_max

        if is_local_version or is_custom_version:
            return

        if is_less_than_supported or is_more_than_supported:
            raise BaseException(f'trying to load ArenaC {arenac_version}\n'
                                f'ArenaC version must be >= {self._USER_MIN_VERSION}\n'
                                f'ArenaC version must be <= {self._USER_MAX_VERSION}\n')


class VersionValidatorLinux:

    def __init__(self, config):

        self._config = config
        # linux
        self._USER_MIN_VERSION = self._config['user_min_version_lin']
        self._USER_MAX_VERSION = self._config['user_max_version_lin']
        self._CUSTOM_MIN_VERSION = self._config['custom_build_min_version_lin']
        self._LOCAL_VERSION = self._config['local_version_lin']
        # arm
        self._USER_MIN_VERSION_ARM = self._config['user_min_version_arm']
        self._USER_MAX_VERSION_ARM = self._config['user_max_version_arm']
        self._CUSTOM_MIN_VERSION_ARM = self._config['custom_build_min_version_arm']
        self._LOCAL_VERSION_ARM = self._config['local_version_arm']

    def validate(self, pathname):

        version = self._get_version(pathname)

        info = Info()
        if info.is_arm:
            self._validate_arm(pathname, version)
        else:
            self._validate_linux(pathname, version)

    def _validate_linux(self, pathname, version):

        is_less_than_supported = version < self._USER_MIN_VERSION
        is_more_than_supported = version > self._USER_MAX_VERSION
        is_custom_version = version > self._CUSTOM_MIN_VERSION
        is_local_version = version == self._LOCAL_VERSION

        if is_local_version or is_custom_version:
            return

        if is_less_than_supported or is_more_than_supported:
            raise BaseException(f'trying to load ArenaC {version}\n'
                                f'ArenaC version must be >= {self._USER_MIN_VERSION}\n'
                                f'ArenaC version must be <= {self._USER_MAX_VERSION}\n')

    def _validate_arm(self, pathname, version):

        is_less_than_supported = version < self._USER_MIN_VERSION_ARM
        is_more_than_supported = version > self._USER_MAX_VERSION_ARM
        is_custom_version = version > self._LOCAL_VERSION_ARM
        is_local_version = version == self._CUSTOM_MIN_VERSION_ARM

        if is_local_version or is_custom_version:
            return

        if is_less_than_supported or is_more_than_supported:
            raise BaseException(f'trying to load ArenaC {version}\n'
                                f'ArenaC version must be >= {self._USER_MIN_VERSION_ARM}\n'
                                f'ArenaC version must be <= {self._USER_MAX_VERSION_ARM}\n')

    def _get_version(self, pathname):
        global _info
        # TODO potintial bugs in this function

        # prep
        # ex :
        # libarenc.so
        # libarenc.so.0
        # libarenc.so.0.0
        # libarenc.so.0.0.0

        # finds the target if it was a symlink
        parent = pathname.parent
        target_pathname = Path(os.path.realpath(pathname))

        if len(target_pathname.suffixes) == 1:  # not just .so
            # most likely that the sym link was copied from a windows machine or aws
            raise ValueError(f'{target_pathname} has no version or is not a '
                             f'valid symlink file')

        name_list = target_pathname.name.split('.')
        # removes 'libarenac' and 'so' from str
        version_units = len(name_list) - 2
        if version_units == 0 or version_units > 3:
            raise BaseException(
                f'{target_pathname} has {version_units} version units')

        version_numbers_str = name_list[2:]
        version_numbers = [int(_) for _ in version_numbers_str]

        return tuple(version_numbers)

# Binary Validator -------------------------------------------------------------------


class BinaryValidator:
    def __init__(self, config):
        global _info
        self._config = config

        self._path_validator = None
        self._platform_validator = None
        self._version_validator = None

        # path
        self._path_validator = PathValidator()
        # platform and version
        if _info.is_windows:
            self._platform_validator = PlatformValidatorWindows()
            self._version_validator = VersionValidatorWindows(self._config)
        elif _info.is_linux:
            self._platform_validator = PlatformValidatorLinux()
            self._version_validator = VersionValidatorLinux(self._config)

    def validate(self, pathname):
        # order matter
        self._path_validator.validate(pathname)
        self._platform_validator.validate(pathname)
        self._version_validator.validate(pathname)
