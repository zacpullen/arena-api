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
import enum

from arena_api import _node_helpers
from arena_api import enums as _enums
from arena_api._xlayer.xarena._xcallback import _xCallback
from arena_api._xlayer.xarena._xglobal import _xGlobal
from arena_api._xlayer.xarena._xnode import (_xBoolean, _xCategory, _xCommand,
                                             _xEnumentry, _xEnumeration,
                                             _xFloat, _xInteger, _xNode,
                                             _xRegister, _xSelector, _xString)


def __base_node__repr__(node):

    try:
        name = node.name
    except:
        name = 'N/A'

    try:
        description = node.description
    except:
        description = 'N/A'

    try:
        interface_type_value = node.interface_type.value
        interface_type_name = str(node.interface_type)
    except:
        interface_type_value = 'N/A'
        interface_type_name = 'N/A'

    try:
        access_mode_value = node.access_mode.value
        access_mode_name = str(node.access_mode)
    except:
        access_mode_value = 'N/A'
        access_mode_name = 'N/A'

    return (
        f'\n{name}'
        f'\n\tdescription  =  \"{description}\"'
        f'\n\ttype  =  <{interface_type_name}: {interface_type_value}>'
        f'\n\taccess_mode  =  <{access_mode_name}: {access_mode_value}>'
    )


