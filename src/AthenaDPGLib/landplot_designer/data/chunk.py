# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

import collections

# Custom Library
from AthenaLib.constants.types import CV_INT,CV_COLOR

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class _ChunkSideSizes:
    chunk_0:CV_INT =  16*(2**0)
    chunk_1:CV_INT =  16*(2**1)
    chunk_2:CV_INT =  16*(2**2)
    chunk_3:CV_INT =  16*(2**3)
    chunk_4:CV_INT =  16*(2**4)
    chunk_5:CV_INT =  16*(2**5)
    chunk_6:CV_INT =  16*(2**6)
    chunk_7:CV_INT =  16*(2**7)
    chunk_8:CV_INT =  16*(2**8)
    chunk_9:CV_INT =  16*(2**9)
    chunk_10:CV_INT = 16*(2**10)
    chunk_11:CV_INT = 16*(2**11)
    chunk_12:CV_INT = 16*(2**12)
    chunk_13:CV_INT = 16*(2**13)
    chunk_14:CV_INT = 16*(2**14)
    chunk_15:CV_INT = 16*(2**15)

    def __iter__(cls):
        yield cls.chunk_0
        yield cls.chunk_1
        yield cls.chunk_2
        yield cls.chunk_3
        yield cls.chunk_4
        yield cls.chunk_5
        yield cls.chunk_6
        yield cls.chunk_7
        yield cls.chunk_8
        yield cls.chunk_9
        yield cls.chunk_10
        yield cls.chunk_11
        yield cls.chunk_12
        yield cls.chunk_13
        yield cls.chunk_14
        yield cls.chunk_15


class _ChunkColors:
    chunk_0:CV_COLOR =  (127,0,0,127)
    chunk_1:CV_COLOR =  (0,127,0,127)
    chunk_2:CV_COLOR =  (0,0,127,127)
    chunk_3:CV_COLOR =  (127,127,0,127)
    chunk_4:CV_COLOR =  (0,127,127,127)
    chunk_5:CV_COLOR =  (127,0,127,127)

    chunk_6:CV_COLOR =  (127,64,64,127)
    chunk_7:CV_COLOR =  (64,127,64,127)
    chunk_8:CV_COLOR =  (64,64,127,127)
    chunk_9:CV_COLOR =  (127,127,64,127)
    chunk_10:CV_COLOR = (64,127,127,127)
    chunk_11:CV_COLOR = (127,64,127,127)

    chunk_12:CV_COLOR = (127,191,191,127)
    chunk_13:CV_COLOR = (191,127,191,127)
    chunk_14:CV_COLOR = (191,191,127,127)
    chunk_15:CV_COLOR = (127,127,191,127)

    def __iter__(cls):
        yield cls.chunk_0
        yield cls.chunk_1
        yield cls.chunk_2
        yield cls.chunk_3
        yield cls.chunk_4
        yield cls.chunk_5
        yield cls.chunk_6
        yield cls.chunk_7
        yield cls.chunk_8
        yield cls.chunk_9
        yield cls.chunk_10
        yield cls.chunk_11
        yield cls.chunk_12
        yield cls.chunk_13
        yield cls.chunk_14
        yield cls.chunk_15

# ----------------------------------------------------------------------------------------------------------------------
ChunkSideSizes = _ChunkSideSizes()
ChunkColors = _ChunkColors()