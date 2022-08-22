# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Callable, ClassVar
import functools

# Custom Library
from AthenaLib.functions.mappings import append_or_extend_list_to_mapping

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class CustomCallbacks:
    # part of the actual class
    mapping_callback:ClassVar[dict[str:list[Callable]]] = {}
    mapping_drag_callback:ClassVar[dict[str:list[Callable]]] = {}
    mapping_drop_callback:ClassVar[dict[str:list[Callable]]] = {}
    mapping_viewport_resize:ClassVar[list[Callable]] = []

    @classmethod
    def _chain(cls, sender, app_data, user_data:None=None, *,mapping:dict):
        for fnc in mapping[sender]:
            fnc(self=cls,sender=sender, app_data=app_data, user_data=user_data)

    @classmethod
    def chain_callback(cls, sender, app_data, user_data:None=None):
        """
        Function which executes the bound functions to the sender's `callback` function.
        The order is defined by at which moment the functions were registered.
        """
        cls._chain(sender, app_data, user_data, mapping=cls.mapping_callback)

    @classmethod
    def chain_drag_callback(cls, sender, app_data, user_data:None=None):
        """
        Function which executes the bound functions to the sender's `drag_callback` function.
        The order is defined by at which moment the functions were registered.
        """
        cls._chain(sender, app_data, user_data, mapping=cls.mapping_drag_callback)

    @classmethod
    def chain_drop_callback(cls, sender, app_data, user_data:None=None):
        """
        Function which executes the bound functions to the sender's `drop_callback` function.
        The order is defined by at which moment the functions were registered.
        """
        cls._chain(sender, app_data, user_data, mapping=cls.mapping_drop_callback)

    @classmethod
    def chain_viewport_resize(cls):
        """
        Allows for multiple functions to be bound to one viewport_resize callback function
        """
        # execute all viewport resize callbacks in order
        #   Fixes a lot of issues most of the time
        for fnc in cls.mapping_viewport_resize:
            fnc()

    @classmethod
    def callback(cls,items:list[str]):
        """
        Registers the function is to be bound as a `callback` to the items which tags are given in the `items` arg
        """
        @functools.wraps(cls)
        def decoration(fnc:Callable):
            for item_name in items: #type: str
                append_or_extend_list_to_mapping(mapping=cls.mapping_callback, key=item_name, value=fnc)
        return decoration

    @classmethod
    def drag_callback(cls,items:list[str]):
        """
        Registers the function is to be bound as a `drag_callback` to the items which tags are given in the `items` arg
        """
        @functools.wraps(cls)
        def decoration(fnc:Callable):
            for item_name in items: #type: str
                append_or_extend_list_to_mapping(mapping=cls.mapping_drag_callback, key=item_name, value=fnc)
        return decoration

    @classmethod
    def drop_callback(cls,items:list[str]):
        """
        Registers the function is to be bound as a `drop_callback` to the items which tags are given in the `items` arg
        """
        @functools.wraps(cls)
        def decoration(fnc:Callable):
            for item_name in items: #type: str
                append_or_extend_list_to_mapping(mapping=cls.mapping_drop_callback, key=item_name, value=fnc)
        return decoration

    @classmethod
    def viewport_resize(cls, fnc):
        """
        Registers the function is to be bound as a `viewport_resize_callback`
        """
        cls.mapping_viewport_resize.append(fnc)
        return fnc