# -*- encoding: utf-8 -*-

from ctypes import *

class PackedTags2TagsPart(Structure):
    _fields_ = [('sequenceNumber', c_uint32),
                ('objectId', c_uint32),
                ('chunkId', c_uint32),
                ('byteCount', c_uint32)]

class ECCOther(Structure):
    _fields_ = [('colParity', c_uint8),
                ('lineParity', c_uint32),
                ('lineParityPrime', c_uint32)]

class PackedTags2(Structure):
    _fields_ = [('t', PackedTags2TagsPart),
                ('ecc', ECCOther)]

MAX_NAME_LENGTH = 255
MAX_ALIAS_LENGTH = 159

class ObjectHeader(Structure):
    _fields_ = [('type', c_int32),
                ('parentObjectId', c_int32),
                ('sum__NoLongerUsed', c_uint16),
                ('name', c_char*(MAX_NAME_LENGTH+1)),
                ('yst_mode', c_uint32),
                ('yst_uid', c_uint32),
                ('yst_gid', c_uint32),
                ('yst_atime', c_uint32),
                ('yst_mtime', c_uint32),
                ('yst_ctime', c_uint32),
                ('fileSize', c_int32),
                ('equivalentObjectId', c_int32),
                ('alias', c_char*(MAX_ALIAS_LENGTH + 1)),
                ('yst_rdev', c_uint32),
                ('roomToGrow', c_uint32*6),
                ('inbandShadowsObject', c_uint32),
                ('inbandIsShrink', c_uint32),
                ('reservedSpace', c_uint32*2),
                ('shadowsObject', c_int32),
                ('isShrink', c_uint32),
                ]

OBJECTID_ROOT = 1
CHUNK_SIZE = 2048
SPARE_SIZE = 64

# yaffs object types
UNKNOWN = 1
FILE = 1
SYMLINK = 2
DIRECTORY = 3
HARDLINK = 4
SPECIAL = 5
