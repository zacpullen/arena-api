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

from arena_api._xlayer.xsave.savec_configurator import SaveCConfigurator
from arena_api._xlayer.binary.binary import Binary
from arena_api._xlayer.binary.binary_loader import BinaryLoader
from arena_api.version import supported_dll_versions

_config = {
    'name': 'SaveC',
    'name_dll': 'SaveC_v140.dll',  # TODO check if the path validator has name checker
    'name_so': 'libsavec.so',
    # from arena_api.arena_api_config module
    'custom_pathnames_dict_name': 'SAVEC_CUSTOM_PATHS',

    # versions

    # windows
    'user_min_version_win': None,
    'user_max_version_win': None,
    'custom_build_min_version_win': (0, 0, 0, 9999),
    'custom_build_max_version_win': (0, 0, 999, 9999),
    'local_version_win': (0, 1, 0, 0),

    # linux
    'user_min_version_lin': None,
    'user_max_version_lin': None,
    'custom_build_min_version_lin': (999, 0, 0),
    'local_version_lin': (0, 1, 0),

    # arm
    'user_min_version_arm': None,
    'user_max_version_arm': None,
    'custom_build_min_version_arm': (999, 0, 0),
    'local_version_arm': (0, 1, 0),

    # all paths are relative to the 'libsavec.so' file
    'dependencies_sos_lin': [
        # NOTE : CHANGES HERE WILL APPLY TO ARM AS WELL TEST IT
        # keep order

        # ffmpeg folder --------------------------------------------------------------

        # not used
        # '../ffmpeg/libavcodec.so',
        # '../ffmpeg/libavutil.so',
        # '../ffmpeg/libpostproc.so',
        # '../ffmpeg/libswresample.so',
        # '../ffmpeg/libswscale.so',

        # must be loaded
        # One of ( i dont know the diff)
        '../ffmpeg/libavformat.so',  # solves missing avformat_new_stream

        # lib64 folder ---------------------------------------------------------------
        'libsave.so'
    ],
    'dependencies_sos_arm64': [
        # same as 'dependencies_sos_lin'
    ],
    'dependencies_sos_armhf': [
        # same as 'dependencies_sos_lin'
    ]
}


_config['user_min_version_win'] = supported_dll_versions['windows'][_config['name']]['min']
_config['user_max_version_win'] = supported_dll_versions['windows'][_config['name']]['max']

_config['user_min_version_lin'] = supported_dll_versions['linux'][_config['name']]['min']
_config['user_max_version_lin'] = supported_dll_versions['linux'][_config['name']]['max']

_config['user_min_version_arm'] = supported_dll_versions['arm'][_config['name']]['min']
_config['user_max_version_arm'] = supported_dll_versions['arm'][_config['name']]['max']

_config['dependencies_sos_arm64'] = _config['dependencies_sos_lin']
_config['dependencies_sos_armhf'] = _config['dependencies_sos_lin']

_savec_binary = Binary(_config)
_configurator = SaveCConfigurator(_savec_binary.hbinary)
_configurator.configure()

hsavec = _savec_binary.hbinary
