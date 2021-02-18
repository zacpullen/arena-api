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


_error_to_exception_dict = None
_get_msg_func = None


class BinaryFunctionReturnValueChecker:
    def __init__(self, error_to_exception_dict, get_msg_func):

        # very ugly idea , but it works
        global _error_to_exception_dict, _get_msg_func
        _error_to_exception_dict = error_to_exception_dict
        _get_msg_func = get_msg_func

    # must be static
    @staticmethod
    def raise_if_error(ret_err, raise_if_error, arguments):
        # because this is a static function that is used as sort of callback
        # when the binary function returns we need to expose the global
        # vars while using it
        global _error_to_exception_dict, _get_msg_func

        if _error_to_exception_dict[ret_err]:
            # not success
            msg = _get_msg_func(ret_err)
            raise _error_to_exception_dict[ret_err](msg)
