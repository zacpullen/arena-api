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

from enum import IntEnum

# TODO SFW-2186


class InterfaceType(IntEnum):
    INTEGER = 2
    BOOLEAN = 3
    COMMAND = 4
    FLOAT = 5
    STRING = 6
    REGISTER = 7
    CATEGORY = 8
    ENUMERATION = 9
    ENUMENTRY = 10


class AccessMode(IntEnum):
    NI = 0
    NA = 1
    WO = 2
    RO = 3
    RW = 4
    UNDEFINED = 5


class CachingMode(IntEnum):
    NO_CACHE = 0
    WRITE_THROUGH = 1
    WRITE_AROUND = 2
    UNDEFINED = 3


class Namespace(IntEnum):
    CUSTOM = 0
    STANDARD = 1
    UNDEFINED = 2


class Visibility(IntEnum):
    BEGINNER = 0
    EXPERT = 1
    GURU = 2
    INVISIBLE = 3
    UNDEFINED = 99


class IncMode(IntEnum):
    NONE = 0
    FIXED = 1
    LIST = 2


class Representation(IntEnum):
    LINEAR = 0
    LOGARITHMIC = 1
    BOOLEAN = 2
    PURE_NUMBER = 3
    HEX_NUMBER = 4
    IPV4_ADDRESS = 5
    MAC_ADDRESS = 6
    UNDEFINED = 7


class DisplayNotation(IntEnum):
    AUTOMATIC = 0
    FIXED = 1
    SCIENTIFIC = 2
    UNDEFINED = 3


class PayloadType(IntEnum):
    IMAGE = 0x0001
    IMAGE_EXTENDED_CHUNK = 0x4001
    CHUNKDATA = 0x0004


class PixelEndianness(IntEnum):
    UNKNOWN = 0
    LITTLE = 1
    BIG = 2


class BayerAlgorithm(IntEnum):
    UNKNOWN = 0
    DIRECTIONAL_INTERPOLATION = 1
    ADAPTIVE_HOMOGENEITY_DIRECTED = 2