class Node():

    def __repr__(self):
        return __base_node__repr__(self)

    def __init__(self, xhnode):
        self.xnode = _xNode(xhnode)
        self.__child_nodes = {}
        self.__parent_nodes = {}

    def __eq__(self, other):
        # for testing sometimes we dont need the same node when we choose
        # two random nodes
        if isinstance(other, Node):
            return self.xnode.hxnode.value == other.xnode.hxnode.value
        return False

    # helper --------------------------------------------------------------
    # TODO SFW-2179
    def __raise_type_error_if_not_expected_type(self, value, expected_type):
        if not isinstance(value, expected_type):
            raise TypeError(
                f'{expected_type.__name__} '
                f'expected instead of {type(value).__name__}')

    # ---------------------------------------------------------------------

    def __get_access_mode(self):

        access_mode = self.xnode.xNodeGetAccessMode()
        return _enums.AccessMode(access_mode)

    # TODO SFW-1958
    # TODO SFW-2027
    def __set_access_mode(self, access_mode):

        if isinstance(access_mode, str):
            access_mode = _enums.AccessMode[access_mode]

        self.xnode.xNodeImposeAccessMode(access_mode)

    access_mode = property(__get_access_mode, __set_access_mode)

    # ---------------------------------------------------------------------

    def __get_visibility(self):
        visibility = self.xnode.xNodeGetVisibility()
        return _enums.Visibility(visibility)

    # TODO SFW-1958
    # TODO SFW-2545
    def __set_visibility(self, visibility):

        if isinstance(visibility, str):
            visibility = _enums.Visibility[visibility]

        self.xnode.xNodeImposeVisibility(visibility)

    visibility = property(__get_visibility, __set_visibility)

    # ---------------------------------------------------------------------

    def __get_caching_mode(self):
        caching_mode = self.xnode.xNodeGetCachingMode()
        return _enums.CachingMode(caching_mode)

    caching_mode = property(__get_caching_mode)

    # ---------------------------------------------------------------------

    def __get_alias_node(self):
        hxNode = self.xnode.xNodeGetAlias()
        if not hxNode:
            return None
        alias_node_base = Node(hxNode)
        alias_node_specific = _node_helpers.cast_from_general_node_to_specific_node_type(
            alias_node_base)
        return alias_node_specific

    alias_node = property(__get_alias_node)

    # ---------------------------------------------------------------------

    def __get_cast_alias_node(self):
        hxNode = self.xnode.xNodeGetCastAlias()
        if not hxNode:
            return None
        node_base = Node(hxNode)
        alias_node_specific = _node_helpers.cast_from_general_node_to_specific_node_type(
            node_base)
        return alias_node_specific

    cast_alias_node = property(__get_cast_alias_node)
    # ---------------------------------------------------------------------

    def __get_description(self):
        return self.xnode.xNodeGetDescription()

    description = property(__get_description)

    # ---------------------------------------------------------------------

    def __get_device_name(self):
        return self.xnode.xNodeGetDeviceName()

    device_name = property(__get_device_name)

    # ---------------------------------------------------------------------
    def __get_display_name(self):
        return self.xnode.xNodeGetDisplayName()

    display_name = property(__get_display_name)

    # ---------------------------------------------------------------------

    def __get_docu_url(self):
        return self.xnode.xNodeGetDocuURL()

    docu_url = property(__get_docu_url)

    # ---------------------------------------------------------------------

    def __get_event_id(self):
        return self.xnode.xNodeGetEventID()

    event_id = property(__get_event_id)

    # ---------------------------------------------------------------------

    def __get_name(self):
        return self.xnode.xNodeGetName()

    name = property(__get_name)

    # ---------------------------------------------------------------------

    def __get_fully_qualified_name(self):
        return self.xnode.xNodeGetFullyQualifiedName()

    fully_qualified_name = property(__get_fully_qualified_name)

    # ---------------------------------------------------------------------

    def __get_namespace(self):
        namespace = self.xnode.xNodeGetNamespace()
        return _enums.Namespace(namespace)

    namespace = property(__get_namespace)

    # ---------------------------------------------------------------------

    def __get_polling_time(self):
        return self.xnode.xNodeGetPollingTime()

    polling_time = property(__get_polling_time)

    # ---------------------------------------------------------------------

    def __get_interface_type(self):
        interface_type = self.xnode.xNodeGetPrincipalInterfaceType()
        return _enums.InterfaceType(interface_type)

    interface_type = property(__get_interface_type)

    # ---------------------------------------------------------------------

    def __get_tool_tip(self):
        return self.xnode.xNodeGetToolTip()

    tool_tip = property(__get_tool_tip)

    # ---------------------------------------------------------------------

    def __get_is_cachable(self):
        return self.xnode.xNodeIsCachable()

    is_cachable = property(__get_is_cachable)

    # ---------------------------------------------------------------------

    def __get_is_deprecated(self):
        return self.xnode.xNodeIsDeprecated()

    is_deprecated = property(__get_is_deprecated)

    # ---------------------------------------------------------------------

    def __get_is_feature(self):
        return self.xnode.xNodeIsFeature()

    is_feature = property(__get_is_feature)

    # ---------------------------------------------------------------------

    def __get_is_readable(self):
        return _xGlobal.xIsReadable(self.xnode.hxnode.value)

    is_readable = property(__get_is_readable)

    # ---------------------------------------------------------------------

    def __get_is_writable(self):
        return _xGlobal.xIsWritable(self.xnode.hxnode.value)

    is_writable = property(__get_is_writable)

    # Other ---------------------------------------------------------------

    def invalidate_node(self):
        return self.xnode.xNodeInvalidateNode()

    # Property ------------------------------------------------------------

    def __get_properties(self):

        num_of_names = self.xnode.xNodeGetNumPropertyNames()

        # keys
        names = map(self.xnode.xNodeGetPropertyName, range(num_of_names))

        # values
        info = {}
        for name in names:

            property_value, property_attributes = self.xnode.xNodeGetProperty(
                name)
            # list of attributes separated by a tab character
            property_attributes = property_attributes.split('\t')
            property_attributes = list(
                filter(lambda str_: str_ != '', property_attributes))

            info[name] = {'value': property_value,
                          'attributes': property_attributes}

        return info
    properties = property(__get_properties)


class NodeString(Node):

    def __init__(self, hxnode):
        super().__init__(hxnode)
        self.xstring = _xString(hxnode)

    def __repr__(self):
        base_node_info = __base_node__repr__(self)

        try:
            value = self.value
            if value == '':
                value == '\"\"'
        except:
            value = 'N/A'

        return (
            f'{base_node_info}'
            f'\n\tvalue  =  \"{value}\"'
        )

    # TODO SFW-2179
    def __raise_type_error_if_not_expected_type(self, value, expected_type):
        if not isinstance(value, expected_type):
            raise TypeError(
                f'{expected_type.__name__} '
                f'expected instead of {type(value).__name__}')

    # value ---------------------------------------------------------------

    def __get_value(self):
        return self.xstring.xStringGetValue()

    def __set_value(self, value):
        self.__raise_type_error_if_not_expected_type(value, str)
        self.xstring.xStringSetValue(value)

    value = property(__get_value, __set_value)


