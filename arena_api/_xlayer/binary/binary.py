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

from arena_api._xlayer.binary.binary_loader import BinaryLoader
from arena_api._xlayer.binary.binary_path_resolver import BinaryPathResolver
from arena_api._xlayer.binary.binary_validator import BinaryValidator
from arena_api._xlayer.info import Info


class Binary:

    def __init__(self, config):

        # attr
        self._config = config
        path_resolver = None
        validator = None
        loader = None

        # start
        info = Info()
        if not info.is_windows and not info.is_linux:
            raise BaseException('unsupported platform')

        # get binary path
        path_resolver = BinaryPathResolver(self._config)
        pathname = path_resolver.resolve()
        if not pathname:
            name = self._config['name']
            raise BaseException(f'Please install {name} or add a custom path '
                                f'to {name} library binary '
                                f'in \'arena_api_config.py\'')

        # validate path
        # validate platform
        # validate version
        validator = BinaryValidator(self._config)
        validator.validate(pathname)

        # load
        loader = BinaryLoader(self._config)
        self.hbinary = loader.load(pathname)
