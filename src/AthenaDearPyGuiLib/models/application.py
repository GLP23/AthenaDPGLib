# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
import dearpygui.dearpygui as dpg
from dataclasses import dataclass, field

# Custom Library
from AthenaLib.models.version import Version

# Custom Packages
from AthenaDearPyGuiLib.models.filepaths import FilePaths
from AthenaDearPyGuiLib.functions.fixes import fix_icon_for_taskbar

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

    def __post_init__(self):
        self.app_model_id = f"{self.name.lower()}_{self.version.to_str(sep='.')}"

    def launch(self):

        dpg.create_context()

        dpg.create_viewport(
            title=self.app_model_id,
            small_icon=self.filepaths.icon,
            large_icon=self.filepaths.icon
        )

        fix_icon_for_taskbar(self.app_model_id)

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui() # blocking call
        dpg.destroy_context()