class NodeInteger(Node):

    def __repr__(self):
        base_node_info = __base_node__repr__(self)

        try:
            value = self.value
        except:
            value = 'N/A'

        try:
            min_val = self.min
        except:
            min_val = 'N/A'

        try:
            max_val = self.max
        except:
            max_val = 'N/A'

        try:
            inc_val = self.inc_value
        except:
            inc_val = 'N/A'

        try:
            unit_val = self.unit

        except:
            unit_val = 'N/A'

        return (
            f'{base_node_info}'
            f'\n\tvalue  =  {value}'
            f'\n\tmin  =  {min_val}'
            f'\n\tmax  =  {max_val}'
            f'\n\tinc  =  {inc_val}'
            f'\n\tunit  = \"{unit_val}\"'
        )

    def __init__(self, hxnode):
        super().__init__(hxnode)
        self.xinteger = _xInteger(hxnode)

    # TODO SFW-2179
    def __raise_type_error_if_not_expected_type(self, value, expected_type):
        if not isinstance(value, expected_type):
            raise TypeError(
                f'{expected_type.__name__} '
                f'expected instead of {type(value).__name__}')

    # ---------------------------------------------------------------------

    def __get_value(self):
        return self.xinteger.xIntegerGetValue()

    def __set_value(self, value):
        self.__raise_type_error_if_not_expected_type(value, int)
        self.xinteger.xIntegerSetValue(value)

    value = property(__get_value, __set_value)

    # ---------------------------------------------------------------------

    def __get_min(self):
        return self.xinteger.xIntegerGetMin()

    def __set_min(self, value):
        self.__raise_type_error_if_not_expected_type(value, int)
        self.xinteger.xIntegerImposeMin(value)

    min = property(__get_min, __set_min)

    # ---------------------------------------------------------------------

    def __get_max(self):
        return self.xinteger.xIntegerGetMax()

    def __set_max(self, value):
        self.__raise_type_error_if_not_expected_type(value, int)
        self.xinteger.xIntegerImposeMax(value)

    max = property(__get_max, __set_max)

    # ---------------------------------------------------------------------

    def __get_inc(self):
        return self.xinteger.xIntegerGetInc()

    inc = property(__get_inc)

    # ---------------------------------------------------------------------

    def __get_inc_mode(self):
        inc_mode = self.xinteger.xIntegerGetIncMode()
        return _enums.IncMode(inc_mode)

    inc_mode = property(__get_inc_mode)

    # ---------------------------------------------------------------------

    def __get_representation(self):
        representation = self.xinteger.xIntegerGetRepresentation()
        return _enums.Representation(representation)

    representation = property(__get_representation)

    # ---------------------------------------------------------------------

    def __get_unit(self):
        return self.xinteger.xIntegerGetUnit()

    unit = property(__get_unit)


class NodeFloat(Node):

    def __repr__(self):
        base_node_info = __base_node__repr__(self)

        try:
            value = self.value
        except:
            value = 'N/A'

        try:
            min_val = self.min
        except:
            min_val = 'N/A'

        try:
            max_val = self.max
        except:
            max_val = 'N/A'

        try:
            inc_val = self.inc_value
        except:
            inc_val = 'N/A'

        try:
            unit_val = self.unit

        except:
            unit_val = 'N/A'

        return (
            f'{base_node_info}'
            f'\n\tvalue  =  {value}'
            f'\n\tmin  =  {min_val}'
            f'\n\tmax  =  {max_val}'
            f'\n\tinc  =  {inc_val}'
            f'\n\tunit  = \"{unit_val}\"'
        )

    def __init__(self, hxnode):
        super().__init__(hxnode)
        self.xfloat = _xFloat(hxnode)

    # TODO SFW-2179
    # TODO SFW-2537
    def __raise_type_error_if_not_expected_type(self, value, expected_type):
        if not isinstance(value, expected_type):
            raise TypeError(
                f'{expected_type.__name__} '
                f'expected instead of {type(value).__name__}')
    # ---------------------------------------------------------------------

    def __get_value(self):
        return self.xfloat.xFloatGetValue()

    def __set_value(self, value):
        self.__raise_type_error_if_not_expected_type(value, float)
        self.xfloat.xFloatSetValue(value)

    value = property(__get_value, __set_value)

    # ---------------------------------------------------------------------

    def __get_min(self):
        return self.xfloat.xFloatGetMin()

    def __set_min(self, value):
        self.__raise_type_error_if_not_expected_type(value, float)
        self.xfloat.xFloatImposeMin(value)

    min = property(__get_min, __set_min)

    # ---------------------------------------------------------------------

    def __get_max(self):
        return self.xfloat.xFloatGetMax()

    def __set_max(self, value):
        self.__raise_type_error_if_not_expected_type(value, float)
        self.xfloat.xFloatImposeMax(value)

    max = property(__get_max, __set_max)

    # ---------------------------------------------------------------------

    def __get_inc(self):

        if self.xfloat.xFloatHasInc():
            return self.xfloat.xFloatGetInc()
        else:
            return None

    inc = property(__get_inc)

    # ---------------------------------------------------------------------

    def __get_inc_mode(self):
        inc_mode = self.xfloat.xFloatGetIncMode()
        return _enums.IncMode(inc_mode)

    inc_mode = property(__get_inc_mode)

    # ---------------------------------------------------------------------

    def __get_representation(self):
        representation = self.xfloat.xFloatGetRepresentation()
        return _enums.Representation(representation)

    representation = property(__get_representation)

    # ---------------------------------------------------------------------

    def __get_unit(self):
        return self.xfloat.xFloatGetUnit()

    unit = property(__get_unit)

    # ---------------------------------------------------------------------

    def __get_display_notation(self):
        display_notation = self.xfloat.xFloatGetDisplayNotation()
        return _enums.DisplayNotation(display_notation)

    display_notation = property(__get_display_notation)

    # ---------------------------------------------------------------------

    def __get_display_precision(self):
        return self.xfloat.xFloatGetDisplayPrecision()

    display_precision = property(__get_display_precision)


