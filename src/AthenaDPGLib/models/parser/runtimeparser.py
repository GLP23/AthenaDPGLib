# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
import xml.etree.ElementTree as ET
from dataclasses import dataclass

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
    document:ET.ElementTree
    root:ET.Element
    callbacks:Callbacks

    def __init__(self, filepath_input:str, callbacks:Callbacks=None):
        # todo check if the file exists or not
        self.filepath = filepath_input
        self.callbacks = callbacks if callbacks is not None else Callbacks()

    def parse(self):
        """dpg.create_context() has to be run beforehand"""
        with open(self.filepath, "r") as file:
            self.document = ET.parse(file)

        self.root = self.document.getroot()
        match self.root:
            case ET.Element(tag="dpg", attrib={"mode":"full",}):
                self._parse_recursive(parent=self.root)
            case ET.Element(tag="dpg", attrib={"mode":"single",}):
                # todo something else here
                self._parse_recursive(parent=self.root)

    def _parse_recursive(self, parent:ET.Element):
        for child in parent: #type: ET.Element
            if (tag:=child.tag) in RUNTIMEPARSER_MAPPING_CONTEXTMANGERS:
                with RUNTIMEPARSER_MAPPING_CONTEXTMANGERS[tag](**child.attrib):
                    self._parse_recursive(parent=child)

            elif tag in RUNTIMEPARSER_MAPPING_ITEMS_STRIPPED:
                if "check" in child.attrib:
                    child.attrib["check"] = True if child.attrib["check"] in TRUTHY else False
                if "callback" in child.attrib:
                    child.attrib["callback"] = self.callbacks[child.attrib["callback"]]
                RUNTIMEPARSER_MAPPING_ITEMS_STRIPPED[tag](**child.attrib)

            else:
                # for special cases
                match child:
                    case ET.Element(tag="primary_window", attrib=attrib):
                        with dpg.window(**attrib, tag="primary_window"):
                            self._parse_recursive(parent=child)
                        dpg.set_primary_window("primary_window", True)

                    case ET.Element(tag="viewport", attrib=attrib):
                        dpg.create_viewport(**attrib)
