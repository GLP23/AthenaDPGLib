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
    mapping_drag:ClassVar[dict[str:list[Callable]]] = {}
    mapping_drop:ClassVar[dict[str:list[Callable]]] = {}
    mapping_viewport_resize:ClassVar[list[Callable]] = []
    mapping_on_close:ClassVar[dict[str:list[Callable]]] = {}

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
    def drag(cls,items:list[str]):
        """
        Registers the function is to be bound as a `drag_callback` to the items which tags are given in the `items` arg
        """
        @functools.wraps(cls)
        def decoration(fnc:Callable):
            for item_name in items: #type: str
                append_or_extend_list_to_mapping(mapping=cls.mapping_drag, key=item_name, value=fnc)
        return decoration

    @classmethod
    def drop(cls,items:list[str]):
        """
        Registers the function is to be bound as a `drop_callback` to the items which tags are given in the `items` arg
        """
        @functools.wraps(cls)
        def decoration(fnc:Callable):
            for item_name in items: #type: str
                append_or_extend_list_to_mapping(mapping=cls.mapping_drop, key=item_name, value=fnc)
        return decoration

    @classmethod
    def on_close(cls,items:list[str]):
        """
        Registers the function is to be bound as a `on_close` to the items which tags are given in the `items` arg
        """
        @functools.wraps(cls)
        def decoration(fnc:Callable):
            for item_name in items: #type: str
                append_or_extend_list_to_mapping(mapping=cls.mapping_on_close, key=item_name, value=fnc)
        return decoration

    @classmethod
    def viewport_resize(cls, fnc):
        """
        Registers the function is to be bound as a `viewport_resize_callback`
        """
        cls.mapping_viewport_resize.append(fnc)
        return fnc