class NodeBoolean(Node):

    def __repr__(self):
        base_node_info = __base_node__repr__(self)

        try:
            value = self.value
        except:
            value = 'N/A'

        return (
            f'{base_node_info}'
            f'\n\tvalue  =  {value}'
        )

    def __init__(self, hxnode):
        super().__init__(hxnode)
        self.xboolean = _xBoolean(hxnode)

    # TODO SFW-2179
    def __raise_type_error_if_not_expected_type(self, value, expected_type):
        if not isinstance(value, expected_type):
            raise TypeError(
                f'{expected_type.__name__} '
                f'expected instead of {type(value).__name__}')

    # ---------------------------------------------------------------------

    def __get_value(self):
        return self.xboolean.xBooleanGetValue()

    def __set_value(self, value):
        self.__raise_type_error_if_not_expected_type(value, bool)
        self.xboolean.xBooleanSetValue(value)

    value = property(__get_value, __set_value)


class NodeEnumeration(Node):

    def __repr__(self):

        base_node_info = __base_node__repr__(self)

        try:
            value = self.value
        except:
            value = 'N/A'
            enumentries = 'N/A'

        if value != 'N/A':
            try:
                enumentries = ''
                for enum in self.enumentry_names:
                    if enumentries == '':
                        enumentries = f'{enum}'
                    else:
                        enumentries = f'{enumentries}, {enum}'
                enumentries = f'[{enumentries}]'

            except:
                enumentries = 'N/A'

        return(
            f'{base_node_info}'
            f'\n\tvalue  =  {value}'
            f'\n\tenumentries  =  {enumentries}'
        )

    def __init__(self, hxnode):
        super().__init__(hxnode)
        self.xenumeration = _xEnumeration(hxnode)
        self.__entries_names = []
        self.__entries_nodes = {}

    # value ---------------------------------------------------------------

    def __get_value(self):
        return self.xenumeration.xEnumerationGetCurrentSymbolic()

    def __set_value_from_str(self, str_value):
        return self.xenumeration.xEnumerationSetBySymbolic(str_value)

    def __set_value(self, value):

        if not isinstance(value, str) and \
           not isinstance(value, NodeEnumentry) and \
           not isinstance(value, enum.Enum):
            raise TypeError(f'str, enumentry node, or enum member are '
                            f'expected instead of {type(value).__name__}.\n'
                            f'possible values are:\n'
                            f'\t{self.enumentry_names}')

        try:
            if isinstance(value, NodeEnumentry) or \
                    isinstance(value, enum.Enum):
                # naming it 'value' could be an issue in printing the
                # exception if the call throw
                value = value.name
            self.__set_value_from_str(value)

        except TypeError:
            # ArenaC will return invalid parameter (TypeError in
            # python). However, the invalid parameter here is for
            # invalid enum name

            raise ValueError(f'\n\'{value}\' is not a valid '
                             'enumentry (node\\name)\nenumentries '
                             'names for this node are:\n'
                             f'\t{self.enumentry_names}')

    value = property(__get_value, __set_value)

    # enumentry_names -----------------------------------------------------
    def __get_enumentry_names(self):

        num_of_entries = self.xenumeration.xEnumerationGetNumSymbbolics()
        entries_names = map(self.xenumeration.xEnumerationGetSymbolicByIndex,
                            range(num_of_entries))
        return list(entries_names)

    enumentry_names = property(__get_enumentry_names)

    # enumentry_nodes -----------------------------------------------------
    def __get_enumentry_nodes(self):
        entries_nodes = {}
        for enum_name in self.enumentry_names:
            hxentry_node = self.xenumeration.xEnumerationGetEntryByName(
                enum_name)
            enum_entry_node = NodeEnumentry(hxentry_node)
            entries_nodes[enum_name] = enum_entry_node
        return entries_nodes

    enumentry_nodes = property(__get_enumentry_nodes)


