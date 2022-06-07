# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Viewport:
    def viewport_define(self):
        dpg.create_viewport(
            title=self.info.name,
            # icons are set up in the method self._viewport_icon()
            # small_icon=...,
            # large_icon=...,

            width=self.settings.width,
            height=self.settings.height,
            x_pos=self.settings.x_pos,
            y_pos=self.settings.y_pos,
            min_width=self.info.min_width,
            max_width=self.info.max_width,
            min_height=self.info.min_height,
            max_height=self.info.max_height,
            resizable=self.info.resizable,
            # vsync=None,
            always_on_top=self.info.always_on_top,
            decorated=self.info.decorated,
            # Clear color is handled by self.set_background_color()
            # clear_color=...,
        )

        # Define the icon for the viewport
        self._viewport_icon()

        # return self to chain methods after eachother
        return self

    def _viewport_icon(self):
        # in the info class this can be defined
        if self.info.icon_to_taskbar:
            # Define application ICON,
            #   makes sure the APPLICATION icon is shown in the taskbar
            if sys.platform == "win32":  # WINDODWS NEEDS THIS to make this possible
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    f"{self.info.name}[{self.info.version_to_str()}]"
                )
            elif sys.platform in ("linux", "linux2"):
                # TODO fix this! (aka, find out how to do this)
                raise NotImplementedError(strings.linux_notimplementederror)
