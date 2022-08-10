# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
import xml.etree.ElementTree as ET
from dataclasses import dataclass
import json

# Custom Library
from AthenaLib.data.text import TRUTHY

# Custom Packages
from AthenaDPGLib.data.runtimeparser_mapping import (
    RUNTIMEPARSER_MAPPING_CONTEXTMANGERS, RUNTIMEPARSER_MAPPING_ITEMS_STRIPPED
)

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
class Callbacks:
    pass

    def __getitem__(self, item):
        if item in self.__dir__():
            return getattr(self,item)
        else:
            raise ValueError(item)

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, init=False)
class RuntimeParser:
    filepath:str
    document:dict
    callbacks:Callbacks

    def __init__(self, filepath_input:str, callbacks:Callbacks=None):
        # todo check if the file exists or not
        self.filepath = filepath_input
        self.callbacks = callbacks if callbacks is not None else Callbacks()

    def parse(self):
        """dpg.create_context() has to be run beforehand"""
        with open(self.filepath, "r") as file:
            self.document = json.load(file)

        match self.document["dpg"]:
            case {"mode":0,"items":items,}:
                self._parse_recursive(parent=items)
            case _:
                raise RuntimeError


    def _parse_recursive(self, parent:list):
        for item in parent: #type:dict
            for tag, attrib in item.items(): #type: str, dict
                if tag in RUNTIMEPARSER_MAPPING_CONTEXTMANGERS:
                    child_items = attrib["items"]
                    attrib.pop("items")
                    with RUNTIMEPARSER_MAPPING_CONTEXTMANGERS[tag](**attrib):
                        self._parse_recursive(parent=child_items)

                elif tag in RUNTIMEPARSER_MAPPING_ITEMS_STRIPPED:
                    if "callback" in attrib:
                        attrib["callback"] = self.callbacks[attrib["callback"]]
                    RUNTIMEPARSER_MAPPING_ITEMS_STRIPPED[tag](**attrib)

                else:
                    # for special cases
                    match tag:
                        case "primary_window":
                            child_items = attrib["items"]
                            attrib.pop("items")
                            with dpg.window(**attrib, tag="primary_window"):
                                self._parse_recursive(parent=child_items)
                            dpg.set_primary_window("primary_window", True)

                        case "viewport":
                            dpg.create_viewport(**attrib)
