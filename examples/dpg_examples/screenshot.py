# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import dearpygui.dearpygui as dpg
from PIL import Image

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def picture_of_window(_, buffer:dpg.mvBuffer):
    x,y = dpg.get_item_pos("window")
    width = dpg.get_item_width("window")
    height = dpg.get_item_height("window")

    image = Image.frombuffer(
        mode="RGBA",
        size=(buffer.get_width(), buffer.get_height()),
        data=buffer
    )
    image.save("screenshot_window.png")

    image_edit = image.crop((x,y, width, height))
    image_edit.save("screenshot_window_edit.png")


def main():
    dpg.create_context()
    dpg.create_viewport(title='Screenshot Example')

    with dpg.window(tag="window",label="Screenshot Example"):
        dpg.add_text("Hello world!")
        dpg.add_button(
            label="Press me, to take a screenshot of the viewport",
            callback=lambda : dpg.output_frame_buffer(file="screenshot_viewport.png")
        )
        dpg.add_button(
            label="Press me, to take a screenshot of this window",
            callback=lambda : dpg.output_frame_buffer(callback=picture_of_window)
        )

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    main()