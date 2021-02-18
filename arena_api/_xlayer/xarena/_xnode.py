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

from ctypes import POINTER, byref, create_string_buffer

from arena_api._xlayer.xarena.arenac import harenac
from arena_api._xlayer.xarena.arenac_defaults import (
    XARENA_STR_BUFFER_SIZE_DEFAULT,
    XARENA_STR_BUFFER_SIZE_1000,
    XARENA_STR_BUFFER_SIZE_MAX)
from arena_api._xlayer.xarena.arenac_types import (ac_access_mode,
                                                   ac_caching_mode,
                                                   ac_display_notation,
                                                   ac_inc_mode,
                                                   ac_interface_type,
                                                   ac_namespace,
                                                   ac_representation,
                                                   ac_visibility, acNode,
                                                   bool8_t, char_ptr, double,
                                                   int64_t, size_t, uint8_t)


class _xNode():
    def __init__(self, hxnode):
        # TODO SFW-2546
        if not hxnode:
            raise TypeError('Node handle is None')
        self.hxnode = acNode(hxnode)

    # Gets General --------------------------------------------------------

    def xNodeGetAccessMode(self):
        access_mode = ac_access_mode(0)
        # AC_ERROR acNodeGetAccessMode(
        #   acNode hNode,
        #   AC_ACCESS_MODE* pAccessMode)
        harenac.acNodeGetAccessMode(
            self.hxnode,
            byref(access_mode))

        return access_mode.value

    def xNodeGetCachingMode(self):

        caching_mode = ac_caching_mode(0)
        # AC_ERROR acNodeGetCachingMode(
        #   acNode hNode,
        #   AC_CACHING_MODE* pCachingMode)
        harenac.acNodeGetCachingMode(
            self.hxnode,
            byref(caching_mode))

        return caching_mode.value

    def xNodeGetAlias(self):

        alias_node = acNode(None)
        # AC_ERROR acNodeGetAlias(
        #   acNode hNode,
        #   acNode* phAliasNode)
        harenac.acNodeGetAlias(
            self.hxnode,
            byref(alias_node))

        return alias_node.value

    def xNodeGetCastAlias(self):

        alias_node = acNode(None)
        # AC_ERROR acNodeGetCastAlias(
        #   acNode hNode,
        #   acNode* phAliasNode)
        harenac.acNodeGetCastAlias(
            self.hxnode,
            byref(alias_node))

        return alias_node.value

    def xNodeGetDescription(self):

        description_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_1000)
        description_len = size_t(XARENA_STR_BUFFER_SIZE_1000)
        # AC_ERROR acNodeGetDescription(
        #   acNode hNode,
        #   char* pDescriptionBuf,
        #   size_t* pBufLen)
        harenac.acNodeGetDescription(
            self.hxnode,
            description_p,
            byref(description_len))

        return description_p.value.decode()

    def xNodeGetDeviceName(self):

        device_name_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_DEFAULT)
        device_name_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acNodeGetDeviceName(
        #   acNode hNode,
        #   char* pDeviceNameBuf,
        #   size_t* pBufLen)
        harenac.acNodeGetDeviceName(
            self.hxnode,
            device_name_p,
            byref(device_name_len))

        return device_name_p.value.decode()

    def xNodeGetDisplayName(self):

        display_name_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_DEFAULT)
        display_name_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acNodeGetDisplayName(
        #   acNode hNode,
        #   char* pDisplayNameBuf,
        #   size_t* pBufLen)
        harenac.acNodeGetDisplayName(
            self.hxnode,
            display_name_p,
            byref(display_name_len))

        return display_name_p.value.decode()

    def xNodeGetDocuURL(self):

        doc_url_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_1000)
        doc_url_len = size_t(XARENA_STR_BUFFER_SIZE_1000)
        # AC_ERROR acNodeGetDocuURL(
        #   acNode hNode,
        #   char* pDocuURLBuf,
        #   size_t* pBufLen)
        harenac.acNodeGetDocuURL(
            self.hxnode,
            doc_url_p,
            byref(doc_url_len))

        return doc_url_p.value.decode()

    def xNodeGetEventID(self):

        event_id_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_DEFAULT)
        event_id_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acNodeGetEventID(
        #   acNode hNode,
        #   char* pEventIDBuf,
        #   size_t* pBufLen)
        harenac.acNodeGetEventID(
            self.hxnode,
            event_id_p,
            byref(event_id_len))

        return event_id_p.value.decode()

    def xNodeGetName(self):

        name_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_DEFAULT)
        name_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acNodeGetName(
        #   acNode hNode,
        #   char* pNameBuf,
        #   size_t* pBufLen)
        harenac.acNodeGetName(
            self.hxnode,
            name_p,
            byref(name_len))

        return name_p.value.decode()

    def xNodeGetFullyQualifiedName(self):

        qualified_name_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_DEFAULT)
        qualified_name_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acNodeGetFullyQualifiedName(
        #   acNode hNode,
        #   char* pNameBuf,
        #   size_t* pBufLen)
        harenac.acNodeGetFullyQualifiedName(
            self.hxnode,
            qualified_name_p,
            byref(qualified_name_len))

        return qualified_name_p.value.decode()

    def xNodeGetNamespace(self):

        namespace = ac_namespace(0)
        # AC_ERROR acNodeGetNamespace(
        #   acNode hNode,
        #   AC_NAMESPACE* pNameSpace)
        harenac.acNodeGetNamespace(
            self.hxnode,
            byref(namespace))

        return namespace.value

    def xNodeGetPollingTime(self):

        polling_time = int64_t(0)
        # AC_ERROR acNodeGetPollingTime(
        #   acNode hNode,
        #   int64_t* pPollingTime)
        harenac.acNodeGetPollingTime(
            self.hxnode,
            byref(polling_time))

        return polling_time.value

    def xNodeGetPrincipalInterfaceType(self):

        interface_type = ac_interface_type(0)
        # AC_ERROR acNodeGetPrincipalInterfaceType(
        #   acNode hNode,
        #   AC_INTERFACE_TYPE* pInterfaceType)
        harenac.acNodeGetPrincipalInterfaceType(
            self.hxnode,
            byref(interface_type))

        return interface_type.value

    def xNodeGetToolTip(self):

        tooltip_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_1000)
        tooltip_len = size_t(XARENA_STR_BUFFER_SIZE_1000)
        # AC_ERROR acNodeGetToolTip(
        #   acNode hNode,
        #   char* pToolTipBuf,
        #   size_t* pBufLen)
        harenac.acNodeGetToolTip(
            self.hxnode,
            tooltip_p,
            byref(tooltip_len))

        return tooltip_p.value.decode()

    def xNodeGetVisibility(self):

        visibility = ac_visibility(0)
        # AC_ERROR acNodeGetVisibility(
        #   acNode hNode,
        #   AC_VISIBILITY* pVisibility)
        harenac.acNodeGetVisibility(
            self.hxnode,
            byref(visibility))

        return visibility.value

    # Children ------------------------------------------------------------

    def xNodeGetNumChildren(self):

        num_children = size_t(0)
        # AC_ERROR acNodeGetNumChildren(
        #   acNode hNode,
        #   size_t* pNumChildren)
        harenac.acNodeGetNumChildren(
            self.hxnode,
            byref(num_children))

        return num_children.value

    def xNodeGetChild(self, index):

        child_node = acNode(None)
        index = size_t(index)
        # AC_ERROR acNodeGetChild(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phChildNode)
        harenac.acNodeGetChild(
            self.hxnode,
            index,
            byref(child_node))

        return child_node.value

    def xNodeGetChildAndAccessMode(self, index):

        child_node = acNode(None)
        index = size_t(index)
        access_mode = ac_access_mode(0)
        # AC_ERROR acNodeGetChildAndAccessMode(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phChildNode,
        #   AC_ACCESS_MODE* pAccessMode)
        harenac.acNodeGetChildAndAccessMode(
            self.hxnode,
            index,
            byref(child_node),
            byref(access_mode))

        return child_node.value, access_mode.value

    # Parents -------------------------------------------------------------

    def xNodeGetNumParents(self):

        num_parents = size_t(0)
        # AC_ERROR acNodeGetNumParents(
        #   acNode hNode,
        #   size_t* pNumParents)
        harenac.acNodeGetNumParents(
            self.hxnode,
            byref(num_parents))

        return num_parents.value

    def xNodeGetParent(self, index):

        index = size_t(index)
        parent_node = acNode(None)
        # AC_ERROR acNodeGetParent(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phParentNode)
        harenac.acNodeGetParent(
            self.hxnode,
            index,
            byref(parent_node))

        return parent_node.value

    def xNodeGetParentAndAccessMode(self, index):

        index = size_t(index)
        parent_node = acNode(None)
        access_mode = ac_access_mode(0)
        # AC_ERROR acNodeGetParentAndAccessMode(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phParentNode,
        #   AC_ACCESS_MODE* pAccessMode)
        harenac.acNodeGetParentAndAccessMode(
            self.hxnode,
            index,
            byref(parent_node),
            byref(access_mode))

        return parent_node.value, access_mode.value

    # Property ------------------------------------------------------------

    def xNodeGetNumPropertyNames(self):

        num_property_names = size_t(0)
        # AC_ERROR acNodeGetNumPropertyNames(
        #   acNode hNode,
        #   size_t* pNumPropertyNames)
        harenac.acNodeGetNumPropertyNames(
            self.hxnode,
            byref(num_property_names))

        return num_property_names.value

    def xNodeGetPropertyName(self, index):

        property_name_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_1000)
        property_name_len = size_t(XARENA_STR_BUFFER_SIZE_1000)
        # AC_ERROR acNodeGetPropertyName(
        #   acNode hNode,
        #   size_t index,
        #   char* pPropertyNameBuf,
        #   size_t* pBufLen)
        harenac.acNodeGetPropertyName(
            self.hxnode,
            index,
            property_name_p,
            byref(property_name_len))

        return property_name_p.value.decode()

    def xNodeGetProperty(self, property_name, str_buffer_size=None):

        # check if it came from a recusive call ti increase the buffer size
        if str_buffer_size:
            if str_buffer_size > XARENA_STR_BUFFER_SIZE_MAX:
                # stopping case for the recursion
                raise BufferError(
                    'internal : recurive call maxed the buffer size')
            XARENA_STR_BUFFER_SIZE = str_buffer_size
        else:
            XARENA_STR_BUFFER_SIZE = XARENA_STR_BUFFER_SIZE_1000

        property_name_p = char_ptr(property_name.encode())
        property_value_p = create_string_buffer(
            XARENA_STR_BUFFER_SIZE)
        property_value_len = size_t(XARENA_STR_BUFFER_SIZE)
        property_attribute_p = create_string_buffer(
            XARENA_STR_BUFFER_SIZE)
        property_attribute_len = size_t(XARENA_STR_BUFFER_SIZE)
        # AC_ERROR acNodeGetProperty(
        #   acNode hNode,
        #   const char* pPropertyName,
        #   char* pPropertyValueBuf,
        #   size_t* pPropertyValueBufLen,
        #   char* pPropertyAttributeBuf,
        #   size_t* pPropertyAttributeBufLen)
        try:
            harenac.acNodeGetProperty(
                self.hxnode,
                property_name_p,
                property_value_p,
                byref(property_value_len),
                property_attribute_p,
                byref(property_attribute_len))
            return property_value_p.value.decode(), property_attribute_p.value.decode()

        except:
            # call again with longer buffer
            return self.xNodeGetProperty(property_name,
                                         str_buffer_size=XARENA_STR_BUFFER_SIZE * 3)

    # impose --------------------------------------------------------------

    def xNodeImposeVisibility(self, visibility):

        visibility = ac_visibility(visibility)
        # AC_ERROR acNodeImposeVisibility(
        #   acNode hNode,
        #   AC_VISIBILITY imposedVisibility)
        harenac.acNodeImposeVisibility(
            self.hxnode,
            visibility)

    def xNodeImposeAccessMode(self, access_mode):

        access_mode = ac_access_mode(access_mode)
        # AC_ERROR acNodeImposeAccessMode(
        #   acNode hNode,
        #   AC_ACCESS_MODE imposedAccessMode)
        harenac.acNodeImposeAccessMode(
            self.hxnode,
            access_mode)

    # is ? ----------------------------------------------------------------

    def xNodeIsCachable(self):

        is_cachable = bool8_t(False)
        # AC_ERROR acNodeIsCachable(
        #   acNode hNode,
        #   bool8_t* pIsCachable)
        harenac.acNodeIsCachable(
            self.hxnode,
            byref(is_cachable))

        return is_cachable.value

    def xNodeIsDeprecated(self):

        is_deprecated = bool8_t(False)
        # AC_ERROR acNodeIsDeprecated(
        #   acNode hNode,
        #   bool8_t* pIsDeprecated)
        harenac.acNodeIsDeprecated(
            self.hxnode,
            byref(is_deprecated))

        return is_deprecated.value

    def xNodeIsFeature(self):

        is_feature = bool8_t(False)
        # AC_ERROR acNodeIsFeature(
        #   acNode hNode,
        #   bool8_t* pIsFeature)

        harenac.acNodeIsFeature(
            self.hxnode,
            byref(is_feature))

        return is_feature.value

    # Other ---------------------------------------------------------------

    def xNodeInvalidateNode(self):

        # AC_ERROR acNodeInvalidateNode(
        #   acNode hNode)
        harenac.acNodeInvalidateNode(
            self.hxnode)


