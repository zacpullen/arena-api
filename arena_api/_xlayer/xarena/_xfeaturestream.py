
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

from ctypes import byref

from arena_api._xlayer.xarena.arenac import harenac
from arena_api._xlayer.xarena.arenac_types import (acFeatureStream, acNodeMap,
                                                   char_ptr)


def xFeatureStreamCreate(h_nodemap):
    nodemap = acNodeMap(h_nodemap)
    featurestream = acFeatureStream(None)
    # AC_ERROR acFeatureStreamCreate(
    #   acNodeMap hNodeMap,
    #   acFeatureStream* phFeatureStream)
    harenac.acFeatureStreamCreate(
        nodemap,
        byref(featurestream))

    return featurestream.value


def xFeatureStreamDestroy(featurestream):
    featurestream = acFeatureStream(featurestream)
    # AC_ERROR acFeatureStreamDestroy(
    #   acFeatureStream hFeatureStream)
    harenac.acFeatureStreamDestroy(
        featurestream)


class _xFeaturestream():

    def __init__(self, h_featurestream):
        # TODO SFW-2546
        if not h_featurestream:
            raise TypeError('h_featurestream handle is None')
        self.h_featurestream = acFeatureStream(h_featurestream)

    def xFeatureStreamSelect(self, feature_name):

        feature_name_p = char_ptr(feature_name.encode())
        # AC_ERROR acFeatureStreamSelect(
        #   acFeatureStream hFeatureStream,
        #   char* pFeatureName)
        harenac.acFeatureStreamSelect(
            self.h_featurestream,
            feature_name_p)

    def xFeatureStreamWrite(self):

        # AC_ERROR acFeatureStreamWrite(
        #   acFeatureStream hFeatureStream)
        harenac.acFeatureStreamWrite(
            self.h_featurestream)

    def xFeatureStreamWriteFileName(self, file_name):

        file_name_p = char_ptr(file_name.encode())
        # AC_ERROR acFeatureStreamWriteFileName(
        #   acFeatureStream hFeatureStream,
        #   char* pFileName)
        harenac.acFeatureStreamWriteFileName(
            self.h_featurestream,
            file_name_p)

    def xFeatureStreamRead(self):

        # AC_ERROR acFeatureStreamRead(
        #   acFeatureStream hFeatureStream)
        harenac.acFeatureStreamRead(
            self.h_featurestream)

    def xFeatureStreamReadFileName(self, file_name):

        file_name_p = char_ptr(file_name.encode())
        # AC_ERROR acFeatureStreamReadFileName(
        #   acFeatureStream hFeatureStream,
        #   char* pFileName)
        harenac.acFeatureStreamReadFileName(
            self.h_featurestream,
            file_name_p)
