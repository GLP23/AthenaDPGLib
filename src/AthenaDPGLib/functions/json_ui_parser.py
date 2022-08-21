# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import json

# Custom Library
from AthenaLib.data.types import PATHLIKE

# Custom Packages
from AthenaDPGLib.data.json_ui_parser_mappings import JSONUIPARSER_ITEMS, JSONUIPARSER_CONTEXTMANGERS

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
error_tag = lambda tag, item : ValueError(
    f"'{tag}' was already present in the tags dictionary.\nRaised in '{item}' item"
)
error_item = lambda item : ValueError(
    f"'{item}' dpg item name could not be parsed as a default dpg item or a custom item"
)
error_file = lambda filepath : ValueError(
    f"The file `{filepath}` had no usable structure"
)

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
def json_ui_parser(filepath:PATHLIKE, custom_dpg_items:dict, tags:set):
    """
    Parses the given json file at the `filepath_input` argument.
    Make sure that the dpg.create_context() has been run before this method is run

    Made as a standalone function to be used outside an AthenaApplication manner
    """

    # Open file and  close as possible
    with open(filepath, "r") as file:
        document = json.load(file)

    try:
        # check for file structure
        dpg_data = document["dpg"]
    except KeyError:
        raise error_file(filepath)

    # parse with the correct parser
    match dpg_data:
        # version specific parsing
        #   Currently this means nothing as there is only one parser version
        #   This is meant for the future where there might eventually be multiple versions of parser,
        #       And this will ensure that the "old" ui files don't break
        case {"_parser": {"version": 0}, "_children": children, }:
            _recursive_json_ui_parser(parent=children, custom_dpg_items=custom_dpg_items,tags=tags)

        # If the version hasn't been specified , it will automatically pick the newest parser
        case {"_children": children, }:
            _recursive_json_ui_parser(parent=children, custom_dpg_items=custom_dpg_items,tags=tags)

        case _:
            raise error_file(filepath)

def _recursive_json_ui_parser(parent:list,custom_dpg_items:dict, tags:set):
        """
        Recursive part of the parser.
        It will recursively parse all child items of DPG items that are run with a context manager (with statement).
        """
        for item, attrib in ((k,v) for i in parent for k, v in i.items()): #type: str, dict
            if "tag" in attrib:
                if (tag := attrib["tag"]) in tags:
                    raise error_tag(tag, item)
                tags.add(tag)

            if item in JSONUIPARSER_CONTEXTMANGERS:
                # run the item with a context.
                #   Else the child items will not be correctly placed within the parent item
                with JSONUIPARSER_CONTEXTMANGERS[item](**attrib):
                    _recursive_json_ui_parser(parent=attrib["_children"],custom_dpg_items=custom_dpg_items,tags=tags)

            elif item in JSONUIPARSER_ITEMS:
                # run the item creation normally
                #   aka: dpg.add_...
                JSONUIPARSER_ITEMS[item](**attrib)

            # for special cases
            elif item in custom_dpg_items:
                # Custom implemented items that either don't have a "normal" dpg function
                #   or are a collection of predefined items
                custom_dpg_items[item](item, attrib)

            else:
                raise error_item(item)
