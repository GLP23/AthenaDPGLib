# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
DPG_TABLE_POLICIES:dict[str|int : int] = {
    "mvtable_sizingfixedfit": dpg.mvTable_SizingFixedFit,
    "mvtable_sizingfixedsame": dpg.mvTable_SizingFixedSame,
    "mvtable_sizingstretchprop": dpg.mvTable_SizingStretchProp,
    "mvtable_sizingstretchsame": dpg.mvTable_SizingStretchSame,

    # Easier mapping for people who don't want to write the ``mvTable_Sizing` bit
    "fixedfit": dpg.mvTable_SizingFixedFit,
    "fixedsame": dpg.mvTable_SizingFixedSame,
    "stretchprop": dpg.mvTable_SizingStretchProp,
    "stretchsame": dpg.mvTable_SizingStretchSame,

    # if for some reason the person knows the actual int values
    #   they can be used as well
    8192: dpg.mvTable_SizingFixedFit,
    16384: dpg.mvTable_SizingFixedSame,
    24576: dpg.mvTable_SizingStretchProp,
    32768: dpg.mvTable_SizingStretchSame,
}