class _xSelector():

    def __init__(self, hxnode):
        # TODO SFW-2546
        if not hxnode:
            raise TypeError('Node handle is None')
        self.hxnode = acNode(hxnode)

    # Selecting -----------------------------------------------------------

    def xSelectorIsSelector(self):

        is_selector = bool8_t(False)
        # AC_ERROR acSelectorIsSelector(
        #   acNode hNode,
        #   bool8_t* pIsSelector)
        harenac.acSelectorIsSelector(
            self.hxnode,
            byref(is_selector))

        return is_selector.value

    def xSelectorGetNumSelectingFeatures(self):

        num_selecting_features = size_t(0)
        # AC_ERROR acSelectorGetNumSelectingFeatures(s
        #   acNode hNode,
        #   size_t* pNumSelectingFeatures)
        harenac.acSelectorGetNumSelectingFeatures(
            self.hxnode,
            byref(num_selecting_features))

        return num_selecting_features.value

    def xSelectorGetSelectingFeature(self, index):

        index = size_t(index)
        selecting_feature_node = acNode(None)
        # AC_ERROR acSelectorGetSelectingFeature(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phSelectingFeatureNode)
        harenac.acSelectorGetSelectingFeature(
            self.hxnode,
            index,
            byref(selecting_feature_node))

        return selecting_feature_node.value

    def xSelectorGetSelectingFeatureAndAccessMode(self, index):

        index = size_t(index)
        selecting_feature_node = acNode(None)
        access_mode = ac_access_mode(0)
        # AC_ERROR acSelectorGetSelectingFeatureAndAccessMode(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phSelectingFeatureNode,
        #   AC_ACCESS_MODE* pAccessMode)
        harenac.acSelectorGetSelectingFeatureAndAccessMode(
            self.hxnode,
            index,
            byref(selecting_feature_node),
            byref(access_mode))

        return selecting_feature_node.value, access_mode.value

    # Selected ------------------------------------------------------------

    def xSelectorGetNumSelectedFeatures(self):

        num_selected_features = size_t(0)
        # AC_ERROR acSelectorGetNumSelectedFeatures(
        #   acNode hNode,
        #   size_t* pNumSelectedFeatures)
        harenac.acSelectorGetNumSelectedFeatures(
            self.hxnode,
            byref(num_selected_features))

        return num_selected_features.value

    def xSelectorGetSelectedFeature(self, index):

        index = size_t(index)
        selected_feature_node = acNode(None)
        # AC_ERROR acSelectorGetSelectedFeature(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phSelectedFeatureNode)
        harenac.acSelectorGetSelectedFeature(
            self.hxnode,
            index,
            byref(selected_feature_node))

        return selected_feature_node.value

    def xSelectorGetSelectedFeatureAndAccessMode(self, index):

        index = size_t(index)
        selected_feature_node = acNode(None)
        access_mode = ac_access_mode(0)
        # AC_ERROR acSelectorGetSelectedFeatureAndAccessMode(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phSelectedFeatureNode,
        #   AC_ACCESS_MODE* pAccessMode)
        harenac.acSelectorGetSelectedFeatureAndAccessMode(
            self.hxnode,
            index,
            byref(selected_feature_node),
            byref(access_mode))

        return selected_feature_node.value, access_mode.value


