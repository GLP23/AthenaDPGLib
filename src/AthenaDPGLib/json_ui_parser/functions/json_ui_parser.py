# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import json

# Custom Library
from AthenaLib.data.types import PATHLIKE

# Custom Packages
from AthenaDPGLib.json_ui_parser.models.custom_dpg_items import CustomDPGItems
from AthenaDPGLib.json_ui_parser.data.json_ui_parser_mappings import JSONUIPARSER_ITEMS, JSONUIPARSER_CONTEXT_MANAGERS
from AthenaDPGLib.json_ui_parser.data.exceptions import error_item, error_file

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
def _item_and_attrib_generator(children:list) ->  tuple[str, dict] :
    for item, attrib in ((k, v) for i in children for k, v in i.items()):
        yield item, attrib

def _attrib_generator(attrib:dict)->dict:
    # TODO quick fix, eventually this has to be changed to a better system but works as intended
    return {k:v for k,v in attrib.items() if not k.startswith("_")}

def _recursive_parser(item: str, attrib: dict, *, custom_dpg_items: type[CustomDPGItems]|CustomDPGItems):
    """
    Recursive part of the parser.
    It will recursively parse all child items of DPG items that are run with a context manager (with statement).
    """

    # for special cases
    #   run first because maybe a custom item name replaces a "normally named dpg item"
    if item in custom_dpg_items.items:
        # Regular dpg.add_... or equivalent function
        custom_dpg_items.items[item](attrib=_attrib_generator(attrib))

    elif item in custom_dpg_items.items_context_managed:
        # item needs to be context managed because it has child items.
        with custom_dpg_items.items_context_managed[item](attrib=_attrib_generator(attrib)):
            for i, a in _item_and_attrib_generator(attrib["_children"]):
                _recursive_parser(item=i, attrib=a, custom_dpg_items=custom_dpg_items)

    elif item in JSONUIPARSER_CONTEXT_MANAGERS:
        # run the item with a context.
        #   Else the child items will not be correctly placed within the parent item
        with JSONUIPARSER_CONTEXT_MANAGERS[item](**_attrib_generator(attrib)):
            # Go over all items and it's descendants if needed
            for item, attrib in _item_and_attrib_generator(attrib["_children"]):
                _recursive_parser(item=item, attrib=attrib, custom_dpg_items=custom_dpg_items)

    elif item in JSONUIPARSER_ITEMS:
        # run the item creation normally
        #   aka: dpg.add_...
        JSONUIPARSER_ITEMS[item](**_attrib_generator(attrib))

    else:
        raise error_item(item)

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def json_ui_parser(filepath:PATHLIKE, *, custom_dpg_items:CustomDPGItems=None):
    """
    Parses the given json file at the `filepath_input` argument.
    Make sure that the dpg.create_context() has been run before this method is run

    Made as a standalone function to be used outside an AthenaApplication manner
    """
    # Created here to make sure they are present and usable by the recursive parser
    #   Here they are created once, instead of on every `_recursive_parser` call
    if custom_dpg_items is None:
        custom_dpg_items = CustomDPGItems # this is an empty object and should work as is

    # Error catching block specifically placed here
    #   Else all `KeyError` exceptions within the parser will be caught
    #   Which should be done at all, as it will catch unintended stuff
    try:
        with open(filepath, "r") as file:
            document = json.load(file)
        # check for file structure
        #   Will error out if the "root" key value pair structure doesn't exist
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
            for item, attrib in _item_and_attrib_generator(children):
                _recursive_parser(item=item, attrib=attrib, custom_dpg_items=custom_dpg_items)

        # No usable format could be found
        case _:
            raise error_file(filepath)

    # function doesn't return anything
    #   Both `custom_dpg_items` and `tags` are expected to be mutable and don't need to be returned
    #   No items are created, as dpg functions only create items internally
    #       Although dpg.add_... or the context managed items do return item tags,
    #           it is expected for any meaningfully tags to be set as attributes in the json files
    #       This way the tags remain unique and exist "separate" from the parser