# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from dataclasses import dataclass,field

# Custom Library

# Custom Packages
from AthenaDPGLib.models.callbacks import Callbacks
from AthenaDPGLib.models.components.translation.component_translation import ComponentTranslation
from AthenaDPGLib.models.components.ui_parser.component_ui_parser import ComponentUIParser
from AthenaDPGLib.models.component import Component
from AthenaDPGLib.functions.fixes import fix_icon_for_taskbar

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True, kw_only=True)
class Application:
    name:str

    # non init
    viewport_id:str|int|None = field(init=False)
    components:list[Component] = field(init=False, default_factory=list)
    _parser:ComponentUIParser = field(init=False)
    _translation:ComponentTranslation = field(init=False)

    def __post_init__(self):
        # always makes sure the context exists
        dpg.create_context()

        # noinspection PyNoneFunctionAssignment
        self.viewport_id = dpg.create_viewport(title=self.name)
        fix_icon_for_taskbar(app_model_id=self.name)

    # ------------------------------------------------------------------------------------------------------------------
    # - Component Properties -
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def parser(self):
        return self._parser
    @parser.setter
    def parser(self, value:ComponentUIParser):
        self._parser = value
        self._parser.component_startup()

    @property
    def translation(self):
        return self._translation
    @translation.setter
    def translation(self, value:ComponentTranslation):
        self._translation = value
        self._translation.component_startup()

    def parse_callbacks(self):
        """
        Goes over all registered callbacks and sets the items' callbacks accordingly
        Will raise errors if the tag doesn't exist yet
        """
        for tag in Callbacks.mapping_callback:
            dpg.set_item_callback(item=tag, callback=Callbacks.chain_callback)
        for tag in Callbacks.mapping_drag_callback:
            dpg.set_item_callback(item=tag, callback=Callbacks.chain_drag_callback)
        for tag in Callbacks.mapping_drop_callback:
            dpg.set_item_callback(item=tag, callback=Callbacks.chain_drop_callback)

        dpg.set_viewport_resize_callback(callback=Callbacks.chain_viewport_resize)

    def run(self):
        self.startup()
        self.main()
        self.closedown()

    def startup(self):
        pass

    def main(self):
        dpg.setup_dearpygui()
        dpg.show_viewport()

        # BLOCKING
        dpg.start_dearpygui()

    def closedown(self):
        dpg.destroy_context()

        for component in self.components:
            component.component_closedown()

