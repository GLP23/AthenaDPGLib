# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
import xml.etree.ElementTree as ET
from dataclasses import dataclass

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, init=False)
class Parser:
    filepath:str
    document:ET.ElementTree
    root:ET.Element
    callbacks:dict

    def __init__(self, filepath_input:str, callbacks:dict=None):
        # todo check if the file exists or not
        self.filepath = filepath_input
        self.callbacks = callbacks if callbacks is not None else {}

    def parse(self):
        with open(self.filepath, "r") as file:
            self.document = ET.parse(file)

        self.root = self.document.getroot()
        if self.root.tag != "DPG":
            raise ValueError("XML root tag has to be a DPG tag")

        for prim_win in self.root.iter("primary_window"):
            with dpg.window(**prim_win.attrib, tag="primary_window"):
                self._parse_recursive(parent=prim_win)
            dpg.set_primary_window("primary_window", True)
            break
        else:
            self._parse_recursive(parent=self.root)

    def _parse_recursive(self, parent:ET.Element):
        for child in parent: #type: ET.Element
            match child:
                case ET.Element(tag="window", attrib={"label": label, **attrib}):
                    if child: # check if the window has children of its own
                        with dpg.window(label=label, **attrib):
                            self._parse_recursive(parent=child)
                    else:
                        dpg.add_window(label=label, **attrib)

                case ET.Element(tag="text", attrib=attrib, text=text):
                    dpg.add_text(text if text else None, **attrib)

                case ET.Element(tag="button", attrib=attrib):
                    if "callback" in attrib:
                        attrib["callback"] = self.callbacks[attrib["callback"]]
                    dpg.add_button(**attrib)
