# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
import pathlib
from dataclasses import dataclass, field

# Custom Library
from AthenaLib.constants.types import PATHLIKE

# Custom Packages
from AthenaDPGLib.general.data.universal_tags import UniversalTags

# ----------------------------------------------------------------------------------------------------------------------
# - Support Code -
# ----------------------------------------------------------------------------------------------------------------------
DPG_ALLOWED_IMAGE_EXT = [".jpg", ".png", ".bmp", ".psd", ".gif", ".hdr",".pic", ".ppm", ".pgm"]
# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
@dataclass(kw_only=True, slots=True)
class TextureRegistry:

    #non init
    _registry:str|int = field(init=False)

    def __post_init__(self):
        self._registry = dpg.add_texture_registry(tag=UniversalTags.TA_texture_registry)

    def load_picture(self, filepath:PATHLIKE, tag:str|UniversalTags):
        # this is not a sufficient check
        #   As an extension doesn't change the filetype
        #   But for now, this is fine
        if not (path:=pathlib.Path(filepath)).suffix.lower() in DPG_ALLOWED_IMAGE_EXT:
            raise ValueError(path)
        # Retrieve the data from the loaded image and store it in the registry
        width, height, channels, data = dpg.load_image(filepath)
        dpg.add_static_texture(
            parent=self._registry,
            width=width,
            height=height,
            default_value=data,
            tag=tag
        )
