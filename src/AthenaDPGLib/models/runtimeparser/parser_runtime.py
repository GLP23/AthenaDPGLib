# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass, field
import json
from typing import Callable
import copy

# Custom Library

# Custom Packages
from AthenaDPGLib.data.runtimeparser_mapping import (
    RUNTIMEPARSER_MAPPING_CONTEXTMANGERS, RUNTIMEPARSER_MAPPING_ITEMS_FULL
)
from AthenaDPGLib.models.runtimeparser.callbacks import Callbacks

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
custom_dpg: dict[str:Callable] = {}
def custom_dpg_item(fnc):
    global custom_dpg
    custom_dpg[fnc.__name__] = fnc
    return fnc

PRIMARY_WINDOW = "primary_window"
SKIP_ATTRIB = {"_children"}
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
@dataclass(slots=True)
class ParserRuntime:
    callbacks:Callbacks = field(default_factory=Callbacks)
    tags:set = field(init=False, default_factory=set)
    custom_dpg: dict[str:Callable] = field(init=False)

    def __post_init__(self):
        global custom_dpg
        self.custom_dpg: dict[str:Callable] = custom_dpg

    def parse(self, filepath_input:str) -> ParserRuntime:
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
        return self

    def _parse_recursive(self, parent:list):
        for item, attrib in ((k,v) for i in parent for k, v in i.items()): #type: str, dict
            self.check_duplicate_tag(item, attrib)
            if item in RUNTIMEPARSER_MAPPING_CONTEXTMANGERS:
                self.dpg_context_manager(
                    fnc=RUNTIMEPARSER_MAPPING_CONTEXTMANGERS[item],
                    attrib=attrib
                )

            elif item in RUNTIMEPARSER_MAPPING_ITEMS_FULL:
                RUNTIMEPARSER_MAPPING_ITEMS_FULL[item](**self.assign_callbacks(attrib))

            # for special cases
            elif item in self.custom_dpg:
                self.custom_dpg[item](self,item,attrib)

            else:
                raise ValueError(item)

    def assign_callbacks(self, attrib:dict) -> dict:
        if "callback" in attrib:
            attrib["callback"] = self.callbacks.mapping_callback[attrib["callback"]]
        if "drag_callback" in attrib:
            attrib["drag_callback"] = self.callbacks.mapping_drag_callback[attrib["drag_callback"]]
        if "drop_callback" in attrib:
            attrib["drop_callback"] = self.callbacks.mapping_drop_callback[attrib["drop_callback"]]
        if "on_enter" in attrib:
            attrib["on_enter"] = self.callbacks.mapping_drag_callback[attrib["on_enter"]]
        return attrib

    def check_duplicate_tag(self, item:str, attrib:dict):
        if "tag" in attrib:
            if (tag := attrib["tag"]) in self.tags:
                raise ValueError(f"'{tag}' was already present in the tags dictionary.\nRaised in the '{item}' item")
            self.tags.add(tag)

    def dpg_context_manager(self, fnc:Callable , attrib:dict):
            with fnc(**self.assign_callbacks(skip_attrib(attrib, SKIP_ATTRIB))):
                self._parse_recursive(parent=attrib["_children"])

    # ------------------------------------------------------------------------------------------------------------------
    # - Special DPG items -
    # ------------------------------------------------------------------------------------------------------------------
    @custom_dpg_item
    def primary_window(self, _: str, attrib: dict):
        attrib["tag"] = PRIMARY_WINDOW
        self.dpg_context_manager(
            fnc=dpg.window,
            attrib=attrib
        )
        dpg.set_primary_window(PRIMARY_WINDOW, True)

    @custom_dpg_item
    def viewport(self, _:str, attrib:dict):
        dpg.create_viewport(**attrib)

    @custom_dpg_item
    def grid_layout(self, _:str, attrib:dict):
        with dpg.table(**map_attrib_policy(skip_attrib(attrib, SKIP_ATTRIB_GRID_LAYOUT)), header_row=False):
            # columns
            for column in attrib["_columns"]:
                dpg.add_table_column(**column)

            # rows with the items
            if "_rows" in attrib:
                for row_attrib, child in zip(attrib["_rows"], attrib["_children"]):
                    with dpg.table_row(**row_attrib):
                       self._parse_recursive(child)
            elif "_row_all" in attrib:
                for child in attrib["_children"]:
                    with dpg.table_row(**attrib["_row_all"]):
                       self._parse_recursive(child)
