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

from arena_api import _node
from arena_api.enums import InterfaceType as _InterfaceType


def cast_from_general_node_to_specific_node_type(base_node):

    node_type = base_node.interface_type
    specific_node = None
    hxnode = base_node.xnode.hxnode.value

    # string node
    if node_type == _InterfaceType.STRING:
        specific_node = _node.NodeString(hxnode)

    # integer
    elif node_type == _InterfaceType.INTEGER:
        specific_node = _node.NodeInteger(hxnode)

    # float
    elif node_type == _InterfaceType.FLOAT:
        specific_node = _node.NodeFloat(hxnode)

    # boolean
    elif node_type == _InterfaceType.BOOLEAN:
        specific_node = _node.NodeBoolean(hxnode)

    # enumeration
    elif node_type == _InterfaceType.ENUMERATION:
        specific_node = _node.NodeEnumeration(hxnode)

    # enumentry
    elif node_type == _InterfaceType.ENUMENTRY:
        specific_node = _node.NodeEnumentry(hxnode)

    # register
    elif node_type == _InterfaceType.REGISTER:
        specific_node = _node.NodeRegister(hxnode)

    # command
    elif node_type == _InterfaceType.COMMAND:
        specific_node = _node.NodeCommand(hxnode)

    # category
    elif node_type == _InterfaceType.CATEGORY:
        specific_node = _node.NodeCategory(hxnode)

    else:
        raise TypeError('Undefined interface type: failed to convert')

    return specific_node
