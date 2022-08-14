# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from typing import Callable
import functools

# Custom Library
from AthenaLib.functions.mappings import append_or_new_list_to_mapping

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Callbacks:
    # part of the actual class?
    mapping_callback:dict[str:list[Callable]] = {}
    mapping_drag_callback:dict[str:list[Callable]] = {}
    mapping_drop_callback:dict[str:list[Callable]] = {}
    mapping_viewport_resize:dict[str:list[Callable]] = {}

    def _chain(self, sender, app_data, user_data:None=None, *,mapping:dict):
        for fnc in mapping[sender]:
            fnc(self=self,sender=sender, app_data=app_data, user_data=user_data)

    def chain_callback(self, sender, app_data, user_data:None=None):
        self._chain(sender, app_data, user_data, mapping=self.mapping_callback)

    def chain_drag_callback(self, sender, app_data, user_data:None=None):
        self._chain(sender, app_data, user_data, mapping=self.mapping_drag_callback)

    def chain_drop_callback(self, sender, app_data, user_data:None=None):
        self._chain(sender, app_data, user_data, mapping=self.mapping_drop_callback)

    def chain_viewport_resize(self):
        # execute all viewport resize callbacks in order
        #   Fixes a lot of issues most of the time
        for _, fnc in self.mapping_viewport_resize.items():
            fnc(self=self)

    @classmethod
    def callback(cls,items:list[str]):
        @functools.wraps(cls)
        def decoration(fnc:Callable):
            for item_name in items: #type: str
                append_or_new_list_to_mapping(mapping=cls.mapping_callback, key=item_name, value=fnc)
        return decoration

    @classmethod
    def drag_callback(cls, fnc:Callable ):
        cls.mapping_drag_callback[fnc.__name__] = fnc
        return fnc

    @classmethod
    def drop_callback(cls, fnc:Callable):
        cls.mapping_drop_callback[fnc.__name__] = fnc
        return fnc

    @classmethod
    def viewport_resize(cls, fnc:Callable):
        cls.mapping_viewport_resize[fnc.__name__] = fnc
        return fnc