class _xString():

    def __init__(self, hxnode):
        # TODO SFW-2546
        if not hxnode:
            raise TypeError('Node handle is None')
        self.hxnode = acNode(hxnode)

    def xStringSetValue(self, value):

        value_p = create_string_buffer(value.encode())
        # AC_ERROR acStringSetValue(
        #   acNode hNode,
        #   char* pValue)
        harenac.acStringSetValue(
            self.hxnode,
            value_p)

    def xStringGetValue(self):

        value_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_DEFAULT)
        value_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acStringGetValue(
        #   acNode hNode,
        #   char* pValue,
        #   size_t* pBufLen)
        harenac.acStringGetValue(
            self.hxnode,
            value_p,
            byref(value_len))

        return value_p.value.decode()

    def xStringGetMaxLength(self):

        length = int64_t(0)
        # AC_ERROR acStringGetMaxLength(
        #   acNode hNode,
        #   int64_t* pMaxLength)
        harenac.acStringGetMaxLength(
            self.hxnode,
            byref(length))

        return length.value


class _xInteger():

    def __init__(self, hxnode):
        # TODO SFW-2546
        if not hxnode:
            raise TypeError('Node handle is None')
        self.hxnode = acNode(hxnode)

    # Get -----------------------------------------------------------------

    def xIntegerGetValue(self):

        value = int64_t(0)
        # AC_ERROR acIntegerGetValue(
        #   acNode hNode,
        #   int64_t* pValue)
        harenac.acIntegerGetValue(
            self.hxnode,
            byref(value))

        return value.value

    def xIntegerGetMin(self):

        min_value = int64_t(0)
        # AC_ERROR acIntegerGetMin(
        #   acNode hNode,
        #   int64_t* pMinimum)
        harenac.acIntegerGetMin(
            self.hxnode,
            byref(min_value))

        return min_value.value

    def xIntegerGetMax(self):

        max_value = int64_t(0)
        # AC_ERROR acIntegerGetMax(
        #   acNode hNode,
        #   int64_t* pMaximum)
        harenac.acIntegerGetMax(
            self.hxnode,
            byref(max_value))

        return max_value.value

    def xIntegerGetInc(self):

        increment = int64_t(0)
        # AC_ERROR acIntegerGetInc(
        #   acNode hNode,
        #   int64_t* pIncrement)
        harenac.acIntegerGetInc(
            self.hxnode,
            byref(increment))

        return increment.value

    def xIntegerGetIncMode(self):

        increment_mode = ac_inc_mode(0)
        # AC_ERROR acIntegerGetIncMode(
        #   acNode hNode,
        #   AC_INC_MODE* pIncrementMode)
        harenac.acIntegerGetIncMode(
            self.hxnode,
            byref(increment_mode))

        return increment_mode.value

    def xIntegerGetRepresentation(self):

        representation = ac_representation(0)
        # AC_ERROR acIntegerGetRepresentation(
        #   acNode hNode,
        #   AC_REPRESENTATION* pRepresentation)
        harenac.acIntegerGetRepresentation(
            self.hxnode,
            byref(representation))

        return representation.value

    def xIntegerGetUnit(self):

        unit_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_DEFAULT)
        unit_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acIntegerGetUnit(
        #   acNode hNode,
        #   char* pUnitBuf,
        #   size_t* pBufLen)
        harenac.acIntegerGetUnit(
            self.hxnode,
            unit_p,
            byref(unit_len))

        return unit_p.value.decode()

    # Impose --------------------------------------------------------------

    def xIntegerSetValue(self, value):

        value = int64_t(value)
        # AC_ERROR acIntegerSetValue(
        #   acNode hNode,
        #   int64_t value)
        harenac.acIntegerSetValue(
            self.hxnode,
            value)

    def xIntegerImposeMin(self, min_value):

        min_value = int64_t(min_value)
        # AC_ERROR acIntegerImposeMin(
        #   acNode hNode,
        #   int64_t imposedMinimum)
        harenac.acIntegerImposeMin(
            self.hxnode,
            min_value)

    def xIntegerImposeMax(self, max_value):

        max_value = int64_t(max_value)
        # AC_ERROR acIntegerImposeMax(
        #   acNode hNode,
        #   int64_t imposedMaximum)
        harenac.acIntegerImposeMax(
            self.hxnode,
            max_value)


class _xFloat():

    def __init__(self, hxnode):
        # TODO SFW-2546
        if not hxnode:
            raise TypeError('Node handle is None')
        self.hxnode = acNode(hxnode)

    # Get -----------------------------------------------------------------

    def xFloatGetValue(self):

        value = double(0)
        # AC_ERROR acFloatGetValue(
        #   acNode hNode,
        #   double* pValue)
        harenac.acFloatGetValue(
            self.hxnode,
            byref(value))

        return value.value

    def xFloatGetMin(self):

        min_value = double(0)
        # AC_ERROR acFloatGetMin(
        #   acNode hNode,
        #   double* pMinimum)
        harenac.acFloatGetMin(
            self.hxnode,
            byref(min_value))

        return min_value.value

    def xFloatGetMax(self):

        max_value = double(0)
        # AC_ERROR acFloatGetMax(
        #   acNode hNode,
        #   double* pMaximum)
        harenac.acFloatGetMax(
            self.hxnode,
            byref(max_value))

        return max_value.value

    def xFloatHasInc(self):

        has_inc = bool8_t(False)
        # AC_ERROR acFloatHasInc(
        #   acNode hNode,
        #   bool8_t* pHasInc)
        harenac.acFloatHasInc(
            self.hxnode,
            byref(has_inc))

        return has_inc.value

    def xFloatGetInc(self):

        increment = double(0)
        # AC_ERROR acFloatGetInc(
        #   acNode hNode,
        #   double* pIncrement)
        harenac.acFloatGetInc(
            self.hxnode,
            byref(increment))

        return increment.value

    def xFloatGetIncMode(self):

        inc_mode = ac_inc_mode(0)
        # AC_ERROR acFloatGetIncMode(
        #   acNode hNode,
        #   AC_INC_MODE* pIncMode)
        harenac.acFloatGetIncMode(
            self.hxnode,
            byref(inc_mode))

        return inc_mode.value

    def xFloatGetRepresentation(self):

        representation = ac_representation(0)
        # AC_ERROR acFloatGetRepresentation(
        #   acNode hNode,
        #   AC_REPRESENTATION* pRepresentation)
        harenac.acFloatGetRepresentation(
            self.hxnode,
            byref(representation))

        return representation.value

    def xFloatGetUnit(self):

        unit_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_DEFAULT)
        unit_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)

        # AC_ERROR acFloatGetUnit(
        #   acNode hNode,
        #   char* pUnitBuf,
        #   size_t* pBufLen)
        harenac.acFloatGetUnit(
            self.hxnode,
            unit_p,
            byref(unit_len))

        return unit_p.value.decode()

    def xFloatGetDisplayNotation(self):

        display_notation = ac_display_notation(0)
        # AC_ERROR acFloatGetDisplayNotation(
        #   acNode hNode,
        #   AC_DISPLAY_NOTATION* pDisplayNotation)
        harenac.acFloatGetDisplayNotation(
            self.hxnode,
            byref(display_notation))

        return display_notation.value

    def xFloatGetDisplayPrecision(self):

        display_precision = int64_t(0)
        # AC_ERROR acFloatGetDisplayPrecision(
        #   acNode hNode,
        #   int64_t* pDisplayPrecision)
        harenac.acFloatGetDisplayPrecision(
            self.hxnode,
            byref(display_precision))

        return display_precision.value

    # Impose --------------------------------------------------------------

    def xFloatSetValue(self, value):

        value = double(value)
        # AC_ERROR acFloatSetValue(
        #   acNode hNode,
        #   double value)
        harenac.acFloatSetValue(
            self.hxnode,
            value)

    def xFloatImposeMin(self, min_value):

        min_value = double(min_value)
        # AC_ERROR acFloatImposeMin(
        #   acNode hNode,
        #   double imposedMinimum)
        harenac.acFloatImposeMin(
            self.hxnode,
            min_value)

    def xFloatImposeMax(self, max_value):

        max_value = double(max_value)
        # AC_ERROR acFloatImposeMax(
        #   acNode hNode,
        #   double imposedMaximum)
        harenac.acFloatImposeMax(
            self.hxnode,
            max_value)


