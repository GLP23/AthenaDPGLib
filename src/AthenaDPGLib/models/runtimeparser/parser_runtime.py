# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass
import json

# Custom Library

# Custom Packages
from AthenaDPGLib.models.runtimeparser.attributes import Attributes
from AthenaDPGLib.data.text import (TAG, PRIMARY_WINDOW,DPG)
from AthenaDPGLib.data.runtimeparser_mapping import (
    RUNTIMEPARSER_MAPPING_CONTEXTMANGERS, RUNTIMEPARSER_MAPPING_ITEMS_FULL
)
from AthenaDPGLib.data.globals import global_custom_dpg_items, global_tags
from AthenaDPGLib.functions.decorators import custom_dpg_item
from AthenaDPGLib.data.exceptions import DPGJSONStructureError

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class ParserRuntime:
    # ------------------------------------------------------------------------------------------------------------------
    # - Actual Parsing -
    # ------------------------------------------------------------------------------------------------------------------
    def parse_file(self, filepath_input:str):
        """
        Parses the given json file at the `filepath_input` argument.
        Make sure that the dpg.create_context() has been run before this method is run
        """

        # Open file and  close as possible
        with open(filepath_input, "r") as file:
            document = json.load(file)

        try:
            # check for file structure
            dpg_data = document[DPG]
        except KeyError:
            raise DPGJSONStructureError(f"The file `{filepath_input}` had no usable structure")

        # parse with the correct parser
        match dpg_data:
            # version specific parsing
            #   Currently this means nothing as there is only one parser version
            #   This is meant for the future where there might eventually be multiple versions of parser,
            #       And this will ensure that the "old" ui files don't break
            case {"_parser": {"version": 0}, "_children":children,}:
                self._parse_recursive(parent=children)

            # If the version hasn't been specified , it will automatically pick the newest parser
            case {"_children":children,}:
                self._parse_recursive(parent=children)

            case _:
                raise DPGJSONStructureError(f"The file `{filepath_input}` had no usable structure")

    def _parse_recursive(self, parent:list):
        for item, attrib in ((k,v) for i in parent for k, v in i.items()): #type: str, dict
            if TAG in attrib:
                if (tag := attrib[TAG]) in global_tags:
                    raise DPGJSONStructureError(
                        f"'{tag}' was already present in the tags dictionary.\nRaised in the '{item}' item"
                    )
                global_tags.add(tag)

            if item in RUNTIMEPARSER_MAPPING_CONTEXTMANGERS:
                with RUNTIMEPARSER_MAPPING_CONTEXTMANGERS[item](**Attributes(attrib)):
                    self._parse_recursive(parent=attrib["_children"])

            elif item in RUNTIMEPARSER_MAPPING_ITEMS_FULL:
                RUNTIMEPARSER_MAPPING_ITEMS_FULL[item](**Attributes(attrib))

            # for special cases
            elif item in global_custom_dpg_items:
                global_custom_dpg_items[item](item, attrib)

            else:
                raise DPGJSONStructureError(
                    f"'{item}' dpg item name could not be parsed as a default iterm or a custom item"
                )

    # ------------------------------------------------------------------------------------------------------------------
    # - Special DPG items -
    # ------------------------------------------------------------------------------------------------------------------
    @custom_dpg_item(name="primary_window")
    def primary_window(self, _: str, attrib: dict):
        attrib[TAG] = PRIMARY_WINDOW
        global_tags.add(PRIMARY_WINDOW)

        with dpg.window(**Attributes(attrib)):
            self._parse_recursive(parent=attrib["_children"])

        dpg.set_primary_window(PRIMARY_WINDOW, True)

    @custom_dpg_item(name="viewport")
    def viewport(self, _:str, attrib:dict):
        dpg.create_viewport(**attrib)

    @custom_dpg_item(name="grid_layout")
    def grid_layout(self, _:str, attrib:dict):
        with dpg.table(**Attributes(attrib), header_row=False):
            # columns
            for column in attrib["_columns"]:
                dpg.add_table_column(**column)

            # rows with the items
            if "_rows" in attrib and len(attrib["_rows"]) == 1:
                attrib_rows = (attrib["_rows"],)*len(attrib["_children"])
            elif "_rows" in attrib and len(attrib["_rows"]) > 1:
                attrib_rows = attrib["_rows"]
            elif "_row_all" in attrib:
                attrib_rows = (attrib["_row_all"],)*len(attrib["_children"])
            else:
                attrib_rows = ({},)*len(attrib["_children"])

            for attrib_row, child in zip(attrib_rows, attrib["_children"]):
                with dpg.table_row(**attrib_row):
                   self._parse_recursive(child)