class NodeEnumentry(Node):
    # needs more design thoughts
    def __repr__(self):

        base_node_info = __base_node__repr__(self)

        try:
            is_self_clearing = self.is_self_clearing
        except:
            is_self_clearing = 'N/A'

        return(
            f'{base_node_info}'
            f'\n\tis_self_clearing  =  {is_self_clearing}'
        )

    def __init__(self, hxnode):
        super().__init__(hxnode)
        self.xenumentry = _xEnumentry(hxnode)

    # ---------------------------------------------------------------------
    # overrides the base calss , node , name property because enums needs
    # to return their sympolic name (which is human readable)
    def __get_name(self):
        return self.xenumentry.xEnumEntryGetSymbolic()

    name = property(__get_name)
    # ---------------------------------------------------------------------

    def __get_is_self_clearing(self):
        return self.xenumentry.xEnumEntryIsSelfClearing()

    is_self_clearing = property(__get_is_self_clearing)

# TODO SFW-2116


class NodeCategory(Node):
    def __repr__(self):
        base_node_info = __base_node__repr__(self)

        try:
            number_of_features = len(self.features)
        except:
            number_of_features = 'N/A'

        return (
            f'{base_node_info}'
            f'\n\tnumber of features  =  {number_of_features}'
        )

    def __init__(self, hxnode):
        super().__init__(hxnode)
        self.xcategory = _xCategory(hxnode)

    def __get_features(self):
        features_nodes = {}
        num_of_features = self.xcategory.xCategoryGetNumFeatures()
        for index_of_feature in range(num_of_features):
            hxfeature_node = self.xcategory.xCategoryGetFeature(
                index_of_feature)
            feature_node_base = Node(hxfeature_node)
            feature_node = _node_helpers.cast_from_general_node_to_specific_node_type(
                feature_node_base)
            features_nodes[feature_node.name] = feature_node

        return features_nodes

    features = property(__get_features)


# TODO SFW-2185
# TODO SFW-2117
class NodeRegister(Node):

    def __repr__(self):
        base_node_info = __base_node__repr__(self)
        return f'{base_node_info}'

    def __init__(self, hxnode):
        super().__init__(hxnode)
        self.xregister = _xRegister(hxnode)

    def get(self, register_length):
        if not isinstance(register_length, int):
            raise TypeError(f'int expected instead of '
                            f'{type(register_length).__name__}')

        return self.xregister.xRegisterGet(register_length)

    def set(self, hsrc_register, src_register_length: int):
        if not isinstance(src_register_length, int):
            raise TypeError(f'int expected instead of '
                            f'{type(src_register_length).__name__}')
        self.xregister.xRegisterSet(hsrc_register, src_register_length)

# TODO SFW-2118


class NodeCommand(Node):

    def __repr__(self):
        base_node_info = __base_node__repr__(self)
        return f'{base_node_info}'

    def __init__(self, hxnode):
        super().__init__(hxnode)
        self.xcommand = _xCommand(hxnode)

    def execute(self):
        '''Excutes the command node
        '''
        return self.xcommand.xCommandExecute()

    def __get_is_done(self):
        return self.xcommand.xCommandIsDone()

    is_done = property(__get_is_done)
