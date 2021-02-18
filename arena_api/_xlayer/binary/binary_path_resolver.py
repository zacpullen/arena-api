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
from pathlib import Path

from arena_api import arena_api_config
from arena_api._xlayer.info import Info

if 'Windows' in platform.system():
    import winreg


class BinaryPathResolverWindows:
    def __init__(self, config):
        self._config = config

        self._name_dll = self._config['name_dll']
        self._custom_pathname_r64 = None
        self._custom_pathname_r32 = None
        self._initialize_custom_vars()

        self._installation_pathname_r64 = None
        self._installation_pathname_r32 = None
        self._initialize_installation_vars()

    def _initialize_custom_vars(self):
        custom_pathnames_dict_name = self._config['custom_pathnames_dict_name']
        custom_pathnames = getattr(arena_api_config,
                                   custom_pathnames_dict_name)

        # 64 custom
        pathname64 = ''
        try:
            pathname64 = custom_pathnames['python64_win']

        except KeyError:
            raise KeyError(f'arena_api.arena_api_config.'
                           f'{custom_pathnames_dict_name} '
                           f'dict is missing \'python64_win\' key')

        if pathname64 != '':
            self._custom_pathname_r64 = Path(pathname64)

        # 32 custom
        pathname32 = ''
        try:
            pathname32 = custom_pathnames['python32_win']
        except KeyError:
            raise KeyError(f'arena_api.arena_api_config.'
                           f'{custom_pathnames_dict_name} '
                           f'dict is missing \'python32_win\' key')

        if pathname32 != '':
            self._custom_pathname_r32 = Path(pathname32)

    def _initialize_installation_vars(self):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Lucid Vision Labs\\Arena SDK') as key:
                # enable reflection if py32 ?
                # winreg.DisableReflectionKey(key)
                # winreg.EnableReflectionKey(key)

                root = winreg.QueryValueEx(key, 'InstallFolder')[0]
                if root == '':
                    raise OSError
                else:
                    root = Path(root)
                    self._installation_pathname_r64 = root / 'x64Release' / self._name_dll
                    self._installation_pathname_r32 = root / 'Win32Release' / self._name_dll
        except OSError:
            self._installation_pathname_r64 = None
            self._installation_pathname_r32 = None

    # repeated in PathResolverLinux
    def resolve(self):
        info = Info()

        if info.is_py64:

            # 64 custom win
            if self._custom_pathname_r64:
                return self._custom_pathname_r64
            # 64 installed win
            else:
                return self._installation_pathname_r64
        else:

            # 32 custom win
            if self._custom_pathname_r32:
                return self._custom_pathname_r32
            # 64 installed win
            else:
                return self._installation_pathname_r32


class BinaryPathResolverLinux:

    def __init__(self, config):
        self._config = config

        self._custom_pathname_r64 = None
        self._custom_pathname_r32 = None
        self._initialize_custom_vars()

        self._installation_pathname = None
        self._initialize_installation_vars()

    def _initialize_custom_vars(self):

        custom_pathnames_dict_name = self._config['custom_pathnames_dict_name']
        custom_pathnames = getattr(arena_api_config,
                                   custom_pathnames_dict_name)

        # 64 custom
        pathname64 = ''
        try:
            pathname64 = custom_pathnames['python64_lin']

        except KeyError:
            raise KeyError(f'arena_api.arena_api_config.'
                           f'{custom_pathnames_dict_name} '
                           f'dict is missing \'python64_lin\' key')

        if pathname64 != '':
            self._custom_pathname_r64 = Path(pathname64)

        # 32 custom
        pathname32 = ''
        try:
            pathname32 = custom_pathnames['python32_lin']
        except KeyError:
            raise KeyError(f'arena_api.arena_api_config.'
                           f'{custom_pathnames_dict_name} '
                           f'dict is missing \'python32_lin\' key')

        if pathname32 != '':
            self._custom_pathname_r32 = Path(pathname32)

    def _initialize_installation_vars(self):
        # TODO change this to use lddconfig -v

        arena_sdk_conf_pathname = Path('/etc/ld.so.conf.d/Arena_SDK.conf')
        if not arena_sdk_conf_pathname.exists():
            self._installation_pathname = None
            return

        # check all paths in file and try to find the shared obj in it
        potential_paths = arena_sdk_conf_pathname.read_text().split()
        name_so = self._config['name_so']
        for path in potential_paths:
            pathname = Path(path) / name_so
            if pathname.exists():
                # because only 64 or 32 can be installed on the system.
                # if it was found then we return the first shared lib found
                self._installation_pathname = pathname
                break

    # repeated in PathResolverWindows

    def resolve(self):
        info = Info()

        if info.is_py64:

            # 64 custom lin
            if self._custom_pathname_r64:
                return self._custom_pathname_r64
            # 64 installed lin
            else:
                return self._installation_pathname
        else:

            # 32 custom lin
            if self._custom_pathname_r32:
                return self._custom_pathname_r32
            # 32 installed lin
            else:
                return self._installation_pathname
        pass


class BinaryPathResolver:
    def __init__(self, config):

        self._config = config
        self._info = None
        self._path_resolver = None

        self._info = Info()
        if self._info.is_windows:
            self._path_resolver = BinaryPathResolverWindows(self._config)

        elif self._info.is_linux:
            self._path_resolver = BinaryPathResolverLinux(self._config)

    def resolve(self):
        return self._path_resolver.resolve()
