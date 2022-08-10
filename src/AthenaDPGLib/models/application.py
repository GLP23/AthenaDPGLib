# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
import dearpygui.dearpygui as dpg
from dataclasses import dataclass, field

# Custom Library
from AthenaLib.models.version import Version

# Custom Packages
from AthenaDPGLib.functions.fixes import fix_icon_for_taskbar
from AthenaDPGLib.models.filepaths import FilePaths
from AthenaDPGLib.models.dpg_component import DpgComponent
from AthenaDPGLib.models.components.basic.window import Window

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(slots=True)
class Application:
    name:str
    version:Version

    filepaths:FilePaths = field(default_factory=FilePaths)

    # non init stuff
    app_model_id:str = field(init=False)
    content:dict[str:DpgComponent] = field(init=False, default_factory=dict)

    def __post_init__(self):
        self.app_model_id = f"{self.name.lower()}_{self.version.to_str(sep='.')}"

        # create the context, else dpg will not work
        dpg.create_context()

    def launch(self):

        for component_id,component in self.content.items(): #type: str, DpgComponent
            dpg.unstage(component.stage)

        dpg.create_viewport(
            title=self.app_model_id,
            small_icon=self.filepaths.icon,
            large_icon=self.filepaths.icon,
            x_pos=1080+100 # todo remove in final version
        )
        fix_icon_for_taskbar(self.app_model_id)

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui() # blocking call
        dpg.destroy_context()

    # ------------------------------------------------------------------------------------------------------------------
    # - Code -
    # ------------------------------------------------------------------------------------------------------------------
    def register_component(self, component:DpgComponent):
        self.content[component.id] = component

