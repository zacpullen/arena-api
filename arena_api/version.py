
import subprocess

from arena_api._xlayer.info import Info as _Info

__info = _Info()

# supported_dll_versions ------------------------------------------------------


def __get_this_platform_dll_versions():

    if __info.is_windows:
        returned_dict = supported_dll_versions['windows']
    elif __info.is_arm:
        returned_dict = supported_dll_versions['arm']
    elif __info.is_linux:
        returned_dict = supported_dll_versions['linux']
    else:
        raise Exception('internal : unsupported platform')

    return returned_dict


supported_dll_versions = {
    'windows': {
        'ArenaC':
        {
            'min': (1, 0, 24, 7),
            'max': (1, 999, 999, 999),
        }
    },

    'linux': {
        'ArenaC':
        {
            'min': (0, 1, 38),
            'max': (0, 999, 999),
        }
    },
    # linux on arm
    'arm': {
        'ArenaC':
        {
            'min': (0, 1, 24),
            'max': (0, 999, 999),
        }
    },

    'this_platform': None
}
supported_dll_versions['this_platform'] = __get_this_platform_dll_versions()

# SaveC is built with ArenaC so they have the same version
for platform in supported_dll_versions.keys():
    supported_dll_versions[platform]['SaveC'] = supported_dll_versions[platform]['ArenaC']


# __version__ -----------------------------------------------------------------

def __get_version_from_pip():
    try:
        raw = subprocess.check_output(['pip', 'show', '-V', 'arena_api'],
                                      encoding='UTF-8')
    except FileNotFoundError:
        try:
            raw = subprocess.check_output(['pip3', 'show', '-V', 'arena_api'],
                                          encoding='UTF-8')
        except FileNotFoundError:
            raise Exception('arena_api requires \'pip\' to be available at '
                            'runtime to get arena_api.__version__ value. ')

    version_number = raw.split()[3]
    return version_number


__version__ = __get_version_from_pip()
