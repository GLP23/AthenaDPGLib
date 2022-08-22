# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
from dataclasses import dataclass
import dearpygui.dearpygui as dpg

# Custom Library

# Custom Packages
from AthenaDPGLib.models.athena_application.athena_application import SubSystem
from AthenaDPGLib.models.custom_callbacks import CustomCallbacks

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class SubSystem_CustomCallbacks(SubSystem):
    """
    Sub System which has to be run after the DPG context has been generated
        and after any GUI elements have been generated
    """

    def run(self):
        self.apply_callbacks()
        self.apply_viewport_resize_callbacks()

    # ------------------------------------------------------------------------------------------------------------------
    # - Apply callbacks to ui -
    # ------------------------------------------------------------------------------------------------------------------
    def apply_callbacks(self):
        """
        Goes over all registered callbacks and sets the items' callbacks accordingly
        Will raise errors if the tag doesn't exist yet.
        This system works because CustomCallbacks only has ClassVar and ClassMethods
        """
        callbacks = [
            (CustomCallbacks.mapping_callback,  {"callback": self.chain_callback}),
            (CustomCallbacks.mapping_drag,      {"drag_callback":self.chain_drag}),
            (CustomCallbacks.mapping_drop,      {"drop_callback":self.chain_drop}),
            (CustomCallbacks.mapping_on_close,  {"on_close":self.chain_on_close}),
        ]

        # gather all active aliases and execute the callbacks on them
        aliases = dpg.get_aliases()
        for mapping, kwargs in callbacks:
            for tag in (t for t in mapping if t in aliases):
                # make sure the thing exists
                if dpg.does_item_exist(item=tag):
                    dpg.configure_item(item=tag, **kwargs)

    def apply_viewport_resize_callbacks(self):
        dpg.set_viewport_resize_callback(callback=self.chain_viewport_resize)

    def apply_callbacks_specific(self,items: set[str]):
        """
        Goes over all items and sets those item's callbacks if the dpg items exist
        This system works because CustomCallbacks only has ClassVar and ClassMethods
        """

        for tag in items:
            if dpg.does_item_exist(item=tag):
                if tag in CustomCallbacks.mapping_callback:
                    dpg.configure_item(item=tag, callback=self.chain_callback)

                if tag in CustomCallbacks.mapping_drag:
                    dpg.configure_item(item=tag, drag_callback=self.chain_drag)

                if tag in CustomCallbacks.mapping_drop:
                    dpg.configure_item(item=tag, drop_callback=self.chain_drop)

                if tag in CustomCallbacks.mapping_on_close:
                    dpg.configure_item(item=tag, on_close=self.chain_on_close)

    # ------------------------------------------------------------------------------------------------------------------
    # - Code -
    # ------------------------------------------------------------------------------------------------------------------
    def _chain(self, sender, app_data, user_data:None=None, *,mapping:dict):
        for fnc in mapping[sender]:
            fnc(self=self,sender=sender, app_data=app_data, user_data=user_data)

    def chain_callback(self, sender, app_data, user_data:None=None):
        """
        Function which executes the bound functions to the sender's `callback` function.
        The order is defined by at which moment the functions were registered.
        """
        self._chain(sender, app_data, user_data, mapping=CustomCallbacks.mapping_callback)

    def chain_drag(self, sender, app_data, user_data:None=None):
        """
        Function which executes the bound functions to the sender's `drag_callback` function.
        The order is defined by at which moment the functions were registered.
        """
        self._chain(sender, app_data, user_data, mapping=CustomCallbacks.mapping_drag)

    def chain_drop(self, sender, app_data, user_data:None=None):
        """
        Function which executes the bound functions to the sender's `drop_callback` function.
        The order is defined by at which moment the functions were registered.
        """
        self._chain(sender, app_data, user_data, mapping=CustomCallbacks.mapping_drop)

    def chain_on_close(self, sender, app_data, user_data:None=None):
        """
        Function which executes the bound functions to the sender's `on_close` function.
        The order is defined by at which moment the functions were registered.
        """
        self._chain(sender, app_data, user_data, mapping=CustomCallbacks.mapping_on_close)

    def chain_viewport_resize(self):
        """
        Allows for multiple functions to be bound to one viewport_resize callback function
        """
        # execute all viewport resize callbacks in order
        #   Fixes a lot of issues most of the time
        for fnc in CustomCallbacks.mapping_viewport_resize:
            fnc(self=self)