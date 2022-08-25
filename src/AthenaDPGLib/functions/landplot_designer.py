# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg

# Custom Library
from AthenaLib.data.types import PATHLIKE

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def mouse_press_callback(sender, app_data, *, radius:int=10):
    pos = dpg.get_mouse_pos(local=True)
    with dpg.draw_layer(parent="drawlist_test"):
        dpg.draw_circle((pos[0]-radius/2, pos[1]-radius/2),radius=radius, fill=(255,255,255,255))


def wnd_landplot_designer(background_path:PATHLIKE):
    # Define the background texture and assign it to the window
    width, height, channels, data = dpg.load_image(background_path)
    with dpg.texture_registry():
        dpg.add_static_texture(width, height, data, tag="background_id")

    with dpg.item_handler_registry(tag="background_registry"):
        dpg.add_item_clicked_handler(callback=mouse_press_callback)
        # dpg.add_mouse_click_handler(callback=mouse_press_callback)

    with dpg.window(tag="wnd_landplot_designer"):
        with dpg.drawlist(tag="drawlist_test", width=width/5, height=height/5):
            dpg.draw_image("background_id", (0,0), (width/5,height/5))

    dpg.bind_item_handler_registry("drawlist_test","background_registry")