class _xBoolean():

    def __init__(self, hxnode):
        # TODO SFW-2546
        if not hxnode:
            raise TypeError('Node handle is None')
        self.hxnode = acNode(hxnode)

    def xBooleanGetValue(self):

        value = bool8_t(False)
        # AC_ERROR acBooleanGetValue(
        #   acNode hNode,
        #   bool8_t* pValue)
        harenac.acBooleanGetValue(
            self.hxnode,
            byref(value))

        return value.value

    def xBooleanSetValue(self, value):

        value = bool8_t(value)
        # AC_ERROR acBooleanSetValue(
        #   acNode hNode,
        #   bool8_t value)
        harenac.acBooleanSetValue(
            self.hxnode,
            value)


class _xEnumeration():

    def __init__(self, hxnode):
        # TODO SFW-2546
        if not hxnode:
            raise TypeError('Node handle is None')
        self.hxnode = acNode(hxnode)

    # Gets ----------------------------------------------------------------

    def xEnumerationGetNumEntries(self):

        num_entries = size_t(0)
        # AC_ERROR acEnumerationGetNumEntries(
        #   acNode hNode,
        #   size_t* pNumEntries)
        harenac.acEnumerationGetNumEntries(
            self.hxnode,
            byref(num_entries))

        return num_entries.value

    def xEnumerationGetEntryByIndex(self, index):

        index = size_t(index)
        entry_node = acNode(None)
        # AC_ERROR acEnumerationGetEntryByIndex(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phEntryNode)
        harenac.acEnumerationGetEntryByIndex(
            self.hxnode,
            index,
            byref(entry_node))

        return entry_node.value

    def xEnumerationGetEntryByName(self, name):

        name_p = create_string_buffer(name.encode())
        entry_node = acNode(None)
        # AC_ERROR acEnumerationGetEntryByName(
        #   acNode hNode,
        #   const char* pEntryName,
        #   acNode* phEntryNode)
        harenac.acEnumerationGetEntryByName(
            self.hxnode,
            name_p,
            byref(entry_node))

        return entry_node.value

    def xEnumerationGetEntryAndAccessModeByIndex(self, index):

        index = size_t(index)
        entry_node = acNode(None)
        access_mode = ac_access_mode(0)
        # AC_ERROR acEnumerationGetEntryAndAccessModeByIndex(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phEntryNode,
        #   AC_ACCESS_MODE* pAccessMode)
        harenac.acEnumerationGetEntryAndAccessModeByIndex(
            self.hxnode,
            index,
            byref(entry_node),
            byref(access_mode))

        return entry_node.value, access_mode.value

    def xEnumerationGetEntryAndAccessModeByName(self, name):

        name_p = create_string_buffer(name.encode())
        entry_node = acNode(None)
        access_mode = ac_access_mode(0)
        # AC_ERROR acEnumerationGetEntryAndAccessModeByName(
        #   acNode hNode,
        #   char* pEntryName,
        #   acNode* phEntryNode,
        #   AC_ACCESS_MODE* pAccessMode)
        harenac.acEnumerationGetEntryAndAccessModeByName(
            self.hxnode,
            name_p,
            byref(entry_node),
            byref(access_mode))

        return entry_node.value, access_mode.value

    def xEnumerationGetNumSymbbolics(self):

        num_symbolics = size_t(0)
        # AC_ERROR acEnumerationGetNumEntries(
        #   acNode hNode,
        #   size_t* pNumEntries)
        harenac.acEnumerationGetNumSymbolics(
            self.hxnode,
            byref(num_symbolics))

        return num_symbolics.value

    def xEnumerationGetSymbolicByIndex(self, index):

        index = size_t(index)
        symbolic_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_DEFAULT)
        symbolic_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)

        # AC_ERROR acEnumerationGetSymbolicByIndex(
        #   acNode hNode,
        #   size_t index,
        #   char* pSymbolicBuf,
        #   size_t* pBufLen)
        harenac.acEnumerationGetSymbolicByIndex(
            self.hxnode,
            index,
            symbolic_p,
            byref(symbolic_len))

        return symbolic_p.value.decode()

    def xEnumerationGetCurrentEntry(self):

        current_entry_node = acNode(None)
        # AC_ERROR acEnumerationGetCurrentEntry(
        #   acNode hNode,
        #   acNode* phEntryNode)
        harenac.acEnumerationGetCurrentEntry(
            self.hxnode,
            byref(current_entry_node))

        return current_entry_node.value

    def xEnumerationGetCurrentEntryAndAccessMode(self):

        current_entry_node = acNode(None)
        access_mode = ac_access_mode(0)
        # AC_ERROR acEnumerationGetCurrentEntryAndAccessMode(
        #   acNode hNode,
        #   acNode* phEntryNode,
        #   AC_ACCESS_MODE* pAccessMode)
        harenac.acEnumerationGetCurrentEntryAndAccessMode(
            self.hxnode,
            byref(current_entry_node),
            byref(access_mode))

        return current_entry_node.value, access_mode.value

    def xEnumerationGetCurrentSymbolic(self):

        symbolic_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_DEFAULT)
        symbolic_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acEnumerationGetCurrentSymbolic(
        #   acNode hNode,
        #   char* pSymbolicBuf,
        #   size_t* pBufLen)
        harenac.acEnumerationGetCurrentSymbolic(
            self.hxnode,
            symbolic_p,
            byref(symbolic_len))

        return symbolic_p.value.decode()

    # Sets ----------------------------------------------------------------

    def xEnumerationSetByIntValue(self, value):

        value = int64_t(value)
        # AC_ERROR acEnumerationSetByIntValue(
        #   acNode hNode,
        #   int64_t value)
        harenac.acEnumerationSetByIntValue(
            self.hxnode,
            value)

    def xEnumerationSetBySymbolic(self, value):

        value_str_p = create_string_buffer(value.encode())
        # AC_ERROR acEnumerationSetBySymbolic(
        #   acNode hNode,
        #   const char* pSymbolic)
        harenac.acEnumerationSetBySymbolic(
            self.hxnode,
            value_str_p)


class _xEnumentry():

    def __init__(self, hxnode):
        # TODO SFW-2546
        if not hxnode:
            # shouldi check the type here ?
            raise TypeError('Node handle is None')
        self.hxnode = acNode(hxnode)

    # Gets ----------------------------------------------------------------

    def xEnumEntryGetIntValue(self):

        int_value = int64_t(0)
        # AC_ERROR acEnumEntryGetIntValue(
        #   acNode hNode,
        #   int64_t* pValue)
        harenac.acEnumEntryGetIntValue(
            self.hxnode,
            byref(int_value))

        return int_value.value

    def xEnumEntryGetNumericValue(self):

        double_value = double(0)
        # AC_ERROR acEnumEntryGetNumericValue(
        #   acNode hNode,
        #   double* pValue)
        harenac.acEnumEntryGetNumericValue(
            self.hxnode,
            byref(double_value))

        return double_value.value

    def xEnumEntryGetSymbolic(self):

        symbolic_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_DEFAULT)
        symbolic_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acEnumEntryGetSymbolic(
        #   acNode hNode,
        #   char* pSymbolicBuf,
        #   size_t* pBufLen)
        harenac.acEnumEntryGetSymbolic(
            self.hxnode,
            symbolic_p,
            byref(symbolic_len))

        return symbolic_p.value.decode()

    # Checks --------------------------------------------------------------

    def xEnumEntryIsSelfClearing(self):

        is_selfclearing = bool8_t(False)
        # AC_ERROR acEnumEntryIsSelfClearing(
        #   acNode hNode,
        #   bool8_t* pIsSelfClearing)
        harenac.acEnumEntryIsSelfClearing(
            self.hxnode,
            byref(is_selfclearing))

        return is_selfclearing.value


class _xCategory():

    def __init__(self, hxnode):
        # TODO SFW-2546
        if not hxnode:
            raise TypeError('Node handle is None')
        self.hxnode = acNode(hxnode)

    def xCategoryGetNumFeatures(self):

        num_features = size_t(0)
        # AC_ERROR acCategoryGetNumFeatures(
        #   acNode hNode,
        #   size_t* pNumFeatures)
        harenac.acCategoryGetNumFeatures(
            self.hxnode,
            byref(num_features))

        return num_features.value

    def xCategoryGetFeature(self, index):

        index = size_t(index)
        feature_node = acNode(None)
        # AC_ERROR acCategoryGetFeature(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phFeatureNode)
        harenac.acCategoryGetFeature(
            self.hxnode,
            index,
            byref(feature_node))

        return feature_node.value

    def xCategoryGetFeatureAndAccessMode(self, index):

        index = size_t(index)
        feature_node = acNode(None)
        access_mode = ac_access_mode(0)
        # AC_ERROR acCategoryGetFeatureAndAccessMode(
        #   acNode hNode,
        #   size_t index,
        #   acNode* phFeatureNode,
        #   AC_ACCESS_MODE* pAccessMode)
        harenac.acCategoryGetFeatureAndAccessMode(
            self.hxnode,
            index,
            byref(feature_node),
            byref(access_mode))

        return feature_node.value, access_mode.value


class _xRegister():

    def __init__(self, hxnode):
        # TODO SFW-2546
        if not hxnode:
            raise TypeError('Node handle is None')
        self.hxnode = acNode(hxnode)

    def xRegisterSet(self, hregister, register_len):

        buffer_p = uint8_t(hregister)
        # AC_ERROR acRegisterSet(
        #   acNode hNode,
        #   const uint8_t* pBuf,
        #   int64_t bufLen)
        harenac.acRegisterSet(
            self.hxnode,
            byref(buffer_p),
            register_len)

    def xRegisterGet(self, register_len):

        buffer_p = uint8_t(0)
        buffer_len = int64_t(register_len)
        # AC_ERROR acRegisterGet(
        #   acNode hNode,
        #   uint8_t* pBuf,
        #   int64_t bufLen)
        harenac.acRegisterGet(
            self.hxnode,
            byref(buffer_p),
            buffer_len)

        return buffer_p.value


class _xCommand():

    def __init__(self, hxnode):
        # TODO SFW-2546
        if not hxnode:
            raise TypeError('Node handle is None')
        self.hxnode = acNode(hxnode)

    def xCommandExecute(self):

        # AC_ERROR acCommandExecute(
        #   acNode hNode)
        harenac.acCommandExecute(
            self.hxnode)

    def xCommandIsDone(self):

        is_done = bool8_t(False)
        # AC_ERROR acCommandIsDone(
        #   acNode hNode,
        #   bool8_t* pIsDone)
        harenac.acCommandIsDone(
            self.hxnode,
            byref(is_done))

        return is_done.value


class _xValue():

    def __init__(self, hxnode):
        # TODO SFW-2546
        if not hxnode:
            raise TypeError('Node handle is None')
        self.hxnode = acNode(hxnode)

    def xValueToString(self):

        value_str_p = create_string_buffer(XARENA_STR_BUFFER_SIZE_DEFAULT)
        value_str_len = size_t(XARENA_STR_BUFFER_SIZE_DEFAULT)
        # AC_ERROR acValueToString(
        #   acNode hNode,
        #   char* pValueBuf,
        #   size_t* pBufLen)
        harenac.acValueToString(
            self.hxnode,
            value_str_p,
            byref(value_str_len))

        return value_str_p.value.decode()

    def xValueFromString(self, value):

        value_str_p = char_ptr(value.encode())
        # AC_ERROR acValueFromString(
        #   acNode hNode,
        #   char* pValue)
        harenac.acValueFromString(
            self.hxnode,
            value_str_p)

    def xValueIsValueCacheValid(self):

        is_valid = bool8_t(False)
        # AC_ERROR acValueIsValueCacheValid(
        #   acNode hNode,
        #   bool8_t* pIsValid)
        harenac.acValueIsValueCacheValid(
            self.hxnode,
            byref(is_valid))

        return is_valid.value