# class Pixelformat(MultiValueEnum):
class PixelFormat(IntEnum):
    
    # Monochrome 1-bit packed
    Mono1p = 0x01010037
    # Monochrome 2-bit packed
    Mono2p = 0x01020038
    # Monochrome 4-bit packed
    Mono4p = 0x01040039
    # Monochrome 8-bit
    Mono8 = 0x01080001
    # Monochrome 8-bit signed
    Mono8s = 0x01080002
    # Monochrome 10-bit unpacked
    Mono10 = 0x01100003
    # Monochrome 10-bit packed
    Mono10p = 0x010A0046
    # Monochrome 12-bit unpacked
    Mono12 = 0x01100005
    # Monochrome 12-bit packed
    Mono12p = 0x010C0047
    # Monochrome 14-bit unpacked
    Mono14 = 0x01100025
    # Monochrome 16-bit
    Mono16 = 0x01100007
    # Bayer Blue-Green 8-bit
    BayerBG8 = 0x0108000B
    # Bayer Blue-Green 10-bit unpacked
    BayerBG10 = 0x0110000F
    # Bayer Blue-Green 10-bit packed
    BayerBG10p = 0x010A0052
    # Bayer Blue-Green 12-bit unpacked
    BayerBG12 = 0x01100013
    # Bayer Blue-Green 12-bit packed
    BayerBG12p = 0x010C0053
    # Bayer Blue-Green 16-bit
    BayerBG16 = 0x01100031
    # Bayer Green-Blue 8-bit
    BayerGB8 = 0x0108000A
    # Bayer Green-Blue 10-bit unpacked
    BayerGB10 = 0x0110000E
    # Bayer Green-Blue 10-bit packed
    BayerGB10p = 0x010A0054
    # Bayer Green-Blue 12-bit unpacked
    BayerGB12 = 0x01100012
    # Bayer Green-Blue 12-bit packed
    BayerGB12p = 0x010C0055
    # Bayer Green-Blue 16-bit
    BayerGB16 = 0x01100030
    # Bayer Green-Red 8-bit
    BayerGR8 = 0x01080008
    # Bayer Green-Red 10-bit unpacked
    BayerGR10 = 0x0110000C
    # Bayer Green-Red 10-bit packed
    BayerGR10p = 0x010A0056
    # Bayer Green-Red 12-bit unpacked
    BayerGR12 = 0x01100010
    # Bayer Green-Red 12-bit packed
    BayerGR12p = 0x010C0057
    # Bayer Green-Red 16-bit
    BayerGR16 = 0x0110002E
    # Bayer Red-Green 8-bit
    BayerRG8 = 0x01080009
    # Bayer Red-Green 10-bit unpacked
    BayerRG10 = 0x0110000D
    # Bayer Red-Green 10-bit packed
    BayerRG10p = 0x010A0058
    # Bayer Red-Green 12-bit unpacked
    BayerRG12 = 0x01100011
    # Bayer Red-Green 12-bit packed
    BayerRG12p = 0x010C0059
    # Bayer Red-Green 16-bit
    BayerRG16 = 0x0110002F
    # Red-Green-Blue-alpha 8-bit
    RGBa8 = 0x02200016
    # Red-Green-Blue-alpha 10-bit unpacked
    RGBa10 = 0x0240005F
    # Red-Green-Blue-alpha 10-bit packed
    RGBa10p = 0x02280060
    # Red-Green-Blue-alpha 12-bit unpacked
    RGBa12 = 0x02400061
    # Red-Green-Blue-alpha 12-bit packed
    RGBa12p = 0x02300062
    # Red-Green-Blue-alpha 14-bit unpacked
    RGBa14 = 0x02400063
    # Red-Green-Blue-alpha 16-bit
    RGBa16 = 0x02400064
    # Red-Green-Blue 8-bit
    RGB8 = 0x02180014
    # Red-Green-Blue 8-bit planar
    RGB8_Planar = 0x02180021
    # Red-Green-Blue 10-bit unpacked
    RGB10 = 0x02300018
    # Red-Green-Blue 10-bit unpacked planar
    RGB10_Planar = 0x02300022
    # Red-Green-Blue 10-bit packed
    RGB10p = 0x021E005C
    # Red-Green-Blue 10-bit packed into 32-bit
    RGB10p32 = 0x0220001D
    # Red-Green-Blue 12-bit unpacked
    RGB12 = 0x0230001A
    # Red-Green-Blue 12-bit unpacked planar
    RGB12_Planar = 0x02300023
    # Red-Green-Blue 12-bit packed  
    RGB12p = 0x0224005D
    # Red-Green-Blue 14-bit unpacked
    RGB14 = 0x0230005E
    # Red-Green-Blue 16-bit  
    RGB16 = 0x02300033
    # Red-Green-Blue 16-bit planar
    RGB16_Planar = 0x02300024
    # Red-Green-Blue 5/6/5-bit packed
    RGB565p = 0x02100035
    # Blue-Green-Red-alpha 8-bit
    BGRa8 = 0x02200017
    # Blue-Green-Red-alpha 10-bit unpacked
    BGRa10 = 0x0240004C
    # Blue-Green-Red-alpha 10-bit packed
    BGRa10p = 0x0228004D
    # Blue-Green-Red-alpha 12-bit unpacked
    BGRa12 = 0x0240004E
    # Blue-Green-Red-alpha 12-bit packed
    BGRa12p = 0x0230004F
    # Blue-Green-Red-alpha 14-bit unpacked
    BGRa14 = 0x02400050
    # Blue-Green-Red-alpha 16-bit
    BGRa16 = 0x02400051
    # Blue-Green-Red 8-bit
    BGR8 = 0x02180015
    # Blue-Green-Red 10-bit unpacked
    BGR10 = 0x02300019
    # Blue-Green-Red 10-bit packed
    BGR10p = 0x021E0048
    # Blue-Green-Red 12-bit unpacked
    BGR12 = 0x0230001B
    # Blue-Green-Red 12-bit packed
    BGR12p = 0x02240049
    # Blue-Green-Red 14-bit unpacked
    BGR14 = 0x0230004A
    # Blue-Green-Red 16-bit
    BGR16 = 0x0230004B
    # Blue-Green-Red 5/6/5-bit packed
    BGR565p = 0x02100036
    # Red 8-bit
    R8 = 0x010800C9
    # Red 10-bit
    R10 = 0x010A00CA
    # Red 12-bit
    R12 = 0x010C00CB
    # Red 16-bit
    R16 = 0x011000CC
    # Green 8-bit
    G8 = 0x010800CD
    # Green 10-bit
    G10 = 0x010A00CE
    # Green 12-bit
    G12 = 0x010C00CF
    # Green 16-bit
    G16 = 0x011000D0
    # Blue 8-bit
    B8 = 0x010800D1
    # Blue 10-bit
    B10 = 0x010A00D2
    # Blue 12-bit
    B12 = 0x010C00D3
    # Blue 16-bit
    B16 = 0x011000D4
    # 3D coordinate A-B-C 8-bit
    Coord3D_ABC8 = 0x021800B2
    # 3D coordinate A-B-C 8-bit planar
    Coord3D_ABC8_Planar = 0x021800B3
    # 3D coordinate A-B-C 10-bit packed
    Coord3D_ABC10p = 0x021E00DB
    # 3D coordinate A-B-C 10-bit packed planar
    Coord3D_ABC10p_Planar = 0x021E00DC
    # 3D coordinate A-B-C 12-bit packed
    Coord3D_ABC12p = 0x022400DE
    # 3D coordinate A-B-C 12-bit packed planar
    Coord3D_ABC12p_Planar = 0x022400DF
    # 3D coordinate A-B-C 16-bit
    Coord3D_ABC16 = 0x023000B9
    # 3D coordinate A-B-C 16-bit planar
    Coord3D_ABC16_Planar = 0x023000BA
    # 3D coordinate A-B-C 32-bit floating point
    Coord3D_ABC32f = 0x026000C0
    # 3D coordinate A-B-C 32-bit floating point planar
    Coord3D_ABC32f_Planar = 0x026000C1
    # 3D coordinate A-C 8-bit
    Coord3D_AC8 = 0x021000B4
    # 3D coordinate A-C 8-bit planar
    Coord3D_AC8_Planar = 0x021000B5
    # 3D coordinate A-C 10-bit packed
    Coord3D_AC10p = 0x021400F0
    # 3D coordinate A-C 10-bit packed planar
    Coord3D_AC10p_Planar = 0x021400F1
    # 3D coordinate A-C 12-bit packed
    Coord3D_AC12p = 0x021800F2
    # 3D coordinate A-C 12-bit packed planar
    Coord3D_AC12p_Planar = 0x021800F3
    # 3D coordinate A-C 16-bit
    Coord3D_AC16 = 0x022000BB
    # 3D coordinate A-C 16-bit planar
    Coord3D_AC16_Planar = 0x022000BC
    # 3D coordinate A-C 32-bit floating point
    Coord3D_AC32f = 0x024000C2
    # 3D coordinate A-C 32-bit floating point planar
    Coord3D_AC32f_Planar = 0x024000C3
    # 3D coordinate A 8-bit
    Coord3D_A8 = 0x010800AF
    # 3D coordinate A 10-bit packed
    Coord3D_A10p = 0x010A00D5
    # 3D coordinate A 12-bit packed
    Coord3D_A12p = 0x010C00D8
    # 3D coordinate A 16-bit
    Coord3D_A16 = 0x011000B6
    # 3D coordinate A 32-bit floating point
    Coord3D_A32f = 0x012000BD
    # 3D coordinate B 8-bit
    Coord3D_B8 = 0x010800B0
    # 3D coordinate B 10-bit packed
    Coord3D_B10p = 0x010A00D6
    # 3D coordinate B 12-bit packed
    Coord3D_B12p = 0x010C00D9
    # 3D coordinate B 16-bit
    Coord3D_B16 = 0x011000B7
    # 3D coordinate B 32-bit floating point
    Coord3D_B32f = 0x012000BE
    # 3D coordinate C 8-bit
    Coord3D_C8 = 0x010800B1
    # 3D coordinate C 10-bit packed
    Coord3D_C10p = 0x010A00D7
    # 3D coordinate C 12-bit packed
    Coord3D_C12p = 0x010C00DA
    # 3D coordinate C 16-bit
    Coord3D_C16 = 0x011000B8
    # 3D coordinate C 32-bit floating point
    Coord3D_C32f = 0x012000BF
    # Confidence 1-bit unpacked
    Confidence1 = 0x010800C4
    # Confidence 1-bit packed
    Confidence1p = 0x010100C5
    # Confidence 8-bit
    Confidence8 = 0x010800C6
    # Confidence 16-bit
    Confidence16 = 0x011000C7
    # Confidence 32-bit floating point
    Confidence32f = 0x012000C8
    # Bi-color Blue/Green - Red/Green 8-bit
    BiColorBGRG8 = 0x021000A6
    # Bi-color Blue/Green - Red/Green 10-bit unpacked
    BiColorBGRG10 = 0x022000A9
    # Bi-color Blue/Green - Red/Green 10-bit packed
    BiColorBGRG10p = 0x021400AA
    # Bi-color Blue/Green - Red/Green 12-bit unpacked
    BiColorBGRG12 = 0x022000AD
    # Bi-color Blue/Green - Red/Green 12-bit packed
    BiColorBGRG12p = 0x021800AE
    # Bi-color Red/Green - Blue/Green 8-bit
    BiColorRGBG8 = 0x021000A5
    # Bi-color Red/Green - Blue/Green 10-bit unpacked
    BiColorRGBG10 = 0x022000A7
    # Bi-color Red/Green - Blue/Green 10-bit packed
    BiColorRGBG10p = 0x021400A8
    # Bi-color Red/Green - Blue/Green 12-bit unpacked
    BiColorRGBG12 = 0x022000AB
    # Bi-color Red/Green - Blue/Green 12-bit packed
    BiColorRGBG12p = 0x021800AC
    # Sparse Color Filter #1 White-Blue-White-Green 8-bit
    SCF1WBWG8 = 0x01080067
    # Sparse Color Filter #1 White-Blue-White-Green 10-bit unpacked
    SCF1WBWG10 = 0x01100068
    # Sparse Color Filter #1 White-Blue-White-Green 10-bit packed
    SCF1WBWG10p = 0x010A0069
    # Sparse Color Filter #1 White-Blue-White-Green 12-bit unpacked
    SCF1WBWG12 = 0x0110006A
    # Sparse Color Filter #1 White-Blue-White-Green 12-bit packed
    SCF1WBWG12p = 0x010C006B
    # Sparse Color Filter #1 White-Blue-White-Green 14-bit unpacked
    SCF1WBWG14 = 0x0110006C
    # Sparse Color Filter #1 White-Blue-White-Green 16-bit unpacked
    SCF1WBWG16 = 0x0110006D
    # Sparse Color Filter #1 White-Green-White-Blue 8-bit
    SCF1WGWB8 = 0x0108006E
    # Sparse Color Filter #1 White-Green-White-Blue 10-bit unpacked
    SCF1WGWB10 = 0x0110006F
    # Sparse Color Filter #1 White-Green-White-Blue 10-bit packed
    SCF1WGWB10p = 0x010A0070
    # Sparse Color Filter #1 White-Green-White-Blue 12-bit unpacked
    SCF1WGWB12 = 0x01100071
    # Sparse Color Filter #1 White-Green-White-Blue 12-bit packed
    SCF1WGWB12p = 0x010C0072
    # Sparse Color Filter #1 White-Green-White-Blue 14-bit unpacked
    SCF1WGWB14 = 0x01100073
    # Sparse Color Filter #1 White-Green-White-Blue 16-bit
    SCF1WGWB16 = 0x01100074
    # Sparse Color Filter #1 White-Green-White-Red 8-bit
    SCF1WGWR8 = 0x01080075
    # Sparse Color Filter #1 White-Green-White-Red 10-bit unpacked
    SCF1WGWR10 = 0x01100076
    # Sparse Color Filter #1 White-Green-White-Red 10-bit packed
    SCF1WGWR10p = 0x010A0077
    # Sparse Color Filter #1 White-Green-White-Red 12-bit unpacked
    SCF1WGWR12 = 0x01100078
    # Sparse Color Filter #1 White-Green-White-Red 12-bit packed
    SCF1WGWR12p = 0x010C0079
    # Sparse Color Filter #1 White-Green-White-Red 14-bit unpacked
    SCF1WGWR14 = 0x0110007A
    # Sparse Color Filter #1 White-Green-White-Red 16-bit
    SCF1WGWR16 = 0x0110007B
    # Sparse Color Filter #1 White-Red-White-Green 8-bit
    SCF1WRWG8 = 0x0108007C
    # Sparse Color Filter #1 White-Red-White-Green 10-bit unpacked
    SCF1WRWG10 = 0x0110007D
    # Sparse Color Filter #1 White-Red-White-Green 10-bit packed
    SCF1WRWG10p = 0x010A007E
    # Sparse Color Filter #1 White-Red-White-Green 12-bit unpacked
    SCF1WRWG12 = 0x0110007F
    # Sparse Color Filter #1 White-Red-White-Green 12-bit packed
    SCF1WRWG12p = 0x010C0080
    # Sparse Color Filter #1 White-Red-White-Green 14-bit unpacked
    SCF1WRWG14 = 0x01100081
    # Sparse Color Filter #1 White-Red-White-Green 16-bit
    SCF1WRWG16 = 0x01100082
    # YCbCr 4:4:4 8-bit
    YCbCr8 = 0x0218005B
    # YCbCr 4:4:4 8-bit
    YCbCr8_CbYCr = 0x0218003A
    # YCbCr 4:4:4 10-bit unpacked
    YCbCr10_CbYCr = 0x02300083
    # YCbCr 4:4:4 10-bit packed
    YCbCr10p_CbYCr = 0x021E0084
    # YCbCr 4:4:4 12-bit unpacked
    YCbCr12_CbYCr = 0x02300085
    # YCbCr 4:4:4 12-bit packed
    YCbCr12p_CbYCr = 0x02240086
    # YCbCr 4:1:1 8-bit
    YCbCr411_8 = 0x020C005A
    # YCbCr 4:1:1 8-bit
    YCbCr411_8_CbYYCrYY = 0x020C003C
    # YCbCr 4:2:2 8-bit
    YCbCr422_8 = 0x0210003B
    # YCbCr 4:2:2 8-bit
    YCbCr422_8_CbYCrY = 0x02100043
    # YCbCr 4:2:2 10-bit unpacked
    YCbCr422_10 = 0x02200065
    # YCbCr 4:2:2 10-bit unpacked
    YCbCr422_10_CbYCrY = 0x02200099
    # YCbCr 4:2:2 10-bit packed
    YCbCr422_10p = 0x02140087
    # YCbCr 4:2:2 10-bit packed
    YCbCr422_10p_CbYCrY = 0x0214009A
    # YCbCr 4:2:2 12-bit unpacked
    YCbCr422_12 = 0x02200066
    # YCbCr 4:2:2 12-bit unpacked
    YCbCr422_12_CbYCrY = 0x0220009B
    # YCbCr 4:2:2 12-bit packed
    YCbCr422_12p = 0x02180088
    # YCbCr 4:2:2 12-bit packed
    YCbCr422_12p_CbYCrY = 0x0218009C
    # YCbCr 4:4:4 8-bit BT.601
    YCbCr601_8_CbYCr = 0x0218003D
    # YCbCr 4:4:4 10-bit unpacked BT.601
    YCbCr601_10_CbYCr = 0x02300089
    # YCbCr 4:4:4 10-bit packed BT.601
    YCbCr601_10p_CbYCr = 0x021E008A
    # YCbCr 4:4:4 12-bit unpacked BT.601
    YCbCr601_12_CbYCr = 0x0230008B
    # YCbCr 4:4:4 12-bit packed BT.601
    YCbCr601_12p_CbYCr = 0x0224008C
    # YCbCr 4:1:1 8-bit BT.601
    YCbCr601_411_8_CbYYCrYY = 0x020C003F
    # YCbCr 4:2:2 8-bit BT.601
    YCbCr601_422_8 = 0x0210003E
    # YCbCr 4:2:2 8-bit BT.601
    YCbCr601_422_8_CbYCrY = 0x02100044
    # YCbCr 4:2:2 10-bit unpacked BT.601
    YCbCr601_422_10 = 0x0220008D
    # YCbCr 4:2:2 10-bit unpacked BT.601
    YCbCr601_422_10_CbYCrY = 0x0220009D
    # YCbCr 4:2:2 10-bit packed BT.601
    YCbCr601_422_10p = 0x0214008E
    # YCbCr 4:2:2 10-bit packed BT.601
    YCbCr601_422_10p_CbYCrY = 0x0214009E
    # YCbCr 4:2:2 12-bit unpacked BT.601
    YCbCr601_422_12 = 0x0220008F
    # YCbCr 4:2:2 12-bit unpacked BT.601
    YCbCr601_422_12_CbYCrY = 0x0220009F
    # YCbCr 4:2:2 12-bit packed BT.601
    YCbCr601_422_12p = 0x02180090
    # YCbCr 4:2:2 12-bit packed BT.601
    YCbCr601_422_12p_CbYCrY = 0x021800A0
    # YCbCr 4:4:4 8-bit BT.709
    YCbCr709_8_CbYCr = 0x02180040
    # YCbCr 4:4:4 10-bit unpacked BT.709
    YCbCr709_10_CbYCr = 0x02300091
    # YCbCr 4:4:4 10-bit packed BT.709
    YCbCr709_10p_CbYCr = 0x021E0092
    # YCbCr 4:4:4 12-bit unpacked BT.709
    YCbCr709_12_CbYCr = 0x02300093
    # YCbCr 4:4:4 12-bit packed BT.709
    YCbCr709_12p_CbYCr = 0x02240094
    # YCbCr 4:1:1 8-bit BT.709
    YCbCr709_411_8_CbYYCrYY = 0x020C0042
    # YCbCr 4:2:2 8-bit BT.709
    YCbCr709_422_8 = 0x02100041
    # YCbCr 4:2:2 8-bit BT.709
    YCbCr709_422_8_CbYCrY = 0x02100045
    # YCbCr 4:2:2 10-bit unpacked BT.709
    YCbCr709_422_10 = 0x02200095
    # YCbCr 4:2:2 10-bit unpacked BT.709
    YCbCr709_422_10_CbYCrY = 0x022000A1
    # YCbCr 4:2:2 10-bit packed BT.709
    YCbCr709_422_10p = 0x02140096
    # YCbCr 4:2:2 10-bit packed BT.709
    YCbCr709_422_10p_CbYCrY = 0x021400A2
    # YCbCr 4:2:2 12-bit unpacked BT.709
    YCbCr709_422_12 = 0x02200097
    # YCbCr 4:2:2 12-bit unpacked BT.709
    YCbCr709_422_12_CbYCrY = 0x022000A3
    # YCbCr 4:2:2 12-bit packed BT.709
    YCbCr709_422_12p = 0x02180098
    # YCbCr 4:2:2 12-bit packed BT.709
    YCbCr709_422_12p_CbYCrY = 0x021800A4
    # YCbCr 4:4:4 8-bit BT.2020
    YCbCr2020_8_CbYCr = 0x021800F4
    # YCbCr 4:4:4 10-bit unpacked BT.2020
    YCbCr2020_10_CbYCr = 0x023000F5
    # YCbCr 4:4:4 10-bit packed BT.2020
    YCbCr2020_10p_CbYCr = 0x021E00F6
    # YCbCr 4:4:4 12-bit unpacked BT.2020 
    YCbCr2020_12_CbYCr = 0x023000F7
    # YCbCr 4:4:4 12-bit packed BT.2020
    YCbCr2020_12p_CbYCr = 0x022400F8
    # YCbCr 4:1:1 8-bit BT.2020
    YCbCr2020_411_8_CbYYCrYY = 0x020C00F9
    # YCbCr 4:2:2 8-bit BT.2020 
    YCbCr2020_422_8 = 0x021000FA
    # YCbCr 4:2:2 8-bit BT.2020
    YCbCr2020_422_8_CbYCrY = 0x021000FB
    # YCbCr 4:2:2 10-bit unpacked BT.2020
    YCbCr2020_422_10 = 0x022000FC
    # YCbCr 4:2:2 10-bit unpacked BT.2020
    YCbCr2020_422_10_CbYCrY = 0x022000FD
    # YCbCr 4:2:2 10-bit packed BT.2020
    YCbCr2020_422_10p = 0x021400FE
    # YCbCr 4:2:2 10-bit packed BT.2020
    YCbCr2020_422_10p_CbYCrY = 0x021400FF
    # YCbCr 4:2:2 12-bit unpacked BT.2020
    YCbCr2020_422_12 = 0x02200100
    # YCbCr 4:2:2 12-bit unpacked BT.2020
    YCbCr2020_422_12_CbYCrY = 0x02200101
    # YCbCr 4:2:2 12-bit packed BT.2020
    YCbCr2020_422_12p = 0x02180102
    # YCbCr 4:2:2 12-bit packed BT.2020
    YCbCr2020_422_12p_CbYCrY = 0x02180103
    # YUV 4:4:4 8-bit
    YUV8_UYV = 0x02180020
    # YUV 4:1:1 8-bit
    YUV411_8_UYYVYY = 0x020C001E
    # YUV 4:2:2 8-bit
    YUV422_8 = 0x02100032
    # YUV 4:2:2 8-bit
    YUV422_8_UYVY = 0x0210001F
    # GigE Vision specific format, Monochrome 10-bit packed
    Mono10Packed = 0x010C0004
    # GigE Vision specific format, Monochrome 12-bit packed
    Mono12Packed = 0x010C0006
    # GigE Vision specific format, Bayer Blue-Green 10-bit packed
    BayerBG10Packed = 0x010C0029
    # GigE Vision specific format, Bayer Blue-Green 12-bit packed
    BayerBG12Packed = 0x010C002D
    # GigE Vision specific format, Bayer Green-Blue 10-bit packed
    BayerGB10Packed = 0x010C0028
    # GigE Vision specific format, Bayer Green-Blue 12-bit packed
    BayerGB12Packed = 0x010C002C
    # GigE Vision specific format, Bayer Green-Red 10-bit packed
    BayerGR10Packed = 0x010C0026
    # GigE Vision specific format, Bayer Green-Red 12-bit packed
    BayerGR12Packed = 0x010C002A
    # GigE Vision specific format, Bayer Red-Green 10-bit packed
    BayerRG10Packed = 0x010C0027
    # GigE Vision specific format, Bayer Red-Green 12-bit packed
    BayerRG12Packed = 0x010C002B
    # GigE Vision specific format, Red-Green-Blue 10-bit packed - variant 1
    RGB10V1Packed = 0x0220001C
    # GigE Vision specific format, Red-Green-Blue 12-bit packed - variant 1
    RGB12V1Packed = 0x02240034
    #
    PolarizeMono8 = 0x81080001
    #
    PolarizeMono12p = 0x810C0047
    #
    PolarizeMono12Packed = 0x810C0006
    #
    PolarizeMono12 = 0x81100008
    #
    PolarizeMono16 = 0x81100007
    #
    PolarizedAngles_0d_45d_90d_135d_Mono8 = 0x8220000F
    #
    PolarizedAngles_0d_45d_90d_135d_Mono12p = 0x8230001F
    #
    PolarizedAngles_0d_45d_90d_135d_Mono16 = 0x8240002F
    #
    PolarizedStokes_S0_S1_S2_Mono8 = 0x8218003F
    #
    PolarizedStokes_S0_S1_S2_Mono12p = 0x8224004F
    #
    PolarizedStokes_S0_S1_S2_Mono16 = 0x8230005F
    #
    PolarizedStokes_S0_S1_S2_S3_Mono8 = 0x8220006F
    #
    PolarizedStokes_S0_S1_S2_S3_Mono12p = 0x8230007F
    #
    PolarizedStokes_S0_S1_S2_S3_Mono16 = 0x8240008F
    #
    PolarizedAolp_Mono8 = 0x810800DF
    #
    PolarizedAolp_Mono12p = 0x810C00EF
    #
    PolarizedDolp_Mono8 = 0x810800BF
    #
    PolarizedDolp_Mono12p = 0x810C00CF
    #
    PolarizedDolpAolp_Mono8 = 0x8210009F
    #
    PolarizedDolpAolp_Mono12p = 0x821800AF
    #
    Coord3D_ABCY16s = 0x82400400
    #
    Coord3D_ABC16s = 0x82300401
    #
    Coord3D_C16s = 0x81100402
    #
    Coord3D_ABCY16 = 0x82400403
    #
    PolarizedAngles_0d_45d_90d_135d_BayerRG8 = 0x8220020F
    #
    PolarizedAngles_0d_45d_90d_135d_BayerRG12p = 0x8230021F
    #
    PolarizedStokes_S0_S1_S2_BayerRG8 = 0x8218023F
    #
    PolarizedStokes_S0_S1_S2_BayerRG12p = 0x8224024F
    #
    PolarizedStokes_S0_S1_S2_S3_BayerRG8 = 0x8220026F
    #
    PolarizedStokes_S0_S1_S2_S3_BayerRG12p = 0x8230027F
    #
    PolarizedAolp_BayerRG8 = 0x810802DF
    #
    PolarizedAolp_BayerRG12p = 0x810C02EF
    #
    PolarizedDolp_BayerRG8 = 0x810802BF
    #
    PolarizedDolp_BayerRG12p = 0x810C02CF
    #
    PolarizedDolpAolp_BayerRG8 = 0x8210029F
    #
    PolarizedDolpAolp_BayerRG12p = 0x821802AF
    
    InvalidPixelFormat = 0
