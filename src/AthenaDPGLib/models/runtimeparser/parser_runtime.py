# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass, field
import json
from typing import Callable

# Custom Library

# Custom Packages
from AthenaDPGLib.models.runtimeparser._parser import _Parser
from AthenaDPGLib.data.strings import (TAG, CALLBACK, DRAG_CALLBACK, DROP_CALLBACK)
from AthenaDPGLib.data.runtimeparser_mapping import (
    RUNTIMEPARSER_MAPPING_CONTEXTMANGERS, RUNTIMEPARSER_MAPPING_ITEMS_FULL
)

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
PRIMARY_WINDOW = "primary_window"
SKIP_ATTRIB = {"_children", CALLBACK, DRAG_CALLBACK, DROP_CALLBACK}
SKIP_ATTRIB_GRID_LAYOUT = {"_columns", "_rows","_children","_row_all"}
def skip_attrib(attrib:dict, skipables:set) -> dict:
    return {k:v for k, v in attrib.items() if k not in skipables}

def map_attrib_policy(attrib:dict) -> dict:
    if "policy" in attrib:
        attrib["policy"] = getattr(dpg, attrib["policy"])
    return attrib

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class ParserRuntime(_Parser):
    tags:set = field(init=False, default_factory=set)

    def parse_single_file(self, filepath_input:str):
        """dpg.create_context() has to be run beforehand"""
        with open(filepath_input, "r") as file:
            document = json.load(file)

        match document["dpg"]:
            case {"mode":"full","_children":children,}:
                self._parse_recursive(parent=children)
            case {"mode":"partial","_children":children,}:
                self._parse_recursive(parent=children)
            case _:
                raise RuntimeError

    def parse_multiple_files(self, filepaths:list[str]):
        for filepath in filepaths:
            self.parse_single_file(filepath)

    def _parse_recursive(self, parent:list):
        for item, attrib in ((k,v) for i in parent for k, v in i.items()): #type: str, dict
            self.check_duplicate_tag(item, attrib)
            if item in RUNTIMEPARSER_MAPPING_CONTEXTMANGERS:
                self.dpg_context_manager(
                    fnc=RUNTIMEPARSER_MAPPING_CONTEXTMANGERS[item],
                    attrib=attrib
                )

            elif item in RUNTIMEPARSER_MAPPING_ITEMS_FULL:
                RUNTIMEPARSER_MAPPING_ITEMS_FULL[item](**attrib)

            # for special cases
            elif item in self.custom_dpg:
                self.custom_dpg[item](self,item,attrib)

            else:
                raise ValueError(item)

    def check_duplicate_tag(self, item:str, attrib:dict):
        if TAG in attrib:
            if (tag := attrib[TAG]) in self.tags:
                raise ValueError(f"'{tag}' was already present in the tags dictionary.\nRaised in the '{item}' item")
            self.tags.add(tag)

    def dpg_context_manager(self, fnc:Callable , attrib:dict):
            with fnc(**skip_attrib(attrib, SKIP_ATTRIB)):
                self._parse_recursive(parent=attrib["_children"])

    # ------------------------------------------------------------------------------------------------------------------
    # - Special DPG items -
    # ------------------------------------------------------------------------------------------------------------------
    @_Parser.custom_dpg_item
    def primary_window(self, _: str, attrib: dict):
        attrib[TAG] = PRIMARY_WINDOW
        self.dpg_context_manager(
            fnc=dpg.window,
            attrib=attrib
        )
        dpg.set_primary_window(PRIMARY_WINDOW, True)

    @_Parser.custom_dpg_item
    def viewport(self, _:str, attrib:dict):
        dpg.create_viewport(**attrib)

    @_Parser.custom_dpg_item
    def grid_layout(self, _:str, attrib:dict):
        with dpg.table(**map_attrib_policy(skip_attrib(attrib, SKIP_ATTRIB_GRID_LAYOUT)), header_row=False):
            # columns
            for column in attrib["_columns"]:
                dpg.add_table_column(**column)

            # rows with the items
            if "_rows" in attrib:
                attrib_rows = attrib["_rows"]
            elif "_row_all" in attrib:
                attrib_rows = (attrib["_row_all"],)*len(attrib["_children"])
            else:
                attrib_rows = ({},)*len(attrib["_children"])

            for attrib_row, child in zip(attrib_rows, attrib["_children"]):
                with dpg.table_row(**attrib_row):
                   self._parse_recursive(child)
